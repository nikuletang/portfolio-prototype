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
