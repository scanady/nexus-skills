#!/usr/bin/env python3
"""Checks for the attribution, funnel, and ROI scripts.

Usage:
    python3 test_toolkit.py              run every check
    python3 test_toolkit.py --regenerate rewrite assets/sample-expected-output.json
"""

import json
import sys
import unittest
from datetime import datetime, timedelta

import analyze_funnel as funnel
import attribute_journeys as attribution
import campaign_roi as roi
from campaign_data import ASSETS, InputError, load_json

SAMPLE = ASSETS / "sample-campaign-data.json"
EXPECTED = ASSETS / "sample-expected-output.json"


def run_sample():
    data = load_json(SAMPLE)
    return {
        "attribution": attribution.analyze(data, attribution.MODELS, 7.0, "revenue"),
        "funnel": funnel.analyze(data, 95.0),
        "roi": roi.analyze(data, roi.load_benchmarks()),
    }


def journey(channels, days, revenue=100.0, **extra):
    start = datetime(2026, 1, 1)
    return {
        "touchpoints": [
            {"channel": c, "timestamp": (start + timedelta(days=d)).isoformat()} for c, d in zip(channels, days)
        ],
        "converted": True,
        "revenue": revenue,
        **extra,
    }


class AttributionTests(unittest.TestCase):
    def test_position_based_weights(self):
        self.assertEqual(attribution.weights("position-based", [0] * 4, None, 7), [0.4, 0.1, 0.1, 0.4])
        self.assertEqual(attribution.weights("position-based", [0] * 2, None, 7), [0.5, 0.5])
        self.assertEqual(attribution.weights("position-based", [0], None, 7), [1.0])

    def test_time_decay_halves_every_half_life(self):
        touches = [(datetime(2026, 1, 1), "a"), (datetime(2026, 1, 8), "b")]
        first, last = attribution.weights("time-decay", touches, datetime(2026, 1, 8), 7)
        self.assertAlmostEqual(first, 1 / 3)
        self.assertAlmostEqual(last, 2 / 3)

    def test_decay_anchors_to_conversion_time(self):
        journeys, _ = attribution.load_journeys(
            {"journeys": [journey(["a", "b"], [0, 7], converted_at="2026-01-15T00:00:00")]}, "revenue"
        )
        first, last = attribution.weights("time-decay", journeys[0]["touches"], journeys[0]["converted_at"], 7)
        self.assertAlmostEqual(first / last, 0.5)
        self.assertAlmostEqual(first + last, 1.0)

    def test_every_model_credits_the_full_revenue(self):
        journeys, _ = attribution.load_journeys(
            {"journeys": [journey(["a", "b", "c"], [0, 2, 5], 300), journey(["b"], [0], 50)]}, "revenue"
        )
        for model in attribution.MODELS:
            self.assertAlmostEqual(sum(attribution.credit_by_channel(model, journeys, 7).values()), 350.0, msg=model)

    def test_touch_after_conversion_is_dropped(self):
        journeys, late = attribution.load_journeys(
            {"journeys": [journey(["a", "b"], [0, 9], converted_at="2026-01-05T00:00:00")]}, "revenue"
        )
        self.assertEqual(late, 1)
        self.assertEqual(len(journeys[0]["touches"]), 1)

    def test_bad_input_raises(self):
        no_revenue = journey(["a"], [0])
        del no_revenue["revenue"]
        with self.assertRaises(InputError):
            attribution.load_journeys({"journeys": [no_revenue]}, "revenue")
        with self.assertRaises(InputError):
            attribution.analyze({"journeys": [{**journey(["a"], [0]), "converted": False}]}, ["linear"], 7, "revenue")
        with self.assertRaises(InputError):
            attribution.load_journeys({"journeys": []}, "revenue")

    def test_conversion_count_mode_needs_no_revenue(self):
        no_revenue = journey(["a", "b"], [0, 1])
        del no_revenue["revenue"]
        result = attribution.analyze({"journeys": [no_revenue]}, ["linear"], 7, "conversions")
        self.assertEqual(result["summary"]["total_value"], 1.0)


