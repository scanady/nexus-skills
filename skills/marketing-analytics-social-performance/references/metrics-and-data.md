# Metrics and Data

What the numbers in a social export are, what they are not, and which to track. Platform-neutral. Where a platform differs, check its own help pages; definitions change without notice.

## Own data only

Analyze exports you are entitled to: your own account, or a client's with their written consent. Use the platform's export feature (analytics export, or "download your data"). Do not scrape other accounts or profiles. Most platform terms forbid it, and no analysis here needs it.

## Columns the scripts understand

| Role | Recognized names | Note |
|---|---|---|
| Exposure (denominator) | impressions, views, reach, plays, video_views, viewers, exposure | Override with `--exposure-col` |
| Interactions (numerator) | reactions, likes, comments, replies, reposts, shares, retweets, quotes, saves, bookmarks | Clicks are excluded by default; name them in `--interaction-cols` if you want them |
| Date | date, published, published_at, posted_at, created_at, day | ISO `YYYY-MM-DD` or `MM/DD/YYYY` |
| Anything else | any column | Text columns become candidate groups (format, topic, platform); numeric columns can be split at the median |

Add your own descriptive columns before analysis: format, topic, platform, hook type, time slot. Declare them before looking at results; see `statistical-honesty.md`.

## What each number is

| Metric | Reality | Trap |
|---|---|---|
| Impressions / views | Times content was rendered or played. Not unique people | Counting rules differ by platform and change over time. A view on one platform is a 3-second autoplay, on another a 30-second watch |
| Reach | Closer to unique accounts. Better denominator when exposed | Often missing per post |
| Reactions, likes | Cheapest interaction (a tap) | Inflates with audience size and low-effort content |
| Comments, replies | Costly interaction (time, public exposure) | Giveaway prompts make them meaningless |
| Shares, reposts, saves | Strong intent signals; shares extend reach | Defined differently per platform |
| Engagement rate | No standard definition | Default here: `(sum of interactions) / exposure` |
| Followers gained | Moves for reasons unrelated to content quality | A strong niche post can add few; one adjacent hit adds followers who never engage |
| Profile or link clicks | Closer to action | Lagged and weakly attributable per post |

State the engagement-rate definition in every report. Definitions that add clicks, add follows, or divide by followers give numbers 3-5x apart. A benchmark quoted elsewhere is on an unknown denominator.

## Three tiers of metric

| Tier | What | Reliability | How |
|---|---|---|---|
| 1. Outcomes | Inbound conversations, named references to a post, invitations, referrals, qualified enquiries, sales | Highest, tied to the objective | Count by hand in the measurement log (`assets/measurement-log.md`) |
| 2. Behavior proxies | Comment count, comment share (comments / interactions), saves, shares | Medium | From the export |
| 3. Reach | Impressions, engagement rate, followers | Lowest: noisy, redefined | Watch for large shifts monthly; never decide weekly on these |

Tier 1 is what the work is for, and almost nobody records it. Start there.

## Why median and MAD

Post results are heavy-tailed: a few posts far outrun the rest, and one of them drags a mean to a value that describes none of your posts. The scripts report:

- **Median** and **MAD** (median absolute deviation) instead of mean and standard deviation.
- **Quartile bands** (STRONG above Q3, WEAK below Q1).
- **Tukey fences on the log scale**: breakout above `exp(Q3 + 1.5 x IQR)` of the logs, dud below the mirror fence. Working on logs lets the lower fence fire on skewed data; on raw values it usually sits below zero and never triggers.
- **sigma_log** = `1.4826 x MAD` of the log values. This is the spread figure the experiment sizer needs.

## The 10-post floor

Under 10 usable posts the scripts describe and refuse to conclude (profile exits 2, tester exits 3). Variation between two similar posts is routinely larger than any difference eight posts could show, so with eight posts you can "find" almost any pattern you search for.

## Compare like with like

- Same platform, same period. Do not pool platforms unless the platform is itself the candidate group.
- Never compare against someone else's numbers: different denominators, different audience size, and published benchmarks come from vendor samples that opted in.
- Your own history is the only honest baseline. That is a reason to post steadily enough to have one.

## Confidence tags for claims in reports

| Tag | Basis |
|---|---|
| Official | Platform's own documentation |
| Study | Third-party study, method known |
| Folklore | Widely repeated, no source |

Tag every definition or rule of thumb you cite. Do not present folklore as measured.

## Sources

1. Each platform's help pages on analytics definitions and data export.
2. Tukey, J. W. (1977). *Exploratory Data Analysis*. Medians, quartiles, 1.5 x IQR fences.
3. Huber, P. J. and Ronchetti, E. M. (2009). *Robust Statistics*, 2nd ed. MAD and the 1.4826 constant.
4. Taleb, N. N. (2020). *Statistical Consequences of Fat Tails*. Why means mislead under heavy tails.
5. Nielsen, J. (2006). "The 90-9-1 Rule for Participation Inequality." Why interactions are few and skewed relative to reach.
