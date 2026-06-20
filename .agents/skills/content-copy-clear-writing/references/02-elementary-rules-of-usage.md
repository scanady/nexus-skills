# II. Elementary Rules of Usage

Seven grammar and punctuation rules most often broken.

---

### Rule 1. Form the possessive singular by adding 's.

Add 's regardless of the final consonant.

| Correct | Incorrect |
|---------|-----------|
| the user's token | the user' token |
| the class's method | the class' method |
| the regex's pattern | the regex' pattern |

**Exceptions:** ancient proper names ending in *-es* or *-is* (Jesus', Moses'). Pronouns (its, hers, theirs) take no apostrophe.

---

### Rule 2. In a series of three or more terms with a single conjunction, use a comma after each term except the last.

> read, parse, and validate  
> add, commit, or revert  
> He opened the file, read the contents, and closed the stream.

Use the serial comma. Omit only in business entity names where convention differs.

---

### Rule 3. Enclose parenthetic expressions between commas.

A parenthetic expression interrupts the flow. Set it off on both sides — never just one.

> The function, which handles authentication, was refactored last sprint.  
> This approach, however, introduces a race condition.

**Always parenthetic** (always take commas):
- The year when part of a full date: `April 6, 1917`
- Abbreviations *etc.* and *jr.*
- Non-restrictive relative clauses (clauses that add information without identifying which one)

**Restrictive clause — no commas** (the clause identifies which one):
> The endpoint that handles login requires authentication.  
> *(Remove this clause and the sentence changes meaning — so no commas.)*

---

### Rule 4. Place a comma before a conjunction introducing a co-ordinate clause.

> The build passed, but the deployment failed.  
> She reviewed the PR, and the changes were merged the next morning.

When the subject is shared and not repeated, omit the comma with *and* if the clauses are closely related:
> He cloned the repo and ran the tests.

---

### Rule 5. Do not join independent clauses with a comma alone.

Two complete sentences joined only by a comma is a comma splice — a common error.

| Comma splice (wrong) | Correct |
|----------------------|---------|
| The server restarted, the connection dropped. | The server restarted; the connection dropped. |
| The test passed, it was merged. | The test passed. It was merged. |

Use a semicolon, a period, or add a conjunction.

---

### Rule 6. Do not break sentences in two without cause.

Don't use a period where a comma or no punctuation belongs:

> Wrong: "He ran the migration. Without checking the rollback plan."  
> Right: "He ran the migration without checking the rollback plan."

A fragment can be intentional for emphasis, but use it deliberately and rarely.

---

### Rule 7. A participial phrase at the beginning of a sentence must refer to the grammatical subject.

The opening phrase modifies the subject. If the subject can't logically perform the opening action, the sentence is a dangling modifier.

| Dangling (wrong) | Fixed |
|------------------|-------|
| Parsing the request, an error was thrown. | Parsing the request, the handler threw an error. |
| Having reviewed the logs, the issue became clear. | Having reviewed the logs, I understood the issue. |
