# III. Elementary Principles of Composition

Eleven rules for writing sentences and paragraphs that hold together.

---

### Rule 8. One paragraph per topic.

Each paragraph develops a single idea. Start a new paragraph when the topic shifts — don't run separate ideas into the same block. The first line of each paragraph signals "a new step in the development of the subject has been reached."

In documentation, this means: one concept per section. In commit messages, one change per paragraph. Don't lump.

---

### Rule 9. Begin each paragraph with a topic sentence.

Put the main point first. Every sentence that follows should support, develop, or qualify the opening statement. End the paragraph in line with how it began — don't drift into a digression or close with a minor detail.

> Topic sentence: "The rate limiter uses a sliding window algorithm."  
> Support: Explain the window size, how the count resets, what triggers rejection.  
> Close: Return to what this means for callers.

---

### Rule 10. Use the active voice.

Active voice is direct, specific, and shorter. Passive voice hides who did what and forces the reader to reconstruct causality.

| Passive | Active |
|---------|--------|
| The migration was run by the pipeline. | The pipeline ran the migration. |
| An error was thrown when the token expired. | The handler threw an error when the token expired. |
| A survey of this region was made in 1900. | This region was surveyed in 1900. |

Passive voice is appropriate when the actor is unknown, irrelevant, or when you need the object as the subject for paragraph flow. Use it intentionally, not by default.

**Watch for weak openings:** Replace *there is / there are / it was* with a real subject and verb.

| Weak | Strong |
|------|--------|
| There were three errors in the log. | The log contained three errors. |
| It was decided to roll back the deploy. | The team rolled back the deploy. |

---

### Rule 11. Put statements in positive form.

Assert what is, not what isn't. Negative constructions are vaguer and weaker.

| Negative | Positive |
|----------|----------|
| not important | trivial |
| did not pay attention to | ignored |
| did not have much confidence in | distrusted |
| not often on time | usually late |
| not possible to verify | unverifiable |

Use *not* for genuine denial or contrast — not as evasion. "Not only X but also Y" is strong. "Not very reliable" is weak.

---

### Rule 12. Use definite, specific, concrete language.

Vague generalities don't persuade or inform. Name things. Give numbers. State specifics.

| Vague | Specific |
|-------|----------|
| A period of unfavorable weather set in. | It rained every day for a week. |
| The new feature improves performance. | The new cache layer cut p99 latency from 420ms to 85ms. |
| There were issues with the configuration. | The `timeout` field was missing from `config.yaml`. |
| This approach is more efficient. | This approach runs in O(n) instead of O(n²). |

The more abstract a claim, the less it communicates. Readers form no picture from "robust solution" or "seamless experience." They do form one from "handles up to 10,000 concurrent connections."

---

### Rule 13. Omit needless words.

Every word should carry weight. Cut words that fill space without adding meaning.

**Common offenders:**

| Verbose | Tight |
|---------|-------|
| in order to | to |
| due to the fact that | because |
| at this point in time | now |
| on a daily basis | daily |
| a large number of | many |
| the question as to whether | whether |
| despite the fact that | although |
| it is worth noting that | (just state it) |
| in the event that | if |
| has the ability to | can |

Cut throat the sentence from the front: if the opening clause doesn't add information, cut it. "It is important to note that the cache expires after 60 seconds" → "The cache expires after 60 seconds."

---

### Rule 14. Avoid a succession of loose sentences.

Don't chain sentence after sentence with *and*, *but*, or *so*. After two or three, the rhythm goes slack.

> Loose: "She opened the PR and she added tests and she updated the docs but the reviewer asked for changes and so she revised everything."

Break it up. Subordinate where one action depends on another. Let short sentences stand alone for emphasis.

---

### Rule 15. Express co-ordinate ideas in similar form.

Parallel structure. Items in a list, items joined by *and* or *or*, items compared — give them the same grammatical form.

| Non-parallel | Parallel |
|--------------|----------|
| to parse, validating, and then the output is sent | to parse, to validate, and to send |
| fast, reliable, and it scales well | fast, reliable, and scalable |

---

### Rule 16. Keep related words together.

Subject and verb belong close to each other. Modifiers belong next to what they modify. Long separations between subject and verb force the reader to hold too much in working memory.

| Related words separated | Related words together |
|-------------------------|------------------------|
| The engineer, after reviewing three approaches and consulting two colleagues, decided. | After reviewing three approaches and consulting two colleagues, the engineer decided. |
| I only found three errors. | I found only three errors. |

---

### Rule 17. In summaries, keep to one tense.

Pick past or present and hold it. Don't slip between tenses mid-summary.

> "The refactor removes the global state and reduced the coupling" → "The refactor removes the global state and reduces coupling."

---

### Rule 18. Place the emphatic words of a sentence at the end.

The end of the sentence is the position of emphasis. Bury the important point in the middle and readers glide past it. Put it last.

| Emphasis buried | Emphasis at end |
|-----------------|-----------------|
| Failing silently, which is the worst outcome, is what this code does. | This code fails silently — the worst outcome. |
| This is a security risk, broadly speaking. | Broadly speaking, this is a security risk. |
| The migration, if it fails, will corrupt all user records. | If the migration fails, it will corrupt all user records. |
