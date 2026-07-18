# Agile Integration

Lean UX is built to run *inside* Agile, via **dual-track agile**: a discovery track (learn what to build) runs in parallel with a delivery track (build it), each feeding the other.

## Dual-Track

| Track | Purpose | Output |
|-------|---------|--------|
| Discovery | learn what to build — hypotheses, experiments, research, collaborative design, prototype tests | validated hypotheses, tested prototypes |
| Delivery | build the validated — planning, dev, QA, deploy, monitor | shippable software |

**Key rule:** only validated designs enter the delivery backlog; invalidated ones are dropped, pivoted, or retested — the delivery team never builds something discovery hasn't tested.

Discovery week: Mon review + new hypotheses · Tue collaborative design · Wed build prototype · Thu run 3–5 tests · Fri synthesize + update backlog. Delivery keeps standard ceremonies with modifications: each story carries its hypothesis + success metric; standup includes discovery updates; demo reports learnings not just features; retro reviews *learning* velocity alongside delivery velocity.

## Staggered Sprints

Discovery runs exactly **one sprint ahead** — while delivery builds features validated in sprint N, discovery validates designs for N+1. Benefits: design is never a bottleneck; the two happen simultaneously; an invalidation doesn't derail the current delivery sprint. Pitfall: getting >1 sprint ahead makes validated designs go stale — keep the gap at one.

## Hypothesis-Driven Stories

Extend the story with *why* and *how we'll know*:

```
As a [user], I want [feature], so that [benefit].
HYPOTHESIS: we believe [outcome] if [persona] achieves [action] with [feature].
SUCCESS METRIC: [metric] changes by [amount] within [timeframe].
EXPERIMENT: how it was validated in discovery.
Acceptance criteria: [technical spec]
```

## Backlog

Columns flow assumptions → hypotheses → testing → validated → (or) invalidated → delivery. Grooming: review invalidated (pivot vs drop), re-prioritize assumptions on new evidence, size *experiments* not features in discovery, and remove zombie items untested for 3 sprints.

## Definition of Done for UX

Expand DoD to include learning — a feature is done when: hypothesis validated against pre-set criteria; design tested with ≥5 users; success metric defined and **instrumented**; code complete/tested/deployed; and a post-launch review is scheduled. Post-launch loop: day 1 verify instrumentation · week 1 compare metric to target · week 2 run 3 follow-up interviews · sprint end report validated/invalidated/inconclusive.

## Avoid Sprint Zero

A weeks-long "design ahead" Sprint Zero is waterfall in disguise (design without engineering input, lost context, designer bottleneck). Instead start discovery and delivery together from day one; the first discovery sprint uses paper prototypes so there's no wait for "finished designs"; engineers join design sessions from the start; staggered sprints maintain flow without a buffer.

## Trust with Engineering

Biggest adoption barrier is design↔engineering trust. Build it by inviting engineers to every Design Studio, sharing experiment results openly (evidence over opinion), pair-designing, prototyping together, and celebrating invalidated hypotheses. Resolve disagreements by framing both options as hypotheses and testing the riskier, using data over authority, and time-boxing the debate.

## Health Metrics

Track whether Lean UX is actually working: hypotheses validated per sprint (2–4), **invalidated per sprint (≥1 — zero signals confirmation bias)**, time from hypothesis to experiment (<1 sprint), backlog items removed via invalidation (≥1/quarter), team members observing research (all, ≥1 session/sprint), post-launch metrics reviewed (100% within 2 weeks).
