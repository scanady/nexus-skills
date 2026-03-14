# Behavioural Science Frameworks Reference

Detailed breakdowns of the core frameworks, cognitive biases, and ethical guardrails used by the Nudge Unit skill. Load this file when generating or evaluating candidate nudges.

---

## Dual-Process Theory (Kahneman)

All nudges target one or both cognitive systems. Understanding the distinction is essential for categorising interventions.

| Attribute | System 1 (Automatic) | System 2 (Reflective) |
|-----------|---------------------|----------------------|
| Speed | Fast | Slow |
| Effort | Effortless | Effortful |
| Awareness | Unconscious / low awareness | Conscious / deliberate |
| Control | Involuntary | Voluntary |
| Capacity | High (parallel) | Low (serial) |
| Driven by | Heuristics, associations, emotions | Rules, logic, analysis |
| Error type | Systematic biases | Computational mistakes |
| Nudge style | Defaults, framing, salience, priming, anchoring | Information disclosure, commitment devices, planning prompts, feedback |

**Design implication**: System 1 nudges reshape the environment so the desired behaviour happens with minimal thought. System 2 nudges provide tools, prompts, or structures that help people think better when they are already engaged.

---

## EAST Framework

Developed by the UK Behavioural Insights Team. Use as the primary design heuristic when structuring any nudge.

### Easy

Reduce friction for the desired behaviour. Add friction for the undesired behaviour.

- **Default enrolment**: Set the desired option as the pre-selected default (e.g., auto-enrolment in pension schemes).
- **Simplify processes**: Reduce the number of steps, forms, or clicks required.
- **Pre-fill information**: Auto-populate forms with known data.
- **Channel factors**: Remove tiny obstacles that disproportionately block action (e.g., providing a map to the clinic, not just an appointment).

### Attractive

Make the desired behaviour or its communication attention-grabbing.

- **Personalisation**: Use the person's name or relevant details in communications.
- **Visual salience**: Use colour, size, images, or placement to draw attention.
- **Lottery / variable rewards**: Small, uncertain rewards attract more attention than guaranteed equivalents.
- **Loss framing**: Frame outcomes in terms of what people stand to lose rather than gain.

### Social

Leverage social influence to encourage the desired behaviour.

- **Descriptive norms**: Tell people what most others do ("9 out of 10 of your neighbours pay their tax on time").
- **Injunctive norms**: Tell people what others approve of.
- **Commitment to others**: Public or peer commitments increase follow-through.
- **Reciprocity**: People feel compelled to return favours.
- **Network effects**: Behaviour spreads through social connections.

### Timely

Intervene at the moment when people are most receptive to change.

- **Disruption moments**: Target life transitions (new job, new home, new year) when habits are already disrupted.
- **Immediate consequences**: Make the outcomes of behaviour visible right away rather than delayed.
- **Planning prompts**: Ask people to specify when, where, and how they will act — at the moment of decision.
- **Present-bias exploitation**: Frame benefits as immediate rather than future to counteract temporal discounting.

---

## MINDSPACE Framework

Developed by the UK Cabinet Office and Institute for Government. Use as a checklist of behavioural levers when brainstorming candidate nudges.

### Messenger

We are heavily influenced by who communicates information.

- **Authority**: Messages from doctors, experts, or leaders carry more weight.
- **Similarity**: We trust messengers who are like us (peers, community members).
- **Likeability**: Warm, relatable communicators are more persuasive.
- _Example_: A tax compliance letter signed by a named local official increases payment rates vs. a generic government letter.

### Incentives

Our responses to incentives are shaped by predictable mental shortcuts.

- **Loss aversion**: Losses feel ~2× worse than equivalent gains feel good. Frame incentives as avoiding loss.
- **Reference points**: People evaluate outcomes relative to their current position, not in absolute terms.
- **Overweighting small probabilities**: A tiny chance of a large reward (lottery) motivates more than a guaranteed small reward.
- _Note_: To remain a nudge, the incentive must be trivial in economic terms. Significant incentives are economic interventions, not nudges.

### Norms

We are strongly influenced by what others do.

- **Descriptive norms**: "Most people in your area do X" — powerful motivator for compliance.
- **Dynamic norms**: "More and more people are starting to do X" — effective even when current behaviour is minority.
- **Injunctive norms**: "People approve of X" — signals social acceptability.
- _Example_: Hotel towel reuse signs citing "75% of guests in this room reused their towels" outperform generic environmental appeals.

### Defaults

We tend to stick with the pre-set option.

- **Status quo bias**: Changing from the default requires effort and feels risky.
- **Opt-out > opt-in**: Auto-enrolment with opt-out achieves dramatically higher participation than opt-in.
- **Smart defaults**: Set the default to the option that benefits most people.
- _Example_: Auto-enrolment in employer pension schemes (UK) increased participation from ~50% to over 90%.

### Salience

Our attention is drawn to what is novel, personally relevant, or emotionally striking.

