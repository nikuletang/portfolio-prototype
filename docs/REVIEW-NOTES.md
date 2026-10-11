# Review notes: questions for Niku

These are things the source PDF (UXfolio export, 11 Oct 2026) doesn't settle. In each case the prototype takes the most conservative reading and doesn't fill the gap with a guess. Please confirm or correct each item.

## A. Facts to confirm

| # | Where on the page | Question | What the prototype does now |
|---|---|---|---|
| A1 | Research → Word bank and image association | The stats **13 participants · ages 18–55 · 8 renters · 5 homeowners** appear in the PDF right after the word bank section. Do they describe the word bank activity only, both activities, or all Sprint 3 research? (The card sort lists 10 participants separately.) | Shows them under the word bank activity. |
| A2 | Reporting → Usability testing (Sprint 3) | How many participants tested iteration 1, and how (moderated, remote, tasks)? What did the **4.6 / 5 confidence score** measure? | Shows the score as written, with no participant count. |
| A3 | Overview → My contributions | Your role lists **user interviews**, but no interviews are described in Sprints 3–5. Should a short interviews section be added, or should the item be removed? | Keeps the item, as in the source. |
| A4 | Photo reporting → A/B test, Landing Option A | The source says the button "would **not** split into 2 separate buttons once clicks." The screen shows split buttons (Fill Form / Image Identifier). Is "not" a typo for "now"? | Describes Option A as splitting into two buttons. |
| A5 | Outcomes → Reflection | The reflection mentions "more engagement with the **Salisbury team**." Is that a carry-over from another case study? What's the correct name? | Uses "the client team". |
| A6 | Hero, Overview, Outcomes | **Project status** is "Development in progress" (2022). What's the current status? Did the Report a Problem and Customer Service forms launch on DC Water's site? Did the developer hand-off (a Sprint 4 goal) happen as planned? | Shows "Development in progress" and calls the hand-off a Sprint 4 *goal*. No production claims. |
| A7 | Photo reporting, Final prototypes | Image recognition is presented as a **concept that wasn't implemented**. Is that correct? Was it handed to DC Water or developers in any form? | Labelled "Concept · prototype only", with simulated recognition. |
| A8 | Reporting → "Categories" decision | The final screens show **Other removed from "Where is the problem?"**, an "If you're unsure, describe your issue here" link, **Other / Not Sure** moved to the problem-type step, and a new **location step**. The source text never describes these changes. When were they made, and what motivated them? | Framed as "What the final screens show", with no rationale added. |
| A9 | Photo reporting → Iteration 2 | The source doesn't say which A/B options were chosen or why. The final prototype uses the **photo layout landing** and the **full-page details**. | Framed as "What the final screens show". |
| A10 | Reporting, Photo reporting | No testing is documented for **Report a Problem iteration 2**, the **Customer Service form**, or **image recognition iteration 2**. Was any done? | Each decision card says "No follow-up test of this change is documented." |
| A11 | Photo reporting | Who made the **sketch** and the **wireframes**? The source says "the team" created the wireframes, but you worked only on image recognition. Should any of this be credited to you specifically? | Credits "the team", as in the source. |
| A12 | Photo reporting → Sketching | Who designed the **chatbot** concept? | Says only that DC Water selected it, and that you worked on image recognition. |
| A13 | Final prototypes → Customer Service | In the final Customer Service screens, the Notifications and Review screens are headed **"Report a Problem"**, not "Customer Service Form". Was that intentional? Do you want to fix it in the exports? | Captions don't mention it. |

## B. Figma prototypes and links

The PDF contains no prototype URLs, so none have been added. To configure them, add these values to `js/config.js`:

| Flow | Config key | Figma file name shown in the PDF embed |
|---|---|---|
| Report a Problem | `figma.reportProblem.url` | "Sprint 3 Prototype" |
| Customer Service Form | `figma.customerService.url` | "Sprint 3 Prototype" (same file) |
| Image Recognition | `figma.imageRecognition.url` | "DC Water – Big Ideas" (rendered blank in the PDF) |
| Back to projects | `backToProjectsUrl` | none in the PDF |

- B1. Both form embeds point to a file named **"Sprint 3 Prototype"**, but the screens include the Sprint 4 changes. Please confirm this is the final file, or share the final link.
- B2. Check that each prototype's sharing setting is "Anyone with the link can view". Otherwise the embed and link won't work for visitors.

## C. Unreadable or uncertain source content

- C1. **Word bank board:** one sticky note is illegible and shown as "[illegible note]". "Infrastructure damage" is a low-confidence reading. A high-resolution board export would settle both.
- C2. **Image recognition Figma embed:** blank in the PDF, so its starting screen is unknown.
- C3. **Card sort board:** the PDF gives the numbers (10 participants, 15 images, 40 categories) but no image. The slot is optional.

## D. Light edits made to source copy (please confirm)

- Fixed typos: "Categorizes created" → "Categories created"; "user resting" → "user testing"; "every important" → "very important"; "up to speak" → "up to speed"; "the only wanted included" → "the only one included"; "with with" → "with".
- "The Homeless population" → "**people experiencing homelessness**" (same meaning, person-first wording).
- Hero line: "Empowering District of Columbia Residents and visitors to Report water-related problems" → "Helping District of Columbia residents and visitors report water-related problems."
- Rewrote long paragraphs as shorter lists and decision cards, with no new facts.
- Added connective labels ("Where it shows up", "What changed") that link findings to design changes only where the PDF shows the link in text or in the screens.
