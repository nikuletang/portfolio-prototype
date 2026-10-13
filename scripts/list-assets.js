// Regenerates the image checklists from each page's asset manifest and HTML:
//   js/assets.js + index.html                     → docs/ASSETS.md        (DC Water)
//   js/grove-assets.js + grove-family-health.html → docs/GROVE-ASSETS.md  (Grove Family Health)
// Usage: node scripts/list-assets.js
const fs = require("fs");
const path = require("path");
const root = path.join(__dirname, "..");
const imgDir = path.join(root, "assets/images");

const sizeFor = {
  phone: "Mobile screen, ~1170 × 2532 px (any 9:19.5)", board: "Board, 16:10, ≥1600 px wide", sketch: "Photo, 4:5, ≥1200 px tall",
  wide: "16:9, ≥2000 px wide", crop: "9:16",
  tall: "Full-page desktop screenshot, any height, ≥1440 px wide", section: "Page crop, any proportions, ≥1440 px wide",
};

const pages = [
  {
    manifest: "js/assets.js", html: "index.html", out: "docs/ASSETS.md",
    intro: "- **Export screens without device frames.** The page draws its own restrained frame.\n",
    groups: [
      ["Hero", /^hero/], ["Research", /^research/], ["Report a Problem: iteration 1", /^rap-v1/],
      ["Report a Problem: iteration 2", /^rap-v2/], ["Customer Service options board", /^cs-sort/],
      ["Image recognition: sketch", /^ir-sketch/], ["Image recognition: iteration 1", /^ir-v1/],
      ["A/B test screens", /^ab-/], ["Image recognition: iteration 2", /^ir-v2/],
      ["Final: Report a Problem", /^rap-\d/], ["Final: Customer Service", /^cs-\d/], ["Final: Image Recognition", /^ir-\d/],
    ],
  },
  {
    manifest: "js/grove-assets.js", html: "grove-family-health.html", out: "docs/GROVE-ASSETS.md",
    intro: "- **Export screenshots without a browser frame.** The page draws the browser window.\n" +
      "- **Keep each image's own proportions.** Tall full-page screenshots stay tall and scroll inside their frame. Nothing is cropped.\n" +
      "- Keep Grove's original site colors. Each image is used only once on the page.\n",
    groups: [
      ["Hero", /^hero/], ["Solution preview", /^solution/], ["Understanding the challenge", /^original/],
      ["Sitemap and visual direction", /^(sitemap|moodboard|branding)/], ["Wireframes", /^wf-/],
      ["Key decisions: before / after", /^cmp-/], ["Final website gallery", /^final-/],
    ],
  },
];

for (const page of pages) {
  const window = {};
  new Function("window", fs.readFileSync(path.join(root, page.manifest), "utf8"))(window);
  const assets = window.CASE_STUDY_ASSETS;
  const html = fs.readFileSync(path.join(root, page.html), "utf8");

  let out = "";
  let total = 0;
  for (const [title, re] of page.groups) {
    const ids = Object.keys(assets).filter((id) => re.test(id));
    if (!ids.length) continue;
    out += `## ${title}\n\n| File | What it shows | Format | Uses | Status |\n|---|---|---|---|---|\n`;
    for (const id of ids) {
      const a = assets[id];
      const uses = (html.match(new RegExp(`data-asset="${id}"`, "g")) || []).length;
      const have = fs.existsSync(path.join(imgDir, a.file));
      const optional = /optional/i.test(a.label + (a.note || ""));
      out += `| \`${a.file}\` | ${a.label}${optional ? " *(optional)*" : ""} | ${sizeFor[a.kind] || a.kind} | ${uses}${uses > 1 ? " (reused)" : ""} | ${have ? "✅ added" : "needed"} |\n`;
      total++;
    }
    out += "\n";
  }
  const head = `# Image assets needed: ${page.html}\n\n${total} image slots in total.\n\n` +
    "Save each file in `assets/images/` with the exact file name below and reload the page. The placeholder is replaced automatically.\n" +
    `To use a different file name or format, edit the \`file\` value in \`${page.manifest}\`.\n\n` +
    page.intro +
    "- **Optional** rows can stay empty. Remove the slot from the HTML if you have no asset for it.\n" +
    "- Files marked *(reused)* appear in more than one place but only need to be uploaded once.\n\n" +
    "_Regenerate this list with `node scripts/list-assets.js`._\n\n";
  fs.writeFileSync(path.join(root, page.out), head + out);
  console.log("Wrote " + page.out + " with " + total + " assets");
}
