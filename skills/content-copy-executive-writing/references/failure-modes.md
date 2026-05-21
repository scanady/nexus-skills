# Failure Modes

The twelve failure mode categories used in the annotated change log. Each entry includes what the failure looks like, why it fails, a before/after example, and a rewrite heuristic. Categories are listed in rough order of impact: structural failures first (which cannot be fixed at the sentence level), then sentence-level failures.

## 1. Buried Lede

**What it looks like:** The recommendation, ask, headline finding, or conclusion appears in the final paragraph (or worse, in the final sentence). The reader has to mine for the answer.

**Why it fails:** Executive readers form a posture in the first few sentences. If they cannot find the point, they read defensively or stop reading. Burying the lede also forces them to re-read once they find it, mapping the context back onto the conclusion, which doubles their cognitive load.

**Before:**
> Over the past six months, we have evaluated three platforms in the customer data space. The evaluation included a technical assessment, a cost model, and reference calls with current users at companies of similar scale to ours. Each platform has strengths and weaknesses, which I will summarize below. After much consideration and based on the criteria established by the leadership team, we believe that Platform A is the best fit for our needs.

**After:**
> I am recommending Platform A for customer data. We evaluated three platforms against the criteria the leadership team set; the analysis is below.

**Heuristic:** Find the sentence that the reader would highlight if you handed them a printout and asked them to find the conclusion. Move that sentence to the first paragraph. Often the first half of the original document was throat-clearing and can be cut entirely.

## 2. Wrong Pattern for Objective

**What it looks like:** The structural choices serve a different objective than the one the communication needs to advance. A decision request structured as a status update. A change announcement structured as a technical explanation. A reassurance written as a defense of the team's competence.

**Why it fails:** Sentence-level polish cannot fix this. The reader gets to the end and does not know what to do, because the structure did not prepare them to act.

**Before structure:** A document titled "Cloud migration update" that contains a chronological narrative of the migration work, but the actual purpose is to ask the CFO to approve an additional $400K to handle a scope expansion.

**After structure:** Recast as a decision request. Recommendation in the first paragraph. Problem (scope expansion) in the second. Alternatives (deferring scope, reducing scope, reallocating from elsewhere) in the third. Risks of each in the fourth. Specific ask with date in the last.

**Heuristic:** If the rewrite requires moving more than two sections, the pattern was wrong. Note this prominently in the structural moves section of the change log so the author learns to diagnose the objective up front.

## 3. Jargon or Acronym Overload

**What it looks like:** Terms, acronyms, or technical vocabulary that the audience does not share. Often combined with unspoken assumptions about what concepts the reader already holds.

**Why it fails:** The reader either stops to decode or skims past, in which case the meaning of the surrounding prose is lost. Executives will rarely admit they did not follow a passage; they will simply discount the whole message.

**Before:**
> We are deprecating the v2 PAS adapter and migrating to a Kafka-fronted CDC pipeline with downstream materialization into the warehouse, which will reduce P95 ingest latency by 60% and simplify the FDM transformations.

**After:**
> We are replacing the current data pipeline for policy administration with a more efficient one. The new pipeline gets data into the warehouse three times faster and removes a class of errors we have been managing manually.

**Heuristic:** Ask whether the audience can act on or judge the statement without knowing the term. If not, replace or define. Specific technical detail can sit in an appendix or in supporting material; the body of the communication carries the meaning, not the mechanism.

## 4. Implementation Detail Crowding Out Implication

**What it looks like:** Paragraphs about how something works or how it was done, with the implication for the reader either absent or buried at the end.

**Why it fails:** Executives read for implication. Implementation detail is what the team owns; implication is what the executive must act on. A communication that loads up on the former without delivering the latter forces the executive to do the translation work themselves, which they will not do.

**Before:**
> The new identity layer uses a federated trust model with OIDC tokens issued by a central authority and validated at each service boundary. We have implemented JWKS rotation on a 24-hour cycle and added a fallback to legacy token validation during the cutover window. The integration with the existing IAM platform required custom claims mapping for the agent identity domain.

**After:**
> The new identity layer is in production. The work that took eight months is done, and we can now authenticate AI agents the same way we authenticate users, which unblocks the agentic delivery model we have been preparing for. Two technical details to flag for you: the cutover has a fallback in place if anything breaks, and the integration with our existing IAM platform is custom rather than off-the-shelf, which is a known maintenance cost we accepted to ship on time.

