# Pattern Catalog: Classic AI-Writing Tells

Full before/after for the documented AI-writing tells. The SKILL.md body carries
the compact index and the tier ordering; load this file when you need the worked
example for a specific pattern, or when reviewing long-form prose where several of
these are likely to co-occur.

The "before" examples deliberately contain the tells (including em dashes, curly
quotes, and emojis) so you can see them. Do not copy that style into output.

Many of these are caught mechanically by `scripts/scan.py`. The scanner gives you
line numbers and severity; this file tells you how to fix what it found.

## Group A: Significance and promotion

### 1. Significance / legacy / broader-trend inflation
Tell: arbitrary facts get framed as pivotal moments or part of a broader movement.
Watch: stands/serves as, is a testament/reminder, a vital/crucial/pivotal role, underscores/highlights its importance, reflects broader, symbolizing its enduring, setting the stage for, marking a shift, key turning point, evolving landscape, indelible mark, deeply rooted.

Before:
> The Statistical Institute of Catalonia was officially established in 1989, marking a pivotal moment in the evolution of regional statistics in Spain. This initiative was part of a broader movement across Spain to decentralize administrative functions.

After:
> The Statistical Institute of Catalonia was established in 1989 to collect and publish regional statistics independently from Spain's national office.

### 2. Notability and media-coverage padding
Tell: claims of importance, often a list of outlets with no context.
Watch: independent coverage, local/regional/national media outlets, written by a leading expert, active social media presence.

Before:
> Her views have been cited in The New York Times, BBC, Financial Times, and The Hindu. She maintains an active social media presence with over 500,000 followers.

After:
> In a 2024 New York Times interview, she argued AI regulation should target outcomes, not methods.

### 4. Promotional / advertisement diction
Tell: travel-brochure adjectives, especially on places and culture.
Watch: boasts a, vibrant, rich (figurative), profound, nestled, in the heart of, groundbreaking (figurative), renowned, breathtaking, must-visit, stunning.

Before:
> Nestled within the breathtaking region of Gonder in Ethiopia, Alamata Raya Kobo stands as a vibrant town with a rich cultural heritage and stunning natural beauty.

After:
> Alamata Raya Kobo is a town in the Gonder region of Ethiopia, known for its weekly market and 18th-century church.

## Group B: Fake depth and structure

### 3. Superficial "-ing" tails
Tell: present-participle phrases tacked onto a sentence to imply analysis.
Watch: highlighting, underscoring, emphasizing, ensuring, reflecting, symbolizing, contributing to, fostering, showcasing, encompassing.

Before:
> The temple's palette of blue, green, and gold resonates with the region's natural beauty, symbolizing Texas bluebonnets and the Gulf of Mexico, reflecting the community's deep connection to the land.

After:
> The temple uses blue, green, and gold. The architect chose them to reference local bluebonnets and the Gulf coast.

### 5. Vague attributions / weasel words
Tell: opinions attributed to unnamed authorities.
Watch: industry reports, observers have cited, experts argue, some critics argue, several sources.

Before:
> Experts believe the Haolai River plays a crucial role in the regional ecosystem.

After:
> The Haolai River supports several endemic fish species, per a 2019 survey by the Chinese Academy of Sciences.

Note: do not fabricate a source to replace the vague one. If you do not have it, cut the claim or flag it.

### 6. Formulaic "Challenges and Future Prospects" sections
Tell: a generic challenges paragraph, often bookended by "Despite..."
Watch: Despite its... faces several challenges, Despite these challenges, Challenges and Legacy, Future Outlook.

Before:
> Despite its prosperity, Korattur faces challenges typical of urban areas, including congestion and water scarcity. Despite these challenges, it continues to thrive.

After:
> Congestion rose after 2015 when three IT parks opened. The municipal corporation began a drainage project in 2022 to address recurring floods.

### 10. Forced rule of three
Tell: ideas padded into triples to sound complete.
Before:
> The event features keynotes, panels, and networking. Attendees can expect innovation, inspiration, and insight.

After:
> The event has talks and panels, with time for informal networking between sessions.

### 12. False ranges
Tell: "from X to Y" where X and Y are not on one scale.
Before:
> Our journey takes us from the singularity of the Big Bang to the grand cosmic web, from the birth of stars to the dance of dark matter.

After:
> The book covers the Big Bang, star formation, and current theories about dark matter.

## Group C: Language and grammar

### 7. AI-vocabulary clusters
Tell: post-2023 high-frequency words, often co-occurring.
Watch: additionally, align with, crucial, delve, emphasizing, enduring, enhance, fostering, garner, highlight (verb), interplay, intricate, key (adj), landscape (abstract), pivotal, showcase, tapestry, testament, underscore, valuable, vibrant.

