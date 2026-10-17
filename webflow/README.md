# Webflow build

The case study is built on the **DC Water** page of the Niku Letang Portfolio Webflow site. All classes start with `dcw-`, and everything sits inside one `dcw-page` wrapper between the site's nav and footer. Nothing has been published.

## Files

```
build.py              Converts the prototype into Webflow-compatible HTML and CSS, one section at a time
out/                  Generated payloads (re-run `python3 webflow/build.py` to regenerate)
custom-code/head.html   Page head code: Caveat font + notebook page-turn styles
custom-code/footer.html Page footer code: notebook page-turn script
```

Webflow's HTML builder doesn't accept `::before`/`::after` or descendant selectors. The build therefore uses real elements and flat or combo classes, such as `.dcw-mock-island` for the phone's island and `.dcw-h2.is-on-dark`. The image galleries that were expandable in the prototype are horizontal scroll strips.

## Choosing the phone style

The mockup frame is driven by the **DCW Phone frame** variable collection, which has two modes:

| Mode | Look |
|---|---|
| Base (Detailed) | Dark phone body, rim, side buttons and dynamic island |
| Simple | Thin flat frame with a smaller corner radius, no island or buttons |

To switch every mockup on the page, select the `dcw-page` wrapper in the Designer and add the combo class **`is-simple-phones`**. Remove the class to go back to the detailed phone. Visitors never see a toggle.

To fine-tune either look, edit the values in **Variables → DCW Phone frame**: padding, radius, screen radius, island height, button width, body color and rim color.

## Still to do in Webflow

- **Images:** every image uses one of three generic placeholders (phone, board, sketch). The hero uses a labelled one. Replace each one in its Image settings. The alt text is already set, and `docs/ASSETS.md` lists every screen.
- **Figma links:** select each "Open prototype in Figma" button and set its URL. Then delete the note under it.
- **Back to projects:** the link points to `/`. Change it if your projects live on another page.
- **Notebook:** the pages stack in the Designer. The page-turn only runs in preview and on the published site, because it comes from the page's custom code.

---

# Grove Family Health page

The Grove case study is built on the **Grove Family Health** page (`/grove-family-health`, unpublished) from the coded prototype `grove-family-health.html`. Same structure as DC Water: Navigation Bar component → `main.dcw-page` → sections → footer component.

```
build_grove.py          Generates the Grove sections (python3 webflow/build_grove.py)
out/grove-sections.json Generated payloads, one per section
placeholders/           The two placeholder images uploaded to the asset library
```

**Classes.** Shared parts reuse the existing `dcw-` classes (section bands, headings, hero, meta list, challenge → response cards, closing), so restyling those changes both case studies. Grove-only parts use `gfh-` classes: the browser-window frame (`gfh-browser`, `gfh-browser-bar`, `gfh-view`), cards, outcomes, the gallery strip and draft notes.

**Screenshots keep their proportions.** Each screenshot is an image inside `gfh-view`, which has a max height (combo classes `is-hero`, `is-preview`, `is-side`, `is-compare`, `is-gallery`) and scrolls vertically, so a tall full-page screenshot is never cropped or squashed. To change a frame's height, edit that combo class.

## Still to do in Webflow

- **Images (22 slots):** every image uses one of three placeholders (tall screenshot, page section, board). Select each one and replace it in Image settings. The alt text is already set, and `docs/GROVE-ASSETS.md` lists what goes where. Export screenshots without a browser frame; the page draws it.
- **Drafting placeholders:** amber boxes (`gfh-draft`) mark copy that's still needed, including one question in the hero. Replace or delete each one before publishing. `docs/GROVE-NOTES.md` lists them all.
- **Draft-only sections:** *Feedback and refinement* and *Reflection* are on the page but hidden with the combo class `is-draft` (`display: none`), so they're also hidden on the canvas. Select them in the Navigator, write the content, then remove `is-draft` to show them.
- **Live site link:** the "Visit the live website" button points to `https://www.grovefamilyhealth.net` (taken from the business case study). Confirm it.
- **Back to projects:** points to `/`. "Next case study" points to `/dc-water`.
- **Enlarge:** the prototype's enlarge dialog isn't in Webflow. Readers scroll inside each frame instead. If you want click-to-enlarge, wrap an image in a Webflow Lightbox.

---

# Senior Services page

The Senior Services case study is built on the **Senior Services** page (`/senior-services`). It's unpublished and marked as a draft, so a site publish won't include it until you turn draft off in Page settings. It's framed as a University of Maryland HCI course project with proposed designs. It has the same structure as the other case studies: Navigation Bar component → `main.dcw-page` → sections → footer component.

```
build_senior.py           Generates the sections (python3 webflow/build_senior.py)
out/senior-sections.json  Generated payloads, one per section
out/senior-check.html     Standalone preview used to check desktop, tablet and mobile layouts
senior-assets/            The original artifacts cropped from the PDF export, as uploaded to the asset library
```

**Classes.** Shared parts reuse the existing `dcw-` classes (section bands, headings, hero, meta list, role cards, stats, status cards, closing) and two `gfh-` ones (closing links and draft notes). No shared class was restyled. Page-specific parts use `ssv-` classes. The only combos on shared classes are `dcw-meta.ssv-meta` and `dcw-status-grid.ssv-reach`, which apply only where `ssv-` is added.

**Images keep their proportions.** Each image is `ssv-img` at full width with automatic height. The affinity diagram (`ssv-img.is-strip`) and the large diagrams (`ssv-img.is-zoom`, phones only) sit in a keyboard-focusable `ssv-scroll` region that scrolls sideways.

**Enlarging.** Each diagram, sketch and wireframe has an "Open full size ↗" link to the original image (new tab). Webflow's native Lightbox can't be configured through the API used here, because its media list isn't exposed. To use a Lightbox instead, wrap an image in a Lightbox element in the Designer and choose the media there.

## Still to do in Webflow

- **Review questions:** `docs/SENIOR-NOTES.md` lists the facts to confirm (team names, timeline, credits, figures).
- **Reflection:** hidden with `is-draft`. Write it, then remove the class.
- **Publish:** turn off "draft" in the page settings when you're ready.