**Heuristic:** For each paragraph of implementation detail, ask: what does this mean for the reader's decision or judgment? If you cannot answer in one sentence, the paragraph does not belong in the body. Move it to an appendix or cut it.

## 5. Hedge Stack

**What it looks like:** A sentence (or paragraph) loaded with qualifiers that collectively cancel the assertion. "We believe that, based on current data and subject to some assumptions, the recommendation could potentially be considered in the appropriate context."

**Why it fails:** Hedging signals that the author does not believe their own recommendation. Executives read hedges as either lack of conviction or political cover, neither of which earns their backing. A single hedge is often appropriate; a stack of hedges in one sentence is a failure pattern.

**Before:**
> Based on our preliminary analysis, and subject to further validation, we tentatively believe that it may be advisable to consider proceeding with Vendor A, though there are some considerations that would need to be weighed.

**After:**
> We recommend Vendor A. Two considerations we have weighed against this recommendation are below; neither changes our view.

**Heuristic:** Count the qualifiers in each sentence. More than one ("we tentatively believe" plus "may be advisable") and the sentence needs to be rewritten. Single, intentional hedges are fine ("the cost model assumes Q3 pricing, which may shift"). Stacked, defensive hedges should be cut to one or zero.

## 6. Missing Stakes

**What it looks like:** A communication that explains the topic without explaining why the reader should care, why this is urgent, or what changes if they do nothing.

**Why it fails:** Executives triage by stakes. A message without stakes goes to the bottom of the queue. Stakes do not have to be dramatic; they have to be honest and specific.

**Before:**
> The platform consolidation initiative has been progressing. We have completed the initial assessment phase and identified key stakeholders. Next steps include vendor evaluation and technical design.

**After:**
> The platform consolidation is on its critical path for the FY26 cost-out commitment. If we do not reach a vendor decision by January, we lose the deployment window and slip the savings to FY27. We have completed the initial assessment and identified key stakeholders; vendor evaluation and technical design are next.

**Heuristic:** Add a "why now" or "what changes if we wait" sentence to any communication that does not have one. If you cannot honestly write that sentence, the communication may be premature.

## 7. Capability Narration Instead of Outcome

**What it looks like:** Listing what the team built, delivered, or worked on, without naming what changed in the business as a result. The "what we did" without the "what is now different."

**Why it fails:** Executives do not care what the team built. They care what the business can now do, or do better. Capability narration without outcome reads as activity reporting, which is the lowest-credibility form of executive communication.

**Before:**
> The data engineering team delivered the new lakehouse architecture, built three new ingestion pipelines, deployed the metadata catalog, and rolled out the data quality framework to four domains.

**After:**
> The data engineering team finished the foundation we needed to scale analytics across the company. Three things are now possible that were not six months ago: new datasets can be onboarded in two weeks instead of two months, business teams can find the data they need without filing tickets, and we can demonstrate data quality to auditors. The lakehouse, ingestion pipelines, metadata catalog, and quality framework are the components that make those outcomes possible.

**Heuristic:** For every capability statement, follow it with "so that..." or "which means..." until the outcome is named. Then write the outcome first and the capability second.

## 8. Ownership Obscured

**What it looks like:** Passive voice, missing subjects, or vague collective nouns ("the team," "the organization," "we") in places where accountability matters. Common in escalations, status updates, and post-mortems.

**Why it fails:** Executives need to know who owns what. Obscured ownership signals either that the author does not know, or that the author is protecting someone or themselves. Both undermine trust and slow the executive's response.

**Before:**
> The decision regarding the vendor selection has been pending for some time, and progress has been slowed by competing priorities. It is hoped that resolution can be reached in the near term.

**After:**
> The procurement team has held the vendor decision for six weeks because the security review has not closed. I am the owner of the original recommendation and I am asking for your help moving the security review forward; the contact is Jane Doe in the CISO office.

**Heuristic:** Find every passive construction. Ask whether the actor is unknown or hidden. If hidden, name them. If unknown, name that you do not know and what you are doing about it.

## 9. Vendor or Tool Name Without Business Meaning

**What it looks like:** Product names, vendor names, or tool names referenced without explaining what they are or what they do in business terms.

**Why it fails:** Executives cannot evaluate vendor or tool choices without understanding what those choices represent. Mentioning Datadog, Snowflake, Confluent, or LangChain by name to a CFO without translation is the same as speaking a foreign language.

