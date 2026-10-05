# Input Schemas

All three scripts read JSON. `assets/sample-campaign-data.json` shows the three shapes in one file (invented data). Validate syntax first with `python3 -m json.tool file.json`.

On bad data a script prints `error: ...` to stderr and exits with code 2. It names the field.

## Journeys: `attribute_journeys.py`

```json
{
  "journeys": [
    {
      "journey_id": "j001",
      "touchpoints": [
        {"channel": "organic_search", "timestamp": "2026-03-01T10:00:00"},
        {"channel": "email", "timestamp": "2026-03-05T14:30:00"}
      ],
      "converted": true,
      "revenue": 240.0,
      "converted_at": "2026-03-06T09:00:00"
    }
  ]
}
```

| Field | Required | Rule |
|---|---|---|
| `touchpoints[].channel` | yes | Non-empty string. Use one spelling per channel |
| `touchpoints[].timestamp` | yes | ISO 8601 date or datetime. Zone-aware values convert to UTC |
| `converted` | no | Default false. Unconverted journeys feed the Reach table only |
| `revenue` | when converted, unless `--value conversions` | Number >= 0 |
| `converted_at` | no | Anchors time-decay. Default is the last touch time. Touches after it are dropped |
| `journey_id` | no | Label only |

## Funnel: `analyze_funnel.py`

```json
{
  "funnel": {"stages": ["Visit", "Cart", "Purchase"], "counts": [5000, 900, 300]},
  "segments": {"paid": {"counts": [2000, 300, 80]}, "organic": {"counts": [3000, 600, 220]}}
}
```

- `stages` and `counts`: same length, at least 2. Counts must not rise from stage to stage.
- Each segment needs `counts` of the same length. Segments should not overlap.
- `--value-per-conversion` is optional and prices the gap-to-best figure.

## Campaigns: `campaign_roi.py`

```json
{
  "campaigns": [
    {
      "name": "Spring Welcome Series",
      "channel": "email",
      "spend": 1800,
      "other_costs": 900,
      "revenue": 41000,
      "impressions": 64000,
      "clicks": 3100,
      "leads": 520,
      "customers": 260
    }
  ]
}
```

- Money and counts are numbers >= 0. A missing field counts as 0.
- `channel` should match a benchmark key (`email`, `paid_search`, `paid_social`, `display`, `organic_search`, `organic_social`, `referral`, `direct`). Others use `default` and trigger a warning.
- `clicks` greater than `impressions` is an error, unless `impressions` is 0 (not tracked).
- `revenue` should come from one attribution view. See `attribution-models.md`.
- One currency only. The scripts do no conversion.

## Data prerequisites

- Journey data needs user-level or session-level paths with timestamps. Aggregate platform reports do not contain paths and cannot feed the attribution script.
- If you have no path data, use the funnel and ROI scripts. Say that attribution was not possible.
- Use only data the user owns or is allowed to analyze. Strip personal identifiers before analysis; the scripts need none.
