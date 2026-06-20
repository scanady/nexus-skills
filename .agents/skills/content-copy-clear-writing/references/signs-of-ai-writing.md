# AI Writing Patterns: Quick Reference

LLMs regress to statistical means — replacing specific facts with generic, important-sounding language. This guide catalogs the most common patterns. Source: Wikipedia editors' field guide for detecting AI-generated submissions (field-tested across thousands of cases).

---

## 1. Puffery and Legacy Claims

LLMs inflate importance by adding statements about how mundane things "represent" or "contribute to" broader topics. Watch for:

**Trigger words:** *stands as a testament to, serves as a reminder, plays a vital/crucial/pivotal role, underscores its importance, reflects broader, symbolizing its enduring/lasting impact, key turning point, indelible mark, deeply rooted, profound heritage, steadfast dedication*

**Pattern:** A factual statement followed by a vague claim about its significance.

> Bad: "The function was refactored in Q3, marking a pivotal moment in the codebase's evolution toward maintainability."  
> Good: "The function was refactored in Q3 to reduce duplication."

**Tell:** These statements apply equally to any subject — they add no specific information.

---

## 2. Superficial Analysis via -ing Phrases

LLMs attach present-participle phrases to signal analysis without doing any. The "-ing" phrase doesn't analyze — it narrates what analysis would sound like.

**Trigger words:** *ensuring reliability, showcasing capabilities, highlighting the importance, underscoring its significance, emphasizing the value, reflecting broader trends, contributing to the ecosystem, aligning with best practices, demonstrating commitment*

**Pattern:** `[fact], [verb]-ing [vague claim].`

> Bad: "The API returns a 404 status code, ensuring a clear developer experience."  
> Good: "The API returns a 404 status code for unknown resources."

**Tell:** The inanimate subject can't actually highlight or underscore anything. It's the writer inserting opinion as fact.

---

## 3. Regression to the Generic

LLMs replace specific, unusual facts with broad, positive descriptions that apply to anything. The result: simultaneously more exaggerated and less specific.

**Signs:**
- Specific details replaced by importance-sounding generalities
- Named facts disappear; vague descriptors multiply
- Hedging preamble acknowledging low importance, followed by importance claims anyway

> Bad: "Though it saw limited use, it contributes to the broader history of early aviation engineering."  
> Good: Either state the specific historical detail, or omit the sentence.

---

## 4. Notability and Media Coverage Claims

LLMs prove importance by listing sources rather than citing what those sources said. Also: the phrase "active social media presence" is a near-certain AI tell.

**Trigger words:** *independent coverage, featured in [outlets], active social media presence, local/regional/national media outlets, widely covered*

> Bad: "The project has been featured in Wired, The New York Times, and Forbes, underscoring its industry impact."  
> Good: Cite what was actually said, or let the work speak for itself.

---

## 5. Word-Level AI Vocabulary

Individual words that appear at high frequency in LLM output and low frequency in strong human writing:

| Avoid | Use instead |
|-------|-------------|
| delve into | examine, explore, look at |
| leverage | use |
| utilize | use |
| multifaceted | complex, varied (or be specific) |
| foster | build, encourage, create |
| realm | area, field, domain |
| tapestry | (cut entirely) |
| synergize | work together |
| facilitate | help, enable, allow |
| robust | strong, reliable (or be specific) |
| seamless | smooth, uninterrupted (or be specific) |
| cutting-edge | current, latest, modern (or be specific) |
| groundbreaking | (be specific about what's new) |

---

## 6. Structure Tells

LLMs overformat. Signs:

- **Excessive headers** — every two sentences gets a bold heading
- **Bullet overload** — information that flows naturally as prose broken into bullets
- **Em-dash and colon overuse** — every clause introduced with a dash or colon
- **Symmetric three-part lists** — advice always comes in exactly three items
- **Bold on random phrases** — bolding that emphasizes everything, thus nothing

Strong human writing uses formatting sparingly. Headers mark genuine section breaks. Bullets appear when items truly lack prose connection.

---

## Quick Test

Before delivering prose, check:

1. Does any sentence claim importance without a specific fact? → Cut or replace with the specific fact.
2. Does any sentence end in an -ing phrase? → Cut the phrase; let the fact stand alone.
3. Does any word appear from the vocabulary list above? → Replace.
4. Is any formatting element present that doesn't aid comprehension? → Remove.
