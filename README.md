# DC Water case study: responsive prototype

A design-review prototype of the DC Water UX case study page, built before the final Webflow build. It uses the real case study copy from the UXfolio PDF, with labelled image placeholders and configurable Figma prototype slots.

> This is a review prototype only. Nothing here touches or publishes to Webflow.

## Preview

There's no build step and no dependencies. Either:

- **Open `preview.html`**, a single self-contained file with the CSS and JS inlined. It works in viewers that open only one file, such as the Claude app or a downloaded copy. Regenerate it with `node scripts/build-preview.js` after editing the source files.
- **Open `index.html`** in a browser from a full copy of the repo. It needs the `css/` and `js/` folders next to it, or
- **Run a local server** (recommended, so embeds behave like production):

  ```sh
  python3 -m http.server 8000
  # then open http://localhost:8000
  ```

To review responsive layouts, use your browser's device toolbar at about 1440 px (desktop), 820 px (tablet) and 375 px (mobile).

## Files

```
index.html            Page structure and all case study copy
css/styles.css        Design tokens (top of file) and layout
js/config.js          Back-to-projects URL and Figma prototype URLs
js/assets.js          Image manifest: file name, label and alt text per image slot
js/main.js            Placeholder → image swap, Figma embeds, section nav
assets/images/        Drop exported images here
docs/ASSETS.md        Every image needed, with file names (generated)
docs/REVIEW-NOTES.md  Factual questions and unreadable source content to confirm
scripts/list-assets.js  Regenerates docs/ASSETS.md
```

## Updating content

| To change… | Edit |
|---|---|
| Copy | `index.html`. Each section is commented (`1. HERO` … `9. CLOSING`). |
| An image | Save it as `assets/images/<file>` using the name in `docs/ASSETS.md`. It replaces the placeholder automatically on reload. To use another name or format, change `file` in `js/assets.js`. |
| Alt text | `alt` for that slot in `js/assets.js`. |
| Figma prototype links | `js/config.js` → `figma.<flow>.url`. Once set, "Open prototype in Figma" becomes a live link and a "Load interactive prototype" button appears. Set `embed: false` to keep only the link. |
| Back to projects | `js/config.js` → `backToProjectsUrl` |
| Fonts | `--font-sans` / `--font-display` at the top of `css/styles.css` |
| Colors | The tokens at the top of `css/styles.css`. Teal `#0f6e68` is 6.1:1 on white. |

Export interface screens **without device frames**. The page applies one consistent, restrained frame (hero, solution preview and prototype posters) and uses frameless screens for comparisons and galleries, so the original interface colors stay intact.

After adding images, run `node scripts/list-assets.js` to refresh the status column in `docs/ASSETS.md`.

## Page structure

1. Hero
2. Project overview: problem, role vs. team, facts, sprint timeline
3. Solution preview: report, receive updates, track
4. Understanding the problem: Sprint 1–2 findings, image card sort, word bank, findings, IA
5. Designing and refining the reporting experience: iteration 1, testing, learned → changed → tested decisions, Customer Service form
6. Exploring photo-based reporting (concept): brief, lightning demos, sketching, wireframes, iteration 1, A/B testing, iteration 2
7. Final experience and prototypes: three flows with Figma slots and complete screen galleries
8. Outcomes, limitations, and reflection: designed / tested / delivered / concept
9. Back to projects

## Notes for the Webflow build

- Each numbered section maps to one Webflow section. Repeating patterns (decision card, before/after compare, screen gallery, flow block) map well to Webflow components.
- The expandable galleries use native `<details>` elements, which you can rebuild as Webflow dropdowns or tabs.
- Accessibility: semantic headings, skip link, visible focus rings, AA-contrast text, `prefers-reduced-motion` respected, and descriptive alt text ready in `js/assets.js`.
