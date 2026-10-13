"""Generate Webflow-compatible HTML/CSS chunks for the Grove Family Health case study.

Same approach as build.py (DC Water): flat classes, no pseudo-elements, no
descendant selectors. Shared building blocks reuse the `dcw-` classes that
already exist on the site (section bands, heads, hero, meta list, chain cards,
closing), so their CSS is NOT re-sent. Everything Grove-specific uses `gfh-`
classes, and only those rules are included in the payloads.

Content mirrors grove-family-health.html (the coded prototype).

Usage: python3 webflow/build_grove.py   -> writes webflow/out/grove-sections.json
"""
import json, os, re, subprocess, html as H

ASSET = "https://cdn.prod.website-files.com/68caf66283367e4c3b2f3706/"
PH = {
    "tall": ASSET + "6acda12d7304092c01bddd6c_gfh-ph-tall.png",
    "section": ASSET + "6acda12def97e62657156926_gfh-ph-section.png",
    "board": ASSET + "6acc456f3d187e174caf33b7_dcw-ph-board.png",
}
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ASSETS = json.loads(subprocess.check_output(["node", "-e",
    'const w={};new Function("window",require("fs").readFileSync(process.argv[1],"utf8"))(w);'
    'process.stdout.write(JSON.stringify(w.CASE_STUDY_ASSETS))', os.path.join(ROOT, "js/grove-assets.js")]))
e = H.escape

TEAL, TEAL_S, TINT, DEEP = "#0f6e68", "#0a524e", "#e3f2ef", "#062b2a"
INK, INK2, INK3, LINE = "#111111", "#3d3d3d", "#5f5f5f", "#e2e2e2"
SHADOW = "0 1px 2px rgba(6,43,42,0.04), 0 10px 24px -16px rgba(6,43,42,0.25)"
D_INK, D_BG, D_LINE = "#6b4500", "#fff7e6", "#e2b45a"

# ---------------------------------------------------------------- helpers
def img(asset_id, cls="gfh-shot"):
    a = ASSETS[asset_id]
    return (f'<img class="{cls}" src="{PH.get(a["kind"], PH["tall"])}" alt="{e(a["alt"])}" '
            f'data-asset="{e(a["file"])}" loading="lazy">')

def browser(asset_id, size):
    """Browser-window frame. The view scrolls vertically so tall pages keep their proportions."""
    return ('<div class="gfh-browser"><div class="gfh-browser-bar" aria-hidden="true">'
            '<div class="gfh-dots"><div class="gfh-dot is-red"></div><div class="gfh-dot is-amber"></div><div class="gfh-dot is-green"></div></div>'
            '<div class="gfh-url"></div></div>'
            f'<div class="gfh-view is-{size}" tabindex="0" role="region" aria-label="{e(ASSETS[asset_id]["label"])}, scrollable">{img(asset_id)}</div></div>')

def head(num, label, h2, lede=None, dark=False):
    d = " is-on-dark" if dark else ""
    num_html = f'<span class="dcw-eyebrow-num{d}">{num}</span>' if num else ""
    out = (f'<div class="dcw-head"><div class="dcw-eyebrow{d}">{num_html}{label}</div>'
           f'<h2 class="dcw-h2{d}">{h2}</h2><div class="dcw-h2-bar"></div>')
    if lede: out += f'<p class="dcw-lede{d}">{lede}</p>'
    return out + "</div>"

def draft(text, kind="Drafting placeholder", items=None, extra=""):
    li = "".join(f'<li class="gfh-draft-li">{x}</li>' for x in items or [])
    lst = f'<ul class="gfh-draft-list">{li}</ul>' if li else ""
    return (f'<div class="gfh-draft{(" " + extra) if extra else ""}"><div class="gfh-draft-k">{kind}</div>'
            f'<div class="gfh-draft-t">{text}</div>{lst}</div>')

def cap(title=None, text=None, num=None, dark=False):
    d = " is-on-dark" if dark else ""
    out = '<div class="gfh-cap">'
    if num: out += f'<div class="dcw-fig-num is-teal">{num}</div>'
    if title: out += f'<div class="gfh-cap-title{d}">{title}</div>'
    if text: out += f'<p class="gfh-cap-text{d}">{text}</p>'
    return out + "</div>"

def chain3(challenge, response, why, response_draft):
    return ('<div class="dcw-chain">'
            f'<div class="dcw-chain-card"><div class="dcw-chain-k">The challenge</div><p class="dcw-chain-p">{challenge}</p></div>'
            '<div class="dcw-chain-arrow">↓</div>'
            f'<div class="dcw-chain-card is-changed"><div class="dcw-chain-k is-changed">Design response</div><p class="dcw-chain-p is-changed">{response}</p>'
            f'{draft(response_draft, extra="is-in-chain")}</div>'
            '<div class="dcw-chain-arrow">↓</div>'
            f'<div class="dcw-chain-card"><div class="dcw-chain-k">Why it mattered</div><p class="dcw-chain-p">{why}</p>'
            '<div class="gfh-intended">Intended benefit</div></div>'
            '</div>')

