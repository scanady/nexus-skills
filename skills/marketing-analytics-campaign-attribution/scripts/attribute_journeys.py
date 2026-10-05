#!/usr/bin/env python3
"""Split conversion credit across channels with five multi-touch models.

Usage:
    python3 attribute_journeys.py journeys.json
    python3 attribute_journeys.py journeys.json --model time-decay --half-life 14
    python3 attribute_journeys.py journeys.json --value conversions --format json
"""

import argparse
import json
from collections import defaultdict

from campaign_data import InputError, fmt, load_json, main_guard, number, parse_time, table

MODELS = ("first-touch", "last-touch", "linear", "time-decay", "position-based")
MIN_CONVERTED = 30
SENSITIVE_SPREAD_PTS = 10.0


def load_journeys(data, value_mode):
    """Validate the input and return journeys with sorted touches."""
    raw = data.get("journeys")
    if not isinstance(raw, list) or not raw:
        raise InputError("'journeys' must be a non-empty list")

    journeys, late_touches = [], 0
    for index, item in enumerate(raw):
        where = f"journeys[{index}]"
        touches = item.get("touchpoints")
        if not isinstance(touches, list) or not touches:
            raise InputError(f"{where}.touchpoints: needs at least one touchpoint")
        parsed = sorted(
            (parse_time(t.get("timestamp"), f"{where}.touchpoints[{i}].timestamp"), t.get("channel"))
            for i, t in enumerate(touches)
        )
        if any(not isinstance(channel, str) or not channel for _, channel in parsed):
            raise InputError(f"{where}: every touchpoint needs a non-empty 'channel'")

        converted = bool(item.get("converted", False))
        revenue, converted_at = 0.0, None
        if converted:
            if value_mode == "revenue":
                if "revenue" not in item:
                    raise InputError(f"{where}: converted journey has no 'revenue' (or use --value conversions)")
                revenue = number(item["revenue"], f"{where}.revenue")
            converted_at = (
                parse_time(item["converted_at"], f"{where}.converted_at")
                if "converted_at" in item
                else parsed[-1][0]
            )
            kept = [p for p in parsed if p[0] <= converted_at]
            late_touches += len(parsed) - len(kept)
            if not kept:
                raise InputError(f"{where}: every touchpoint is after 'converted_at'")
            parsed = kept

        journeys.append(
            {
                "id": item.get("journey_id", f"#{index}"),
                "touches": parsed,
                "converted": converted,
                "value": revenue if value_mode == "revenue" else 1.0,
                "converted_at": converted_at,
            }
        )
    return journeys, late_touches


def weights(model, touches, converted_at, half_life):
    """Return one credit fraction per touch, in time order. Fractions sum to 1."""
    count = len(touches)
    if model == "first-touch":
        return [1.0] + [0.0] * (count - 1)
    if model == "last-touch":
        return [0.0] * (count - 1) + [1.0]
    if model == "linear":
        return [1 / count] * count
    if model == "position-based":
        if count == 1:
            return [1.0]
        if count == 2:
            return [0.5, 0.5]
        return [0.4] + [0.2 / (count - 2)] * (count - 2) + [0.4]
    raw = [0.5 ** ((converted_at - when).total_seconds() / 86400 / half_life) for when, _ in touches]
    total = sum(raw)
    return [w / total for w in raw]


def credit_by_channel(model, journeys, half_life):
    credit = defaultdict(float)
    for journey in journeys:
        if not journey["converted"]:
            continue
        fractions = weights(model, journey["touches"], journey["converted_at"], half_life)
        for (_, channel), fraction in zip(journey["touches"], fractions):
            credit[channel] += fraction * journey["value"]
    return credit


def rank(credit):
    total = sum(credit.values())
    ordered = sorted(credit.items(), key=lambda item: (-item[1], item[0]))
    return [
        {"channel": ch, "credit": round(v, 2), "share_pct": round(100 * v / total, 1)}
        for ch, v in ordered
    ]


def reach(journeys):
    """Per channel: journeys touched and how many of them converted."""
    touched, won = defaultdict(int), defaultdict(int)
    for journey in journeys:
        for channel in {channel for _, channel in journey["touches"]}:
            touched[channel] += 1
            won[channel] += journey["converted"]
    rows = [
        {
            "channel": ch,
            "journeys_touched": touched[ch],
            "converted_journeys": won[ch],
            "conversion_rate_pct": round(100 * won[ch] / touched[ch], 1),
        }
        for ch in touched
    ]
    return sorted(rows, key=lambda r: (-r["journeys_touched"], r["channel"]))