class FunnelTests(unittest.TestCase):
    def test_wilson_interval_for_half(self):
        self.assertEqual(funnel.wilson(50, 100), [40.4, 59.6])

    def test_equal_rates_give_p_of_one(self):
        self.assertAlmostEqual(funnel.two_sided_p(50, 100, 50, 100), 1.0)

    def test_big_gap_is_significant(self):
        self.assertLess(funnel.two_sided_p(10, 100, 50, 100), 0.001)

    def test_rates_and_bottlenecks(self):
        result = funnel.analyze({"funnel": {"stages": ["a", "b", "c"], "counts": [1000, 400, 100]}}, None)
        self.assertEqual([r.get("rate_pct") for r in result["stages"]], [None, 40.0, 25.0])
        self.assertEqual(result["overall_conversion_pct"], 10.0)
        self.assertEqual(result["bottlenecks"]["largest_absolute_loss"]["transition"], "a -> b")
        self.assertEqual(result["bottlenecks"]["lowest_rate"]["transition"], "b -> c")

    def test_rising_counts_raise(self):
        with self.assertRaises(InputError):
            funnel.analyze({"funnel": {"stages": ["a", "b"], "counts": [10, 20]}}, None)

    def test_segment_gap_to_best(self):
        data = {
            "funnel": {"stages": ["a", "b"], "counts": [2000, 600]},
            "segments": {"x": {"counts": [1000, 400]}, "y": {"counts": [1000, 200]}},
        }
        result = funnel.analyze(data, 10.0)
        top = result["segments"]["findings"][0]
        self.assertEqual((top["segment"], top["gap_to_best_extra_conversions"]), ("y", 200.0))
        self.assertEqual(top["gap_to_best_extra_value"], 2000.0)
        self.assertTrue(top["differs"])


class RoiTests(unittest.TestCase):
    def test_metrics_by_hand(self):
        m = roi.metrics(1000, 500, 4500, 100000, 2000, 100, 50)
        self.assertEqual(
            (m["roi_pct"], m["roas"], m["loaded_roas"], m["cpa"], m["cpl"], m["cpc"], m["cpm"], m["ctr_pct"]),
            (200.0, 4.5, 3.0, 30.0, 15.0, 0.5, 10.0, 2.0),
        )
        self.assertEqual((m["click_to_lead_pct"], m["lead_to_customer_pct"], m["revenue_per_customer"]), (5.0, 50.0, 90.0))

    def test_undefined_ratios_are_none(self):
        m = roi.metrics(0, 0, 100, 0, 0, 0, 0)
        self.assertTrue(all(m[k] is None for k in ("roi_pct", "roas", "cpa", "cpl", "cpc", "cpm", "ctr_pct")))

    def test_band_direction(self):
        self.assertEqual(roi.band(5.0, (2, 4, 8), True), "good")
        self.assertEqual(roi.band(1.0, (2, 4, 8), True), "underperforming")
        self.assertEqual(roi.band(10, (15, 45, 120), False), "excellent")
        self.assertEqual(roi.band(200, (15, 45, 120), False), "underperforming")

    def test_unknown_channel_uses_default_and_warns(self):
        data = {"campaigns": [{"name": "x", "channel": "podcast", "spend": 100, "revenue": 50}]}
        result = roi.analyze(data, roi.load_benchmarks())
        self.assertTrue(result["campaigns"][0]["loses_money"])
        self.assertTrue(any("podcast" in w for w in result["warnings"]))

    def test_bad_input_raises(self):
        with self.assertRaises(InputError):
            roi.analyze({"campaigns": [{"spend": "lots"}]}, roi.load_benchmarks())
        with self.assertRaises(InputError):
            roi.analyze({"campaigns": [{"spend": 1, "impressions": 10, "clicks": 20}]}, roi.load_benchmarks())


class SampleTests(unittest.TestCase):
    def test_sample_output_matches_expected(self):
        self.assertEqual(json.loads(json.dumps(run_sample())), load_json(EXPECTED))


if __name__ == "__main__":
    if "--regenerate" in sys.argv:
        EXPECTED.write_text(json.dumps(run_sample(), indent=2) + "\n", encoding="utf-8")
        print(f"wrote {EXPECTED}")
    else:
        unittest.main()