- **Simplification**: In complex environments, make the key information stand out.
- **Personalisation**: Personal relevance ("Your energy usage is...") increases engagement.
- **Anchoring**: The first number people see disproportionately influences their estimate.
- _Example_: Simplified energy bills with a neighbourhood comparison and colour-coded usage drive conservation behaviour.

### Priming

Our behaviour is influenced by subconscious cues in the environment.

- **Semantic priming**: Exposure to words or concepts influences subsequent behaviour (e.g., words related to ageing slow walking speed).
- **Environmental cues**: Physical environment elements — smells, sounds, images — shape behaviour without awareness.
- **Goal priming**: Subtle cues that activate a goal (e.g., an image of eyes near an honesty box increases contributions).
- _Example_: Placing fruit at eye level in a cafeteria increases fruit selection without removing unhealthy options.

### Affect

Our emotional state powerfully shapes our decisions.

- **Mood congruence**: People in good moods are more generous, optimistic, and open to change.
- **Emotional framing**: The same information feels different depending on emotional framing (fear vs. hope).
- **Affect heuristic**: We substitute "how do I feel about it?" for "what do I think about it?" when making complex decisions.
- _Example_: Graphic health warnings on cigarette packets leverage disgust/fear to reduce smoking appeal.

### Commitments

We seek to be consistent with our public promises and past actions.

- **Public commitments**: Writing down or publicly stating a goal increases follow-through.
- **Implementation intentions**: "If [situation], then I will [action]" plans double or triple action rates.
- **Escalation**: Start with a small ask, then build — people who agree to a small request are more likely to agree to a larger one later.
- _Example_: Asking patients to write down their next appointment date/time on a card reduced missed appointments by 18%.

### Ego

We act in ways that make us feel better about ourselves.

- **Self-image**: People behave consistently with their desired identity ("You are the kind of person who...").
- **Positive feedback**: Recognition and praise reinforce desired behaviours.
- **Cognitive dissonance**: When actions conflict with self-image, people adjust behaviour to reduce discomfort.
- _Example_: Labelling voters as "above-average citizens" before an election increases turnout.

---

## Common Cognitive Biases for Nudge Design

Quick reference of biases most frequently leveraged or counteracted in nudge interventions.

| Bias | Description | Nudge application |
|------|------------|-------------------|
| **Status quo bias** | Preference for the current state of affairs | Set beneficial defaults; people rarely switch |
| **Loss aversion** | Losses hurt ~2× more than equivalent gains | Frame messages in terms of what people stand to lose |
| **Anchoring** | Over-reliance on the first piece of information encountered | Set a high-but-reasonable anchor for donations, savings rates, etc. |
| **Social proof** | Tendency to follow what others do | Communicate descriptive norms ("most people do X") |
| **Present bias** | Overvaluing immediate rewards vs. future ones | Make future benefits feel immediate; use commitment devices |
| **Framing effect** | Decisions change based on how options are presented | Same info, different frame — choose the frame that promotes desired behaviour |
| **Default effect** | Tendency to accept the pre-selected option | Auto-enrol with opt-out |
| **Availability heuristic** | Judging likelihood by how easily examples come to mind | Make desired outcomes vivid and memorable |
| **Endowment effect** | Overvaluing what we already possess | Give people a trial or provisional ownership of the desired state |
| **Hyperbolic discounting** | Steep discounting of future rewards | Bring consequences forward in time; use immediate micro-feedback |
| **Optimism bias** | Believing bad outcomes are less likely to happen to us | Personalise risk information to counter "it won't happen to me" |
| **Choice overload** | Too many options leads to decision paralysis or poor choices | Curate and reduce option sets; highlight recommended options |

---

## Ethical Guardrails

### The Transparency Test

> "Would this intervention still be broadly acceptable and effective if the target population knew exactly what was being done and why?"

A nudge that fails this test risks being manipulative rather than helpful.

### Ethical Principles for Nudge Design

1. **Autonomy**: The person retains full freedom to choose any option, including the undesired one. Opt-out must be genuinely easy.
2. **Welfare alignment**: The nudge must serve the nudgee's own interests or clearly stated public welfare goals — not solely the nudger's interests.
3. **Transparency**: The nudge and its rationale should be publicly defensible. Secret manipulation is ethically distinct from transparent choice architecture.
4. **Proportionality**: The strength of the nudge should be proportionate to the importance of the behavioural goal and the risk of harm.
5. **Reversibility**: The person should be able to undo the effects of the nudge easily (e.g., opt back out of auto-enrolment).
6. **Non-discrimination**: Nudges must not disproportionately disadvantage vulnerable groups or exploit cognitive limitations in harmful ways.

### Red Flags — When a Nudge Crosses the Line

- The person would object if they knew about the intervention → **manipulation, not a nudge**
- Opting out is deliberately difficult or obscured → **sludge, not a nudge**
- The nudge primarily benefits the nudger at the nudgee's expense → **exploitation, not a nudge**
- The intervention relies on deception about facts → **misinformation, not a nudge**