def decision(num, title, challenge, response, why, response_draft, before, after):
    def item(label, asset_id, is_after):
        lab = f'<div class="dcw-cmp-label{" is-after" if is_after else ""}">{label}</div>'
        note = "" if is_after else draft("Original site or wireframe? Update the label.", extra="is-sm")
        return f'<div class="gfh-cmp-item">{lab}{browser(asset_id, "compare")}{note}</div>'
    return (f'<div class="gfh-decision"><div class="gfh-decision-text">'
            f'<div class="gfh-theme-num">{num}</div><h3 class="gfh-decision-title">{title}</h3>'
            f'{chain3(challenge, response, why, response_draft)}</div>'
            f'<div class="gfh-cmp">{item("Before", before, False)}{item("After · Final design", after, True)}</div></div>')

# ---------------------------------------------------------------- sections
S = {}

S["hero"] = f'''<header class="dcw-section is-hero" id="top">
<div class="dcw-hero-dots"></div>
<div class="dcw-wrap"><div class="dcw-hero-grid">
<div class="dcw-hero-copy">
<div class="dcw-eyebrow is-on-dark">Website redesign · UX/UI · January 2026</div>
<h1 class="dcw-h1">Grove Family Health</h1>
<p class="dcw-hero-tagline">Making direct primary care easy to understand for patients and employers.</p>
<p class="dcw-p is-on-dark">A website redesign for a direct primary care practice in Southern Maryland. The new site explains a less familiar model of care in plain terms and gives patients and employers the information and next steps that apply to them.</p>
<div class="dcw-hero-actions"><a class="dcw-btn is-hero" href="#final">View the final website ↓</a></div>
<div class="dcw-facts">
<div class="dcw-fact"><div class="dcw-chip is-on-dark"><span class="dcw-chip-dot"></span>My role</div><div class="dcw-fact-v">Web designer &amp; developer</div></div>
<div class="dcw-fact"><div class="dcw-chip is-on-dark"><span class="dcw-chip-dot"></span>Client</div><div class="dcw-fact-v">Grove Family Health</div></div>
<div class="dcw-fact"><div class="dcw-chip is-on-dark"><span class="dcw-chip-dot"></span>Launched</div><div class="dcw-fact-v">January 2026</div></div>
<div class="dcw-fact"><div class="dcw-chip is-on-dark"><span class="dcw-chip-dot"></span>Industry</div><div class="dcw-fact-v">Healthcare</div></div>
</div>
{draft('The business case study lists the role as "Web Designer &amp; Developer". Keep that title here, or use a UX/UI title and mention development separately?', "Question for Niku", extra="is-spaced")}
</div>
<div class="dcw-hero-visual"><div class="dcw-hero-halo"></div><div class="gfh-hero-frame">{browser("hero-mockup", "hero")}</div></div>
</div></div></header>'''

pills = ["Sitemap", "Mood board", "Branding sheet", "Wireframes", "High-fidelity design"]
deliv = [("Sitemap", "A structure for the site that organizes information for patients and employers.", "#architecture", "See the sitemap"),
         ("Mood board", "Visual references for a modern direction within the existing identity.", "#visual-direction", "See the mood board"),
         ("Branding sheet", "How the existing brand carries into the website.", "#visual-direction", "See the branding sheet"),
         ("Wireframes", "Page layouts planning hierarchy, navigation and next steps.", "#wireframes", "See the wireframes"),
         ("High-fidelity design", "The final page designs that launched in January 2026.", "#design", "See the designs")]
S["overview"] = f'''<section class="dcw-section" id="overview"><div class="dcw-wrap">
{head("01", "Project overview", "A modern website for a different kind of primary care")}
<div class="dcw-split">
<div class="gfh-brief">
<div class="gfh-brief-k">The brief</div>
<p class="dcw-statement is-brief">Create a modern website that clearly explains the direct primary care model and serves both patients and employers.</p>
<p class="dcw-p is-flush">Grove Family Health offers a more personal, accessible model of care to individuals and to employers. The practice needed a site that communicated that value and helped each audience understand their options and take the next step.</p>
</div>
<div class="dcw-meta">
<div class="dcw-meta-row"><div class="dcw-meta-k">Client</div><div class="dcw-meta-v">Grove Family Health, a direct primary care practice in Southern Maryland</div></div>
<div class="dcw-meta-row"><div class="dcw-meta-k">My role</div><div class="dcw-meta-v">Web designer &amp; developer</div></div>
<div class="dcw-meta-row"><div class="dcw-meta-k">Scope</div><div class="dcw-pills">{"".join(f'<div class="dcw-chip"><span class="dcw-chip-dot"></span>{p}</div>' for p in pills)}</div></div>
<div class="dcw-meta-row"><div class="dcw-meta-k">Launch</div><div class="dcw-meta-v">January 2026</div></div>
<div class="dcw-meta-row"><div class="dcw-meta-k">Constraint</div><div class="dcw-meta-v">Work within the practice's existing branding</div></div>
<div class="dcw-meta-row"><div class="dcw-meta-k">Timeline</div>{draft("Project start date and duration.", extra="is-sm")}</div>
<div class="dcw-meta-row"><div class="dcw-meta-k">Collaboration</div>{draft("Who I worked with: client contacts, any other designers or developers, and how feedback was shared.", extra="is-sm")}</div>
</div></div>
<div class="dcw-block">
<h3 class="dcw-h3">What I created</h3>
<div class="gfh-deliv">{"".join(f'<div class="gfh-deliv-card"><div class="gfh-deliv-title">{t}</div><p class="gfh-deliv-text">{x}</p><a class="gfh-deliv-link" href="{h}">{l} ↓</a></div>' for t, x, h, l in deliv)}</div>
<div class="gfh-constraint"><div class="gfh-badge">Constraint</div><p class="gfh-constraint-text">Grove Family Health already had an established brand. This project wasn't a rebrand: the mood board and branding sheet developed the website's visual direction within that existing identity.</p></div>
</div>
</div></section>'''

