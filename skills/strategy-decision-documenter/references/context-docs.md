# Context Docs

Use context docs to preserve project language, not implementation trivia. Goal: future reader knows what domain words mean, which aliases to avoid, and how key concepts relate.

## Discovery

Check docs in this order:
- Root `CONTEXT-MAP.md` means multiple contexts. Use map to choose correct context doc.
- Root `CONTEXT.md` means single context unless code structure clearly says otherwise.
- Context-local `CONTEXT.md` near relevant module wins over root doc for local language.
- No context doc means wait. Create one only after first real term, relationship, or ambiguity resolves.

## `CONTEXT.md` Shape

```md
# <Context Name>

<One or two sentences: what this context owns and why it exists.>

## Language

**<Canonical Term>**:
<One-sentence definition of what it is.>
_Avoid_: <aliases, overloaded words, or misleading terms>

## Relationships

- A **Term** <relationship verb> one or more **Other Terms**

## Example Dialogue

> **Developer:** "<question using canonical terms>"
> **Domain expert:** "<answer that clarifies boundary or relationship>"

## Flagged Ambiguities

- "<ambiguous word>" was used for <meaning A> and <meaning B>; resolved as <canonical split>.
```

## `CONTEXT-MAP.md` Shape

Use only when repo has multiple meaningful contexts.

```md
# Context Map

## Contexts

- [<Context>](./path/CONTEXT.md) - <what it owns>

## Relationships

- **Context A -> Context B**: <how they communicate or depend on each other>
```

## Edit Rules

- Prefer small local edits over full rewrites.
- Define what term is, not lifecycle or implementation behavior.
- Keep definitions to one sentence unless precision would break.
- Record aliases to avoid when they prevent future ambiguity.
- Add relationships when cardinality, ownership, or boundary matters.
- Add example dialogue when it clarifies distinction better than definition.
- Add flagged ambiguity when same word meant multiple things in session.

## Exclusions

Do not add:
- Generic software words: timeout, request, handler, service, repository, adapter
- Low-level class names unless domain expert would say them
- Temporary implementation choices that belong in code or ADR
- Every term mentioned in chat. Capture only vocabulary with future coordination value.

## Multi-Context Choice

When more than one context could own term:
- Ask one ownership question.
- Recommend context with strongest data ownership.
- If term crosses contexts, record it in map relationship, not both glossaries by default.
