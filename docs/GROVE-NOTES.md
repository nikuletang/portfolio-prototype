# Grove Family Health: review notes

Questions and open items for the Grove Family Health case study prototype (`grove-family-health.html`). The source was a screenshot of the business case study on the Stellar Lume Studio site. Where the source doesn't settle something, the page takes the most conservative reading and marks the gap. Drafting placeholders show in amber on the page; switch **Drafts → Hide** in the top bar to see the reader view.

## A. Facts and content to confirm

| # | Where on the page | Question | What the prototype does now |
|---|---|---|---|
| G1 | Hero, Overview | **Role title.** The business case study says "Web Designer & Developer". Keep that, or use a UX/UI title and mention development separately? | Shows "Web designer & developer" (from the source). Hero label reads "Website redesign · UX/UI · January 2026" as briefed. |
| G2 | Overview → Timeline | Project start date and duration. | Drafting placeholder. |
| G3 | Overview → Collaboration | Who else worked on the project (client contacts, other designers or developers)? Were any structural decisions (dedicated service pages, the non-member pathway, simpler navigation) made with or by others? | Placeholder. The page credits you with the sitemap, mood board, branding sheet, wireframes and high-fidelity designs only, and describes the structure as what the sitemap does. |
| G4 | Final website → "Visit the live website" | Is **https://www.grovefamilyhealth.net** the right URL? It's taken from the business case study. | Linked. Set `liveSiteUrl: ""` in `js/grove-config.js` to hide the button. |
| G5 | Solution preview, Wireframes, Final website | The actual **page names** for the patient-focused and employer-focused pages, the wireframed pages, and the gallery pages. | Generic labels ("Patient-focused page", "Page name"). No page names invented. |
| G6 | Understanding the challenge | How were the challenges identified (review of the original site, client conversations, analytics…)? | States that these are project challenges and design observations, not research findings. |
| G7 | Key design decisions | For each comparison, is "Before" the **original site** or the **wireframe**? | Labelled "Before" only, with a drafting note. |
| G8 | Outcomes → 30% | Anything more the client said about the **30% increase in inquiries** (which channels, compared with what period)? | Attributed to Grove Family Health with the 30–45 day timeframe, and states that channels, method and baseline weren't specified. Not attributed to Google Analytics. No calls, emails or conversions are mentioned. |
| G9 | Outcomes → #1 on Google | Anything to add about the ranking? | Shown as a point-in-time observation about three weeks after launch, not a current or guaranteed ranking, and not attributed to the redesign. |
| G10 | Hero, Overview | The source says Grove is "Southern Maryland's **leading** direct primary care practice." | Uses the neutral "a direct primary care practice in Southern Maryland". |
| G11 | Visual direction | The page says the identity was already in place and makes no claim about designing the logo or colors. Did you create any new brand elements (icons, illustration style, photography direction)? | Neutral wording plus caption placeholders. |

## B. Drafting placeholders on the page

Each one is an element with `data-draft`. Delete it once its content is written.

| Section | Placeholder |
|---|---|
| Hero | Role title question (G1) |
| Overview | Timeline, Collaboration |
| Solution preview | Confirm page names and captions |
| Understanding the challenge | How the issues were identified (G6) |
| Site architecture | Sitemap rationale: original vs. new structure, how navigation separates audiences, why pages are grouped as they are |
| Visual direction | Mood board captions (imagery, mood); branding sheet captions (typography, color, interface elements) |
| Wireframes | Rationale for hierarchy, navigation, key information and next steps; confirm which pages were wireframed |
| Key design decisions | Specifics for each design response; "original site or wireframe?" for each Before image |
| Final website | A one-line caption for each gallery page |

## C. Draft-only sections (hidden from readers)

These sections are omitted in the reader view. To publish one, write its content and then remove `data-draft` from the `<section>` **and** from its item in the section nav (Feedback only).

| Section | Needs |
|---|---|
| Feedback and refinement (`#feedback`) | Client feedback received, when it came up, what you changed and why. Optional before/after pair. Give it eyebrow number 08 and renumber Final website (09) and Outcomes (10). |
| Reflection (`#reflection`) | Your reflection. Prompts are on the page. The page-turning notebook from the DC Water page can be reused here. |

## D. Not carried over from the business case study

- The sales closing ("Join our clients…", "Get Started", "Schedule a Free Call") is replaced with **Back to projects** and **Next case study: DC Water**.
- Agency framing ("partnered with Stellar Lume Studio") and "Focus: SEO + UX + Conversion" are dropped.
- The source's headline "Ranked #1 on Google…" is moved from the top of the page to Outcomes, where its timeframe and caveats are visible.