def pv(asset_id, step, title, text):
    return f'<div class="gfh-fig">{browser(asset_id, "preview")}{cap(title, text, step)}</div>'

S["solution"] = f'''<section class="dcw-section is-tint" id="solution"><div class="dcw-wrap">
{head("02", "Solution preview", "One website, two audiences, a clear next step", "The redesigned site gives patients and employers their own path to the information that applies to them, with the next step visible along the way.")}
<div class="gfh-trio">
{pv("solution-home", "01 · Homepage", "A clear starting point", "Introduces direct primary care and points patients and employers toward the information meant for them.")}
{pv("solution-patients", "02 · For patients", "Options and a path to membership", "Services and care options explained clearly, with a step-by-step path for non-members toward enrollment.")}
{pv("solution-employers", "03 · For employers", "Information to evaluate a plan", "What employers need to understand direct primary care as an option for their team, and how to take the next step.")}
</div>
{draft("Confirm the page names for the patient and employer pages and adjust the captions to match the screenshots.", extra="is-spaced")}
</div></section>'''

obs = [("No guided path for each audience", "Patients and employers arrived with different questions, but the site didn't lead either group clearly to the information meant for them.", "give each audience a clear starting point"),
       ("Services were hard to take in quickly", "Services were grouped in a way that made it harder to quickly understand the available options.", "give services their own, focused pages"),
       ("The care model needed explaining", "Direct primary care works differently from the insurance-based care many visitors know, and the site needed to explain it more clearly.", "explain the model in plain, reassuring language"),
       ("No defined journey to a decision", "Both individuals and employers could benefit from a more defined journey toward evaluating plans or enrolling in membership.", "make the next step visible and easy to take")]
S["challenge"] = f'''<section class="dcw-section" id="challenge"><div class="dcw-wrap">
{head("03", "Understanding the challenge", "A practice with strong value that wasn't fully reflected online", "Grove Family Health delivers a more personal, accessible care model for individuals and employers. Their previous website didn't clearly communicate that value, which made it harder for visitors to understand their options or move forward with confidence.")}
<div class="gfh-challenge">
<div class="gfh-challenge-text">
<h3 class="dcw-h3">Where visitors were getting stuck</h3>
<p class="dcw-p">Patients and employers were visiting the site but didn't always have a clear, guided path to the information they needed. These are the project challenges and design observations that shaped the redesign.</p>
<div class="gfh-obs">{"".join(f'<div class="gfh-obs-item"><div class="gfh-obs-n">{i:02d}</div><div class="gfh-obs-body"><h4 class="gfh-obs-title">{t}</h4><p class="gfh-obs-text">{x}</p><div class="gfh-obs-need"><span class="gfh-obs-need-k">The redesign needed to →</span> {n}</div></div></div>' for i, (t, x, n) in enumerate(obs, 1))}</div>
<p class="gfh-note">These observations come from the project brief and the design work. They aren't findings from formal user research.</p>
{draft("How were these issues identified: a review of the original site, conversations with the client, analytics, or something else? Add a sentence on that here if you'd like to.", "Question for Niku")}
</div>
<div class="gfh-challenge-media"><div class="gfh-sticky">{browser("original-site", "side")}{cap("The original website", "Before the redesign.")}</div></div>
</div>
</div></section>'''

S["architecture"] = f'''<section class="dcw-section is-quiet" id="architecture"><div class="dcw-wrap">
{head("04", "Site architecture", "Organizing the site for two audiences", "I created a sitemap to plan how patients and employers would each find the information that applies to them, and how every page would lead to a next step.")}
<div class="gfh-artifact">{img("sitemap", "gfh-board")}{cap("Sitemap", "The structure of the redesigned site.")}</div>
<div class="dcw-block">
<div class="dcw-kicker">What the structure does</div>
<div class="gfh-struct">
<div class="gfh-struct-card"><div class="gfh-struct-title">Dedicated service pages</div><p class="gfh-struct-text">Services are broken into their own pages, to make each option easier to understand and easier to find in search.</p></div>
<div class="gfh-struct-card"><div class="gfh-struct-title">A path for non-members</div><p class="gfh-struct-text">A separate pathway leads people who aren't yet members step by step toward enrollment.</p></div>
<div class="gfh-struct-card"><div class="gfh-struct-title">Simpler navigation</div><p class="gfh-struct-text">Fewer, clearer choices, so the next step feels obvious from anywhere on the site.</p></div>
</div>
{draft("Sitemap rationale, in your words:", items=["How the original structure compared, and what changed.", "How the navigation separates patient and employer content.", "Why pages were grouped the way they are."], extra="is-spaced")}
</div>
</div></section>'''

