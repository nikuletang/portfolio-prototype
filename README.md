# Portfolio case studies: responsive prototypes

Design-review prototypes of case study pages for Niku Letang's UX portfolio, built before the Webflow builds:

| Page | Open | Self-contained copy |
|---|---|---|
| DC Water | `index.html` | `preview.html` |
| Grove Family Health | `grove-family-health.html` | `grove-preview.html` |

Both pages share `css/styles.css` and `js/main.js`. The Grove page is described in [Grove Family Health](#grove-family-health) below.

## DC Water

A design-review prototype of the DC Water UX case study page, built before the final Webflow build. It uses the real case study copy from the UXfolio PDF, with labelled image placeholders and configurable Figma prototype slots.

> This is the review prototype. The Webflow build of the same page (DC Water page, unpublished) is described in [`webflow/README.md`](webflow/README.md).

## Preview

There's no build step and no dependencies. Either:

- **Open `preview.html`** (DC Water) or **`grove-preview.html`** (Grove), single self-contained files with the CSS and JS inlined. They work in viewers that open only one file, such as the Claude app or a downloaded copy. Regenerate both with `node scripts/build-preview.js` after editing the source files. Images in `assets/images/` aren't inlined, so these copies show placeholders.
- **Open `index.html`** or **`grove-family-health.html`** in a browser from a full copy of the repo. It needs the `css/` and `js/` folders next to it, or
- **Run a local server** (recommended, so embeds behave like production):

  ```sh
  python3 -m http.server 8000
  # then open http://localhost:8000 (DC Water)
  # or http://localhost:8000/grove-family-health.html
  ```

To review responsive layouts, use your browser's device toolbar at about 1440 px (desktop), 820 px (tablet) and 375 px (mobile).

## Files

```
index.html            DC Water: page structure and all case study copy
css/styles.css        Shared design tokens (top of file) and layout
js/config.js          DC Water: back-to-projects URL and Figma prototype URLs
js/assets.js          DC Water: image manifest (file name, label and alt text per slot)
js/main.js            Shared: placeholder → image swap, Figma embeds, section nav,
                      drafts toggle, enlarge dialog, config links
assets/images/        Drop exported images here (Grove images in assets/images/grove/)
docs/ASSETS.md        DC Water: every image needed, with file names (generated)
docs/REVIEW-NOTES.md  DC Water: factual questions to confirm

grove-family-health.html  Grove: page structure and all case study copy
css/grove.css             Grove: browser frame, drafts, enlarge dialog, page layouts
js/grove-config.js        Grove: back-to-projects URL, live site URL, drafts default
js/grove-assets.js        Grove: image manifest
docs/GROVE-ASSETS.md      Grove: every image needed (generated)
docs/GROVE-NOTES.md       Grove: questions, drafting placeholders, draft-only sections

scripts/list-assets.js    Regenerates docs/ASSETS.md and docs/GROVE-ASSETS.md
scripts/build-preview.js  Regenerates preview.html and grove-preview.html
```

## Updating content

| To change… | Edit |
|---|---|
| Copy | `index.html`. Each section is commented (`1. HERO` … `9. CLOSING`). |
| An image | Save it as `assets/images/<file>` using the name in `docs/ASSETS.md`. It replaces the placeholder automatically on reload. To use another name or format, change `file` in `js/assets.js`. |
| Alt text | `alt` for that slot in `js/assets.js`. |
| Figma prototype links | `js/config.js` → `figma.<flow>.url`. Once set, "Open prototype in Figma" becomes a live link and a "Load interactive prototype" button appears. Set `embed: false` to keep only the link. |
| Back to projects | `js/config.js` → `backToProjectsUrl` |
| Mockup style | `js/config.js` → `mockupFrame` (`"detailed"` phone or `"simple"` frame). Reviewers can also switch with the **Mockups: Phone / Simple** toggle in the top bar. |
| Fonts | `--font-sans` / `--font-display` at the top of `css/styles.css` |
| Colors | The tokens at the top of `css/styles.css`. Teal `#0f6e68` is 6.1:1 on white. |

Export interface screens **without device frames**. The page draws every phone itself, as either a detailed phone or a simple frame, so the original interface colors stay intact. The sketch stays unframed.

After adding images, run `node scripts/list-assets.js` to refresh the status column in `docs/ASSETS.md`.

## Page structure

1. Hero
2. Project overview: problem, role vs. team, facts, sprint timeline
3. Solution preview: report, receive updates, track
4. Understanding the problem: Sprint 1–2 findings, image card sort, word bank, findings, IA
5. Designing and refining the reporting experience: iteration 1, testing, learned → changed → tested decisions, Customer Service form
6. Exploring photo-based reporting (concept): brief, lightning demos, sketching, wireframes, iteration 1, A/B testing, iteration 2
7. Final experience and prototypes: three flows with Figma slots and complete screen galleries
8. Outcomes, limitations, and reflection: designed / tested / delivered / concept, with reflections in a page-turning notebook
9. Back to projects

## Grove Family Health

`grove-family-health.html` adapts the Grove Family Health business case study into a portfolio case study. It follows the DC Water page's visual hierarchy and components (hero band, numbered section heads, section nav, challenge → response chains, dark showcase band), organized around Grove's own process: sitemap, visual direction, wireframes, high-fidelity design, launch.

**Page structure:** hero · 01 overview · 02 solution preview · 03 understanding the challenge · 04 site architecture · 05 visual direction · 06 wireframes · 07 key design decisions · feedback and refinement *(draft only)* · 08 final website · 09 outcomes · reflection *(draft only)* · closing.

| To change… | Edit |
|---|---|
| Copy | `grove-family-health.html`. Each section is commented. |
| An image | Save it in `assets/images/grove/` with the name in `docs/GROVE-ASSETS.md`, then reload. Alt text and labels are in `js/grove-assets.js`. |
| Back to projects / live site link | `js/grove-config.js` → `backToProjectsUrl`, `liveSiteUrl` (empty hides the button) |
| Draft visibility | `js/grove-config.js` → `showDrafts`. Reviewers can also use **Drafts: Show / Hide** in the top bar. |

**Screenshots and frames.** Every website screenshot sits in a drawn browser window. Export screenshots without a frame, in Grove's original colors. Images keep their own proportions: a tall full-page screenshot scrolls inside its frame rather than being cropped or squeezed, and **Enlarge** opens it at full width in a dialog (Esc or Close returns focus to the button).

**Drafts.** Amber boxes marked "Drafting placeholder" or "Question for Niku" are review-only. Any element with `data-draft` disappears in the reader view. The Feedback and Reflection sections are entirely `data-draft`, so readers don't see them until they're written. See `docs/GROVE-NOTES.md`.

## Webflow build

The page is built on the Webflow **DC Water** page with `dcw-` classes. See [`webflow/README.md`](webflow/README.md) for how it was generated, how to switch the phone mockup style (the `is-simple-phones` combo class), and what's left to fill in.
