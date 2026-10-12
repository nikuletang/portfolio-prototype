// Regenerates docs/ASSETS.md from js/assets.js and index.html.
// Usage: node scripts/list-assets.js
const fs = require("fs");
const path = require("path");
const root = path.join(__dirname, "..");
const window = {};
new Function("window", fs.readFileSync(path.join(root, "js/assets.js"), "utf8"))(window);
const assets = window.CASE_STUDY_ASSETS;
const html = fs.readFileSync(path.join(root, "index.html"), "utf8");
const imgDir = path.join(root, "assets/images");

const groups = [
  ["Hero", /^hero/], ["Research", /^research/], ["Report a Problem: iteration 1", /^rap-v1/],
  ["Report a Problem: iteration 2", /^rap-v2/], ["Customer Service options board", /^cs-sort/],
  ["Image recognition: sketch", /^ir-sketch/], ["Image recognition: iteration 1", /^ir-v1/],
  ["A/B test screens", /^ab-/], ["Image recognition: iteration 2", /^ir-v2/],
  ["Final: Report a Problem", /^rap-\d/], ["Final: Customer Service", /^cs-\d/], ["Final: Image Recognition", /^ir-\d/],
];
const sizeFor = { phone: "Mobile screen, ~1170 × 2532 px (any 9:19.5)", board: "Board, 16:10, ≥1600 px wide", sketch: "Photo, 4:5, ≥1200 px tall", wide: "16:9, ≥2000 px wide", crop: "9:16" };

let out = "# Image assets needed\n\n";
out += "Save each file in `assets/images/` with the exact file name below and reload the page. The placeholder is replaced automatically.\n";
out += "To use a different file name or format, edit the `file` value in `js/assets.js`.\n\n";
out += "- **Export screens without device frames.** The page draws its own restrained frame.\n";
out += "- **Optional** rows can stay empty. Remove the slot from `index.html` if you have no asset for it.\n";
out += "- Files marked *(reused)* appear in more than one place but only need to be uploaded once.\n\n";
out += "_Regenerate this list with `node scripts/list-assets.js`._\n\n";
let total = 0;
for (const [title, re] of groups) {
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
out = out.replace("# Image assets needed\n\n", `# Image assets needed\n\n${total} image slots in total.\n\n`);
fs.writeFileSync(path.join(root, "docs/ASSETS.md"), out);
console.log("Wrote docs/ASSETS.md with", total, "assets");