S["visual"] = f'''<section class="dcw-section" id="visual-direction"><div class="dcw-wrap">
{head("05", "Visual direction", "A modern look within an existing brand", "Grove Family Health's identity was already in place. I used a mood board and a branding sheet to define how that identity would carry into a modern, reassuring website.")}
<div class="gfh-pair">
<div class="gfh-artifact">{img("moodboard", "gfh-board")}{cap("Mood board", "The visual direction for the website.")}
{draft("Captions to write:", items=["<strong>Imagery:</strong> the kind of photography or illustration chosen, and why.", "<strong>Mood:</strong> the feeling the site should convey to patients and employers."], extra="is-spaced")}</div>
<div class="gfh-artifact">{img("branding-sheet", "gfh-board")}{cap("Branding sheet", "How the existing brand applies to the website.")}
{draft("Captions to write:", items=["<strong>Typography:</strong> the typefaces and hierarchy for the site.", "<strong>Color:</strong> how the existing brand colors are used on screen (backgrounds, buttons, accents).", "<strong>Interface elements:</strong> buttons, cards or icons defined on the sheet."], extra="is-spaced")}</div>
</div>
</div></section>'''

focus = [("Hierarchy", "What each audience needs to see first on a page."),
         ("Navigation", "How patients and employers move to the content meant for them."),
         ("Key information", "Where the care model and service details are placed."),
         ("Next steps", "Where calls to action appear along each path.")]
def wf(asset_id, title):
    return f'<div class="gfh-fig"><div class="gfh-wf-frame">{browser(asset_id, "preview")}</div>{cap(title)}</div>'
S["wireframes"] = f'''<section class="dcw-section is-tint" id="wireframes"><div class="dcw-wrap">
{head("06", "Wireframes", "Planning the experience before the visuals", "I wireframed the key pages to settle the hierarchy, navigation, where key information sits and where each next step appears, before moving into visual design.")}
<div class="gfh-focus">{"".join(f'<div class="gfh-focus-card"><div class="gfh-struct-title">{t}</div><p class="gfh-struct-text">{x}</p>{draft("Rationale to add.", extra="is-sm")}</div>' for t, x in focus)}</div>
<div class="dcw-block"><div class="gfh-trio">
{wf("wf-home", "Homepage")}{wf("wf-patients", "Patient-focused page")}{wf("wf-employers", "Employer-focused page")}
</div>
{draft("Confirm which pages were wireframed and rename these captions to match. Add or remove slots as needed.", extra="is-spaced")}
</div>
</div></section>'''

S["design"] = f'''<section class="dcw-section" id="design"><div class="dcw-wrap">
{head("07", "High-fidelity design", "Key design decisions", "In the high-fidelity designs, I brought the structure and visual direction together around three goals. Each decision below shows the challenge, my design response, and why it mattered.")}
<p class="gfh-note is-head">"Why it mattered" describes what each change was intended to do. Measured results are reported separately under Outcomes.</p>
{decision("01", "Helping patients and employers find what's relevant to them",
  "Patients and employers came to the site with different questions, without a clear path to the information meant for them.",
  "Separate paths for patients and employers, supported by simplified navigation.",
  "Each visitor can get to what applies to them with less effort.",
  "Add specifics: how each audience is directed (navigation labels, homepage sections).", "cmp-find-before", "cmp-find-after")}
{decision("02", "Making the care model and service options easier to understand",
  "Services were grouped in a way that made options hard to take in quickly, and the direct primary care model needed a clearer explanation.",
  "Dedicated pages for services, with reassuring, plain-language content about how care works.",
  "Visitors can understand their options before they decide, and each service has its own page, which improves clarity and search visibility.",
  "Add specifics: how the care model is explained (sections, FAQs, comparisons).", "cmp-model-before", "cmp-model-after")}
{decision("03", "Making the next step clear",
  "Visitors who were ready to act didn't have a clearly defined journey toward enrolling in membership or evaluating a plan.",
  "A step-by-step pathway for non-members toward enrollment, and visible calls to action throughout the site.",
  "Every path ends in an obvious next step, so no one is left wondering what to do next.",
  "Add specifics: where the calls to action sit and what they say.", "cmp-next-before", "cmp-next-after")}
</div></section>'''

S["feedback"] = f'''<section class="dcw-section is-draft" id="feedback"><div class="dcw-wrap">
<div class="gfh-draft-banner"><strong>Draft only.</strong> Hidden on the live site until it has content: remove the is-draft class from this section to show it.</div>
{head(None, "Feedback and refinement", "Refining the design with client feedback")}
<div class="dcw-grid-2">
{draft("Client feedback:", items=["What the client asked for or raised during reviews.", "When in the process it came up (wireframes, high-fidelity, pre-launch)."])}
{draft("Revisions:", items=["What I changed in response, and why.", "Optional: a before/after pair. Copy a comparison from Key design decisions."])}
</div>
</div></section>'''