def sensitivity(model_results):
    """Per channel: how far its credit share moves between models."""
    by_model = [{row["channel"]: row["share_pct"] for row in ranked} for ranked in model_results.values()]
    channels = set().union(*by_model)
    shares = {ch: [seen.get(ch, 0.0) for seen in by_model] for ch in channels}
    rows = [
        {
            "channel": ch,
            "min_share_pct": min(vals),
            "max_share_pct": max(vals),
            "spread_pts": round(max(vals) - min(vals), 1),
            "model_sensitive": max(vals) - min(vals) >= SENSITIVE_SPREAD_PTS,
        }
        for ch, vals in shares.items()
    ]
    return sorted(rows, key=lambda r: (-r["spread_pts"], r["channel"]))


def analyze(data, models, half_life, value_mode):
    journeys, late_touches = load_journeys(data, value_mode)
    converted = [j for j in journeys if j["converted"]]
    if not converted:
        raise InputError("no converted journeys: nothing to attribute")

    single = sum(1 for j in converted if len(j["touches"]) == 1)
    warnings = []
    if len(converted) < MIN_CONVERTED:
        warnings.append(
            f"Only {len(converted)} converted journeys (< {MIN_CONVERTED}). Credit shares are anecdotal, not stable."
        )
    if single / len(converted) >= 0.5:
        warnings.append(
            f"{single} of {len(converted)} conversions have one touchpoint. Models agree on those by construction; "
            "check that the tracking records the full path."
        )
    if late_touches:
        warnings.append(f"Dropped {late_touches} touchpoint(s) that happened after the conversion time.")

    results = {name: rank(credit_by_channel(name, journeys, half_life)) for name in models}
    unit = "revenue" if value_mode == "revenue" else "conversions"
    return {
        "summary": {
            "journeys": len(journeys),
            "converted_journeys": len(converted),
            "conversion_rate_pct": round(100 * len(converted) / len(journeys), 1),
            "total_value": round(sum(j["value"] for j in converted), 2),
            "value_unit": unit,
            "single_touch_conversion_share_pct": round(100 * single / len(converted), 1),
            "time_decay_half_life_days": half_life,
        },
        "models": results,
        "reach": reach(journeys),
        "sensitivity": sensitivity(results) if len(results) > 1 else [],
        "warnings": warnings,
    }


def render(result):
    s = result["summary"]
    money = "$" if s["value_unit"] == "revenue" else ""
    out = [
        "MULTI-TOUCH ATTRIBUTION",
        f"  Journeys: {s['journeys']}   Converted: {s['converted_journeys']} ({s['conversion_rate_pct']}%)",
        f"  Total {s['value_unit']}: {money}{s['total_value']:,.2f}   "
        f"Single-touch conversions: {s['single_touch_conversion_share_pct']}%",
    ]
    for name, ranked in result["models"].items():
        out += ["", f"MODEL: {name}" + (f" (half-life {s['time_decay_half_life_days']}d)" if name == "time-decay" else "")]
        out.append(
            table(
                ["Channel", s["value_unit"].title(), "Share"],
                [(r["channel"], fmt(r["credit"], prefix=money), fmt(r["share_pct"], ".1f", suffix="%")) for r in ranked],
                [22, 14, 8],
            )
        )
    out += ["", "REACH (all journeys, converted or not)"]
    out.append(
        table(
            ["Channel", "Touched", "Converted", "Conv rate"],
            [
                (r["channel"], r["journeys_touched"], r["converted_journeys"], fmt(r["conversion_rate_pct"], ".1f", suffix="%"))
                for r in result["reach"]
            ],
            [22, 8, 10, 10],
        )
    )
    if result["sensitivity"]:
        out += ["", f"MODEL SENSITIVITY (flag when share moves >= {SENSITIVE_SPREAD_PTS:.0f} points)"]
        out.append(
            table(
                ["Channel", "Min share", "Max share", "Spread", "Flag"],
                [
                    (
                        r["channel"],
                        fmt(r["min_share_pct"], ".1f", suffix="%"),
                        fmt(r["max_share_pct"], ".1f", suffix="%"),
                        fmt(r["spread_pts"], ".1f", suffix=" pts"),
                        "sensitive" if r["model_sensitive"] else "",
                    )
                    for r in result["sensitivity"]
                ],
                [22, 10, 10, 10, 10],
            )
        )
    if result["warnings"]:
        out += ["", "WARNINGS", *(f"  - {w}" for w in result["warnings"])]
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("input_file", help="JSON file with a 'journeys' list")
    parser.add_argument("--model", choices=MODELS, help="run one model (default: all five)")
    parser.add_argument("--half-life", type=float, default=7.0, help="time-decay half-life in days (default 7)")
    parser.add_argument("--value", choices=("revenue", "conversions"), default="revenue", help="credit revenue or conversion counts")
    parser.add_argument("--format", choices=("text", "json"), default="text", dest="output_format")
    args = parser.parse_args()

    if args.half_life <= 0:
        raise InputError("--half-life must be > 0")
    result = analyze(load_json(args.input_file), [args.model] if args.model else MODELS, args.half_life, args.value)
    print(json.dumps(result, indent=2) if args.output_format == "json" else render(result))


if __name__ == "__main__":
    main_guard(main)