**Before:**
> We are evaluating Confluent Cloud against MSK for the streaming layer, with a likely decision in favor of Confluent given the operational maturity advantage.

**After:**
> For the streaming infrastructure, we have a choice between a fully managed service from a specialist vendor (Confluent) and a managed offering from AWS (MSK). We are leaning toward the specialist because their operational tooling reduces the team we need to staff to run it; the cost premium is roughly $200K a year, which we will recover within eighteen months in headcount cost.

**Heuristic:** On first reference, name what the product does and what category it belongs to. Keep the brand name for traceability, but lead with the function. A reader should be able to follow the argument without recognizing the brand.

## 10. Performative Completeness

**What it looks like:** Long enumerations of everything the team has touched, every workstream, every meeting, every milestone. The sense that the author is demonstrating coverage rather than communicating signal.

**Why it fails:** Comprehensive coverage drowns signal. Executives cannot tell what matters from what is filler. The implicit message is "I have not done the work of figuring out what is important," and the reader will not do that work for the author.

**Before:**
> This month, we completed the access management uplift, finalized the data classification policy, ran the disaster recovery test, conducted the quarterly access review, refreshed the third-party risk inventory, updated the incident response playbook, delivered the security awareness training, completed the OS patching cycle, deployed the new endpoint agents, and progressed on the zero-trust roadmap.

**After:**
> Two items this month matter for you: the disaster recovery test surfaced a gap in our backup region that we are remediating, and the zero-trust roadmap is at a fork that needs your direction. Eight other items shipped on schedule; details below if you want them.

**Heuristic:** Of the items listed, which three would the executive want to know about if they only read three? Lead with those. Demote the rest to an appendix or a "shipped this period" list.

## 11. Generic Abstraction

**What it looks like:** Phrases like "various challenges," "numerous opportunities," "strategic alignment," "key stakeholders," "best practices." Language that fills space without carrying information.

**Why it fails:** Generic abstraction is the linguistic signature of AI slop. It is also a pattern in human writing when the author has not done the work to be specific. Executives recognize it instantly and discount the surrounding content.

**Before:**
> We are facing various challenges in scaling the platform, and we are exploring numerous opportunities to address them through best practices and strategic alignment with key stakeholders.

**After:**
> Three challenges are slowing platform scaling: the storage layer is at 80% capacity, the on-call rotation is at four engineers when it should be six, and the customer onboarding queue has grown from two weeks to six. We are addressing each: a storage expansion is funded and starts in November, two senior engineer hires are in progress for the rotation, and we have a proposal to add an onboarding specialist that I want to discuss with you.

**Heuristic:** When you see a generic abstraction, ask "what specifically?" three times. The third answer is usually concrete enough to use. If it is still abstract, the author may not have the substance and should be flagged.

## 12. Numbers Without Context

**What it looks like:** Metrics, percentages, dollar figures, or counts presented without a comparison, baseline, or target. The number is delivered as if it speaks for itself.

**Why it fails:** A number alone does not tell the reader whether it is good, bad, or neutral. "Latency is 80ms" could be excellent or terrible depending on the system. "We saved $400K" could be remarkable or trivial depending on the budget. Without context, the executive either guesses or discounts.

**Before:**
> System availability was 99.2% this quarter. The team closed 412 tickets. Cost per transaction was $0.018.

**After:**
> System availability was 99.2% this quarter, against our 99.5% SLA. The miss was driven by the October outage; we are still inside the annual SLA window. Ticket closure was 412, up from 380 last quarter, reflecting both higher volume and the new triage process. Cost per transaction was $0.018, down 12% from last quarter and on track for the FY26 target of $0.015.

**Heuristic:** For every number, ask what it should be compared to: target, baseline, prior period, industry benchmark, or threshold. If no comparison is available, ask the author to provide one. If no comparison is appropriate, omit the number; it is not adding signal.

## Annotation Grouping in the Change Log

When producing the annotated change log, group annotations by category, not by location in the document. Lead with the structural moves (which usually map to the first three categories above), then the sentence-level edits. This ordering teaches the pattern: structure first, then craft.

If a single change addresses multiple failure modes (for example, a rewrite that fixes both jargon and missing stakes), annotate it under the primary category and note the secondary improvement in the explanation.

If a failure mode does not appear in the draft, do not invent an instance to fill out the change log. A short, focused log is more useful than a comprehensive one with weak examples.