def shot(asset_id, n):
    return (f'<div class="gfh-strip-item">{browser(asset_id, "gallery")}'
            f'<div class="gfh-cap"><div class="gfh-cap-title is-on-dark">Page name</div>'
            f'{draft("One line on what this page does for visitors.", extra="is-sm")}</div></div>')
S["final"] = f'''<section class="dcw-section is-dark" id="final"><div class="dcw-wrap">
{head("08", "Final website", "The launched website", "Selected pages from the website that launched in January 2026. Scroll inside each frame to see the full page.", dark=True)}
<div class="gfh-strip" tabindex="0" role="region" aria-label="Final website pages, scrolls horizontally">{"".join(shot(f"final-{i}", i) for i in range(1, 6))}</div>
<p class="gfh-note is-on-dark">Scroll sideways for more pages.</p>
<div class="gfh-live"><a class="dcw-btn is-hero" href="https://www.grovefamilyhealth.net" target="_blank" rel="noopener">Visit the live website ↗</a></div>
</div></section>'''

S["outcomes"] = f'''<section class="dcw-section is-quiet" id="outcomes"><div class="dcw-wrap">
{head("09", "Outcomes", "After launch", "The website launched in January 2026. Two results were reported in the weeks after launch. They come from different sources and are shown separately.")}
<div class="gfh-outcomes">
<div class="gfh-outcome"><div class="gfh-outcome-type">Client-reported result</div><div class="gfh-outcome-num" aria-hidden="true">30%</div>
<h3 class="gfh-outcome-what">increase in inquiries within the first 30–45 days after launch</h3>
<div class="gfh-outcome-meta">
<div class="gfh-outcome-row"><div class="gfh-outcome-k">Source</div><div class="gfh-outcome-v">Reported by Grove Family Health</div></div>
<div class="gfh-outcome-row"><div class="gfh-outcome-k">Timeframe</div><div class="gfh-outcome-v">First 30–45 days after the January 2026 launch</div></div>
<div class="gfh-outcome-row"><div class="gfh-outcome-k">Note</div><div class="gfh-outcome-v">Inquiry channels, measurement method and baseline weren't specified.</div></div>
</div></div>
<div class="gfh-outcome"><div class="gfh-outcome-type">Search observation</div><div class="gfh-outcome-num" aria-hidden="true">#1</div>
<h3 class="gfh-outcome-what">on Google for "primary care Southern Maryland"</h3>
<div class="gfh-outcome-meta">
<div class="gfh-outcome-row"><div class="gfh-outcome-k">When</div><div class="gfh-outcome-v">Observed about three weeks after the January 2026 launch</div></div>
<div class="gfh-outcome-row"><div class="gfh-outcome-k">Note</div><div class="gfh-outcome-v">A point-in-time observation, not a current or guaranteed ranking. Search rankings depend on many factors and change over time.</div></div>
</div></div>
</div>
</div></section>'''

S["reflection"] = f'''<section class="dcw-section is-draft" id="reflection"><div class="dcw-wrap">
<div class="gfh-draft-banner"><strong>Draft only.</strong> Hidden on the live site until it has content: remove the is-draft class from this section to show it.</div>
{head(None, "Reflection", "What I learned")}
{draft("Prompts to answer:", items=["What was it like designing within an existing brand?", "What did designing for two audiences on one site teach you?", "What would you do differently, or measure next time?"])}
</div></section>'''

S["closing"] = '''<section class="dcw-section is-closing"><div class="dcw-wrap"><div class="dcw-closing">
<div class="gfh-closing-links"><a class="dcw-back" href="/">← Back to projects</a><a class="gfh-next" href="/dc-water">Next case study: DC Water →</a></div>
<div class="dcw-closing-note">Grove Family Health · Website redesign · 2026</div>
</div></div></section>'''

