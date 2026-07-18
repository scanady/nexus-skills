# Collaborative Design

Design is a team activity, not a phase or a department. When the whole cross-functional team designs together, handoff waste disappears and shared understanding replaces documentation.

## Design Studio

The signature technique — a timed workshop where the team generates, critiques, and converges on solutions.

| Phase | Time | Activity |
|-------|------|----------|
| Problem statement | 5 min | facilitator frames the hypothesis + constraints |
| Diverge (individual) | 10 min | each person sketches 6–8 ideas (6-up template) |
| Present + critique | 3 min/person | present; team questions and highlights |
| Converge (pairs) | 10 min | pairs combine the best into refined concepts |
| Present + critique #2 | 3 min/pair | evaluate; pick top 2–3 |
| Team converge | 10 min | select elements into one direction to prototype |

Total 60–90 min. Facilitation: enforce time boxes strictly (pressure forces breadth); paper/markers only during sketching (no laptops); everyone sketches (boxes and stick figures are fine); critique the idea, not the person; dot-vote to prioritize; **photograph the whiteboard — that's the documentation**.

**6-up template** — one sheet, six panels, one idea each in 5 minutes; no erasing, move on; star your favorite. Other quick formats: Crazy 8s (8 sketches in 8 min), solution sketch (one refined idea), storyboard (multi-step journey), How-Might-We reframe.

## Cross-Functional Participation

| Role | Brings |
|------|--------|
| Designer | synthesizes input into coherent experiences |
| Developer | feasibility — stops designing the impossible/expensive |
| PM | business context and priorities |
| Data analyst | grounds decisions in usage data |
| QA | edge cases and error states |
| Stakeholder | domain context; buy-in through participation |

Ground rules: no seniority in the room; "yes, and" before "no, but"; the designer *synthesizes*, doesn't dictate; the only valid design criterion in a studio is "does this test our hypothesis?" Counter resistance: "we sketch ideas, not art"; "the team that designs together builds faster"; "the designer synthesizes — you contribute perspective, not pixels."

## Reduce Deliverables

Replace documents nobody reads with the minimum for shared understanding:

| Traditional | Lean UX replacement |
|-------------|---------------------|
| 60-page wireframe deck | whiteboard photo from the studio |
| annotated mockup + spec | Figma prototype with the developer in the room |
| 20-page persona | one-page proto-persona, updated weekly |
| poster journey map | storyboard sketch from a session |
| 30-page usability report | 5-min highlight reel + 3 bullet findings |

"Just enough" test: who needs this? will it be read? what's the minimum artifact that conveys the decision? is it for communication or approval?

## Shared Understanding

The real output — everyone holds the same mental model of *what* is being built, *why*, and *how success is measured*. Build it via co-located sketching, pair designing, whole-team research observation (≥2 sessions/sprint), shared walls, and demos that include "what we learned / what we're testing next." Test it: ask each member independently — what are we building this sprint, why (which hypothesis), how will we know it worked? Divergent answers → realign.

## Living Style Guides

Not static PDFs — running code, jointly owned by design + engineering, evolving as patterns are built and validated, low-ceremony to extend. Code is the source of truth (Figma-only updates drift). Minimal contents: colors, typography, spacing scale, components with states/variants, common patterns (empty/loading/error), voice & tone.

## Remote

All of the above works virtually with adjustments: FigJam/Miro canvas with pre-made sections, cameras on for critique, visible timer, anonymous dot voting, one person capturing decisions. Add ~50% time per phase, use breakout rooms for pairs, set explicit speaking order, share context 24h ahead, push a 3-bullet recap within an hour (the shared wall isn't passive when remote).

## Anti-Patterns
- HiPPO dominance → anonymous voting, hypothesis-based critique
- Design by committee → designer synthesizes; critique informs, doesn't dictate
- Sketch theater → time pressure, praise quantity
- No follow-through → assign action items, track in backlog
- Excluding developers → they attend every studio; pair weekly