Before:
> An enduring testament to Italian colonial influence is the adoption of pasta in the local culinary landscape, showcasing how these dishes integrated into the traditional diet.

After:
> Pasta, introduced during Italian colonization, remains common, especially in the south.

### 8. Copula avoidance
Tell: elaborate verbs standing in for "is/are".
Watch: serves as, stands as, marks, represents, boasts, features, offers.

Before:
> Gallery 825 serves as LAAA's exhibition space and boasts over 3,000 square feet.

After:
> Gallery 825 is LAAA's exhibition space. It has 3,000 square feet across four rooms.

### 9. Negative parallelism
Tell: "Not just X, it's Y" / "Not only... but..."
Before:
> It's not just about the beat riding under the vocals; it's part of the aggression. It's not merely a song, it's a statement.

After:
> The heavy beat adds to the aggressive tone.

### 11. Elegant variation (synonym cycling)
Tell: the same referent renamed every sentence to dodge repetition.
Before:
> The protagonist faces challenges. The main character must overcome obstacles. The central figure triumphs. The hero returns home.

After:
> The protagonist faces many challenges but eventually triumphs and returns home.

## Group D: Style artifacts (mostly mechanical, caught by the scanner)

### 13. Em-dash overuse
Before:
> The term is promoted by Dutch institutions—not the people themselves—even in official documents.

After:
> The term is promoted by Dutch institutions, not the people themselves, even in official documents.

### 14. Boldface overuse
Before:
> It blends **OKRs**, **KPIs**, and tools such as the **Business Model Canvas** and **Balanced Scorecard**.

After:
> It blends OKRs, KPIs, and tools like the Business Model Canvas and Balanced Scorecard.

### 15. Inline-header vertical lists
Before:
> - **User Experience:** improved with a new interface.
> - **Performance:** enhanced through optimized algorithms.

After:
> The update improves the interface and speeds up load times through optimized algorithms.

### 16. Title Case in headings
Before: `## Strategic Negotiations And Global Partnerships`
After: `## Strategic negotiations and global partnerships`

### 17. Emojis in prose or headings
Before:
> 🚀 **Launch Phase:** product launches in Q3
> 💡 **Key Insight:** users prefer simplicity

After:
> The product launches in Q3. User research showed a preference for simplicity.

### 18. Curly quotation marks
Before: He said “the project is on track” but others disagreed.
After: He said "the project is on track" but others disagreed.

## Group E: Chatbot residue (Tier 1, dead giveaways)

### 19. Collaborative-communication artifacts
Watch: I hope this helps, Of course!, Certainly!, You're absolutely right!, Would you like..., let me know, here is a...

Before:
> Here is an overview of the French Revolution. I hope this helps! Let me know if you'd like me to expand.

After:
> The French Revolution began in 1789, when financial crisis and food shortages fed widespread unrest.

### 20. Knowledge-cutoff / availability disclaimers
Watch: as of [date], up to my last training update, while specific details are limited, based on available information.

Before:
> While specific details about the founding are not extensively documented in readily available sources, it appears to date from the 1990s.

After:
> The company was founded in 1994, per its registration documents.

### 21. Sycophantic / servile tone
Before:
> Great question! You're absolutely right that this is complex. That's an excellent point about the economic factors.

After:
> The economic factors you raised are relevant here.

## Group F: Filler, hedging, padding

### 22. Filler phrases
- "in order to achieve this goal" to "to achieve this"
- "due to the fact that it was raining" to "because it was raining"
- "at this point in time" to "now"
- "in the event that you need help" to "if you need help"
- "has the ability to process" to "can process"
- "it is important to note that the data shows" to "the data shows"

### 23. Excessive hedging
Before:
> It could potentially possibly be argued that the policy might have some effect.

After:
> The policy may affect outcomes.

### 24. Generic positive conclusions
Before:
> The future looks bright. Exciting times lie ahead on the journey toward excellence.

After:
> The company plans to open two more locations next year.

### 25. Transition-word overuse
Tell: nearly every paragraph opens with a formal connective.
Watch: Furthermore, Moreover, Consequently, In addition, Similarly, Likewise, Nevertheless, Notably, Importantly.

Before:
> The team shipped on time. Furthermore, they cut bugs by 40%. Moreover, satisfaction improved. Additionally, the codebase got cleaner.

After:
> The team shipped on time and cut bugs by 40%. Satisfaction went up too, and the codebase ended up cleaner.

### 26. Summary echo
Tell: the question or topic is restated before the answer.
Before:
> When it comes to whether remote work improves productivity, this is indeed a topic that has generated significant discussion.

After:
> The evidence is mixed. A Stanford study found remote workers 13% more productive; a Microsoft study found collaboration declined.