# ---------------------------------------------------------------- CSS (gfh- only)
BASE = f"""
.gfh-browser {{ position: relative; width: 100%; overflow: hidden; border: 1px solid #d9dddc; border-radius: 12px; background-color: #ffffff; box-shadow: 0 1px 2px rgba(0,0,0,0.06), 0 24px 48px -24px rgba(6,43,42,0.35); }}
.gfh-browser-bar {{ display: flex; align-items: center; grid-column-gap: 10px; height: 30px; padding-left: 12px; padding-right: 12px; border-bottom: 1px solid #e0e3e2; background-color: #f1f3f2; }}
.gfh-dots {{ display: flex; flex: none; grid-column-gap: 6px; }}
.gfh-dot {{ width: 9px; height: 9px; border-radius: 50%; background-color: #c9cecd; }}
.gfh-dot.is-red {{ background-color: #f0857a; }}
.gfh-dot.is-amber {{ background-color: #f3c25b; }}
.gfh-dot.is-green {{ background-color: #6dc77b; }}
.gfh-url {{ flex: 1; max-width: 60%; height: 16px; margin-left: auto; margin-right: auto; border: 1px solid #e0e3e2; border-radius: 999px; background-color: #ffffff; }}
.gfh-view {{ position: relative; overflow-x: hidden; overflow-y: auto; background-color: #ffffff; }}
.gfh-view.is-hero {{ max-height: 620px; }}
.gfh-view.is-preview {{ max-height: 440px; }}
.gfh-view.is-side {{ max-height: 620px; }}
.gfh-view.is-compare {{ max-height: 380px; }}
.gfh-view.is-gallery {{ max-height: 520px; }}
.gfh-shot {{ display: block; width: 100%; max-width: 100%; height: auto; }}
.gfh-board {{ display: block; width: 100%; height: auto; border-radius: 8px; }}
.gfh-hero-frame {{ position: relative; z-index: 1; width: 100%; max-width: 440px; }}
.gfh-fig {{ display: flex; flex-direction: column; min-width: 0; }}
.gfh-cap {{ margin-top: 14px; }}
.gfh-cap-title {{ margin-bottom: 3px; color: {INK}; font-size: 15px; font-weight: 600; line-height: 1.35; }}
.gfh-cap-title.is-on-dark {{ color: #ffffff; }}
.gfh-cap-text {{ margin-top: 0; margin-bottom: 0; color: {INK3}; font-size: 14px; line-height: 1.5; }}
.gfh-cap-text.is-on-dark {{ color: rgba(255,255,255,0.72); }}
.gfh-trio {{ display: grid; grid-template-columns: 1fr 1fr 1fr; grid-column-gap: clamp(24px, 4vw, 56px); grid-row-gap: 40px; align-items: start; }}
.gfh-brief {{ padding: clamp(20px, 3vw, 32px); border-radius: 16px; background-image: linear-gradient(160deg, #e3f2ef, #d2ebe5); }}
.gfh-brief-k {{ margin-bottom: 10px; color: {TEAL_S}; font-size: 13px; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; }}
.dcw-statement.is-brief {{ font-size: clamp(19px, 1.9vw, 23px); }}
.dcw-p.is-flush {{ margin-bottom: 0; }}
.gfh-deliv {{ display: grid; grid-template-columns: repeat(5, 1fr); grid-column-gap: 12px; grid-row-gap: 12px; }}
.gfh-deliv-card {{ display: flex; flex-direction: column; padding: 18px 18px 16px; border: 1px solid {LINE}; border-radius: 14px; background-color: #ffffff; box-shadow: {SHADOW}; }}
.gfh-deliv-title {{ margin-bottom: 6px; color: {INK}; font-size: 16px; font-weight: 600; }}
.gfh-deliv-text {{ margin-top: 0; margin-bottom: 0; color: {INK2}; font-size: 15px; line-height: 1.45; }}
.gfh-deliv-link {{ margin-top: auto; padding-top: 12px; color: {TEAL}; font-size: 13px; font-weight: 600; text-decoration: none; }}
.gfh-constraint {{ display: flex; align-items: flex-start; grid-column-gap: 14px; max-width: 760px; margin-top: 32px; padding: 16px 18px; border: 1px solid {LINE}; border-left: 4px solid {TEAL}; border-radius: 10px; background-color: #ffffff; }}
.gfh-badge {{ flex: none; margin-top: 2px; padding: 3px 8px; border: 1px solid {TEAL_S}; border-radius: 999px; color: {TEAL_S}; font-size: 11px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; }}
.gfh-constraint-text {{ margin-top: 0; margin-bottom: 0; color: {INK2}; font-size: 15px; line-height: 1.6; }}
.gfh-challenge {{ display: grid; grid-template-columns: 7fr 5fr; grid-column-gap: clamp(28px, 5vw, 72px); grid-row-gap: 40px; align-items: start; }}
.gfh-challenge-media {{ height: 100%; }}
.gfh-sticky {{ position: sticky; top: 96px; }}
.gfh-obs {{ border-top: 1px solid {LINE}; }}
.gfh-obs-item {{ display: grid; grid-template-columns: 48px 1fr; padding-top: 20px; padding-bottom: 20px; border-bottom: 1px solid {LINE}; }}
.gfh-obs-n {{ padding-top: 2px; color: {TEAL}; font-family: Inconsolata, monospace; font-size: 14px; font-weight: 700; }}
.gfh-obs-title {{ margin-top: 0; margin-bottom: 5px; color: {INK}; font-size: 17px; font-weight: 600; line-height: 1.35; }}
.gfh-obs-text {{ margin-top: 0; margin-bottom: 0; color: {INK2}; font-size: 15.5px; line-height: 1.55; }}
.gfh-obs-need {{ margin-top: 9px; color: {TEAL_S}; font-size: 14px; font-weight: 600; }}
.gfh-obs-need-k {{ color: {INK3}; font-weight: 400; }}
.gfh-note {{ margin-top: 16px; margin-bottom: 0; color: {INK3}; font-size: 14px; line-height: 1.5; }}
.gfh-note.is-head {{ max-width: 760px; margin-top: -24px; margin-bottom: 40px; }}
.gfh-note.is-on-dark {{ color: rgba(255,255,255,0.72); }}
.gfh-artifact {{ padding: clamp(14px, 2.5vw, 28px); border: 1px solid {LINE}; border-radius: 16px; background-color: #ffffff; }}
.gfh-struct {{ display: grid; grid-template-columns: 1fr 1fr 1fr; grid-column-gap: 14px; grid-row-gap: 14px; }}
.gfh-struct-card {{ padding: 18px 20px; border: 1px solid {LINE}; border-top: 4px solid {TEAL}; border-radius: 14px; background-color: #ffffff; }}
.gfh-struct-title {{ margin-bottom: 5px; color: {INK}; font-size: 16px; font-weight: 600; }}
.gfh-struct-text {{ margin-top: 0; margin-bottom: 0; color: {INK2}; font-size: 15px; line-height: 1.55; }}
.gfh-pair {{ display: grid; grid-template-columns: 1fr 1fr; grid-column-gap: clamp(24px, 4vw, 48px); grid-row-gap: 32px; align-items: start; }}
.gfh-focus {{ display: grid; grid-template-columns: repeat(4, 1fr); grid-column-gap: 12px; grid-row-gap: 12px; }}
.gfh-focus-card {{ padding: 16px 18px; border: 1px solid {LINE}; border-radius: 12px; background-color: #ffffff; }}
.gfh-wf-frame {{ padding: 12px; border: 1px solid {LINE}; border-radius: 14px; background-color: #ffffff; }}
.gfh-decision {{ display: grid; grid-template-columns: 5fr 7fr; grid-column-gap: clamp(28px, 5vw, 72px); grid-row-gap: 28px; margin-bottom: clamp(40px, 5vw, 64px); padding-bottom: clamp(40px, 5vw, 64px); border-bottom: 1px solid {LINE}; }}
.gfh-theme-num {{ margin-bottom: 6px; color: {TEAL}; font-family: Inconsolata, monospace; font-size: 13px; font-weight: 700; }}
.gfh-decision-title {{ margin-top: 0; margin-bottom: 18px; color: {INK}; font-size: 20px; font-weight: 600; line-height: 1.3; }}
.gfh-intended {{ display: inline-block; margin-top: 10px; padding: 1px 8px; border: 1px dashed #c9c9c9; border-radius: 999px; color: {INK3}; font-size: 12px; font-weight: 600; }}
.gfh-cmp {{ display: grid; grid-template-columns: 1fr 1fr; grid-column-gap: clamp(16px, 3vw, 32px); grid-row-gap: 24px; align-items: start; }}
.gfh-cmp-item {{ display: flex; flex-direction: column; align-items: flex-start; min-width: 0; }}
.gfh-strip {{ position: relative; display: grid; grid-auto-flow: column; grid-auto-columns: clamp(250px, 28vw, 340px); grid-column-gap: clamp(16px, 2.5vw, 28px); padding-top: 4px; padding-bottom: 18px; overflow-x: auto; overflow-y: hidden; scroll-snap-type: x mandatory; }}
.gfh-strip-item {{ min-width: 0; scroll-snap-align: start; }}
.gfh-live {{ margin-top: 28px; }}
.gfh-outcomes {{ display: grid; grid-template-columns: 1fr 1fr; grid-column-gap: clamp(16px, 3vw, 32px); grid-row-gap: 16px; }}
.gfh-outcome {{ display: flex; flex-direction: column; align-items: flex-start; padding: clamp(22px, 3vw, 36px); border: 1px solid {LINE}; border-top: 4px solid {TEAL}; border-radius: 18px; background-color: #ffffff; box-shadow: {SHADOW}; }}
.gfh-outcome-type {{ margin-bottom: 14px; padding: 3px 9px; border-radius: 999px; background-color: {TINT}; color: {TEAL_S}; font-size: 11px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; }}
.gfh-outcome-num {{ color: {TEAL}; font-family: Poppins, sans-serif; font-size: clamp(48px, 6vw, 72px); font-weight: 700; line-height: 1; letter-spacing: -0.03em; }}
.gfh-outcome-what {{ margin-top: 12px; margin-bottom: 0; color: {INK}; font-family: Inter, sans-serif; font-size: clamp(17px, 1.6vw, 20px); font-weight: 600; line-height: 1.4; }}
.gfh-outcome-meta {{ width: 100%; margin-top: auto; padding-top: 16px; }}
.gfh-outcome-row {{ display: grid; grid-template-columns: 110px 1fr; grid-column-gap: 10px; padding-top: 8px; border-top: 1px solid {LINE}; margin-top: 8px; }}
.gfh-outcome-k {{ padding-top: 2px; color: {INK3}; font-size: 12px; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; }}
.gfh-outcome-v {{ color: {INK2}; font-size: 14.5px; line-height: 1.5; }}
.gfh-closing-links {{ display: flex; flex-wrap: wrap; align-items: center; grid-column-gap: 32px; grid-row-gap: 12px; }}
.gfh-next {{ color: rgba(255,255,255,0.86); font-size: 16px; font-weight: 600; text-decoration: none; }}
.gfh-next:hover {{ color: #6fd9cb; }}
.gfh-draft {{ margin-top: 0; padding: 12px 14px; border: 1px dashed {D_LINE}; border-radius: 8px; background-color: {D_BG}; color: {D_INK}; font-size: 14px; line-height: 1.5; }}
.gfh-draft.is-sm {{ margin-top: 10px; padding: 8px 10px; font-size: 13px; }}
.gfh-draft.is-spaced {{ margin-top: 20px; }}
.gfh-draft.is-in-chain {{ margin-top: 10px; padding: 8px 10px; font-size: 13px; }}
.gfh-draft-k {{ margin-bottom: 3px; font-size: 11px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; }}
.gfh-draft-t {{ color: {D_INK}; }}
.gfh-draft-list {{ margin-top: 4px; margin-bottom: 0; padding-left: 18px; }}
.gfh-draft-li {{ color: {D_INK}; }}
.dcw-section.is-draft {{ display: none; border-top: 2px dashed {D_LINE}; background-color: #fffdf7; }}
.gfh-draft-banner {{ margin-bottom: 24px; padding: 10px 14px; border-radius: 8px; background-color: #fff0cc; color: {D_INK}; font-size: 14px; }}
"""
MED = f"""
.gfh-trio {{ grid-column-gap: 16px; }}
.gfh-deliv {{ grid-template-columns: repeat(3, 1fr); }}
.gfh-focus {{ grid-template-columns: 1fr 1fr; }}
.gfh-challenge {{ grid-template-columns: 1fr; }}
.gfh-challenge-media {{ max-width: 440px; }}
.gfh-sticky {{ position: static; }}
.gfh-struct {{ grid-template-columns: 1fr; }}
.gfh-decision {{ grid-template-columns: 1fr; }}
.gfh-view.is-side {{ max-height: 520px; }}
"""
SMALL = f"""
.gfh-trio {{ grid-template-columns: 1fr; grid-row-gap: 40px; }}
.gfh-fig {{ width: 100%; max-width: 380px; margin-left: auto; margin-right: auto; }}
.gfh-deliv {{ grid-template-columns: 1fr 1fr; }}
.gfh-pair {{ grid-template-columns: 1fr; }}
.gfh-focus {{ grid-template-columns: 1fr; }}
.gfh-cmp {{ grid-template-columns: 1fr; }}
.gfh-outcomes {{ grid-template-columns: 1fr; }}
.gfh-outcome-row {{ grid-template-columns: 1fr; grid-row-gap: 2px; }}
.gfh-constraint {{ flex-direction: column; grid-row-gap: 8px; }}
.gfh-hero-frame {{ max-width: 340px; }}
.gfh-view.is-hero {{ max-height: 480px; }}
.gfh-view.is-compare {{ max-height: 320px; }}
.gfh-view.is-gallery {{ max-height: 440px; }}
.gfh-strip {{ grid-auto-columns: 78vw; }}
"""
TINY = """
.gfh-deliv { grid-template-columns: 1fr; }
"""

def parse_rules(css):
    return [(m.group(1).strip(), m.group(2).strip()) for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", css) if m.group(1).strip()]

RULES = {"base": parse_rules(BASE), "med": parse_rules(MED), "small": parse_rules(SMALL), "tiny": parse_rules(TINY)}
MQ = {"med": "@media screen and (max-width: 991px)", "small": "@media screen and (max-width: 767px)", "tiny": "@media screen and (max-width: 479px)"}

def css_for(html, done):
    classes = set(c for attr in re.findall(r'class="([^"]+)"', html) for c in attr.split())
    def used(sel, bp):
        names = re.findall(r"\.([\w-]+)", sel.split(":")[0])
        return names and all(c in classes for c in names) and (bp, sel) not in done
    parts = []
    for bp in ("base", "med", "small", "tiny"):
        rs = [(s, b) for s, b in RULES[bp] if used(s, bp)]
        for s, _ in rs: done.add((bp, s))
        txt = " ".join(f"{s} {{ {b} }}" for s, b in rs)
        if txt: parts.append(txt if bp == "base" else f"{MQ[bp]} {{ {txt} }}")
    return "\n".join(parts)

def compact(h):
    return re.sub(r">\s+<", "><", h).strip()

ORDER = ["hero", "overview", "solution", "challenge", "architecture", "visual", "wireframes", "design", "feedback", "final", "outcomes", "reflection", "closing"]

if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    done, out = set(), []
    for k in ORDER:
        h = compact(S[k])
        out.append({"label": k, "html": h, "css": css_for(h, done)})
    json.dump(out, open(os.path.join(HERE, "out/grove-sections.json"), "w"), ensure_ascii=False, indent=1)
    used = set(c for o in out for attr in re.findall(r'class="([^"]+)"', o["html"]) for c in attr.split())
    print("classes used:", " ".join(sorted(c for c in used if c.startswith("dcw-") or c.startswith("is-"))))
    for o in out:
        print(o["label"], len(o["html"]), len(o["css"]))
