"""Generate Webflow-compatible HTML/CSS chunks for the DC Water case study.

Webflow's HTML importer only accepts single-class (and combo-class)
selectors, no pseudo-elements and no descendant selectors, so this
markup uses flat `dcw-` classes and real elements for decorations.

Usage: python3 webflow/build.py   -> writes webflow/out/sections.json
"""
import json, os, re, html as H

ASSET = "https://cdn.prod.website-files.com/68caf66283367e4c3b2f3706/"
PH = {
    "hero": ASSET + "6acc44ec30c62e248c3089d5_ph-hero-final-mockup.png",
    "phone": ASSET + "6acc456fdd0c8e3018726091_dcw-ph-phone.png",
    "board": ASSET + "6acc456f3d187e174caf33b7_dcw-ph-board.png",
    "sketch": ASSET + "6acc456ff590656966da3597_dcw-ph-sketch.png",
}
V = {  # Webflow variables (collection "DCW Phone frame")
    "pad": "var(--_dcw-phone-frame---dcw-phone-pad)",
    "rad": "var(--_dcw-phone-frame---dcw-phone-radius)",
    "srad": "var(--_dcw-phone-frame---dcw-phone-screen-radius)",
    "island": "var(--_dcw-phone-frame---dcw-phone-island-h)",
    "btn": "var(--_dcw-phone-frame---dcw-phone-btn-w)",
    "body": "var(--_dcw-phone-frame---dcw-phone-body)",
    "rim": "var(--_dcw-phone-frame---dcw-phone-rim)",
}
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# asset manifest from the prototype (labels, alt text, file names)
import subprocess
ASSETS = json.loads(subprocess.check_output(["node", "-e",
    'const w={};new Function("window",require("fs").readFileSync(process.argv[1],"utf8"))(w);'
    'process.stdout.write(JSON.stringify(w.CASE_STUDY_ASSETS))', os.path.join(ROOT, "js/assets.js")]))

e = H.escape

# ---------------------------------------------------------------- helpers
def img(asset_id, cls="dcw-mock-screen", kind=None):
    a = ASSETS[asset_id]
    kind = kind or a["kind"]
    src = PH["hero"] if asset_id == "hero-mockup" else PH.get(kind, PH["phone"])
    return (f'<img class="{cls}" src="{src}" alt="{e(a["alt"])}" '
            f'data-asset="{e(a["file"])}" loading="lazy">')

def mock(asset_id, extra=""):
    return (f'<div class="dcw-mock{(" " + extra) if extra else ""}"><div class="dcw-mock-body">'
            f'<div class="dcw-mock-btn"></div><div class="dcw-mock-btn-l"></div>'
            f'<div class="dcw-mock-island"></div>{img(asset_id)}</div></div>')

def fig(asset_id, title=None, text=None, num=None, extra_mock=""):
    cap = ""
    if title or text or num:
        cap = '<div class="dcw-fig-cap">'
        if num: cap += f'<div class="dcw-fig-num">{num}</div>'
        if title: cap += f'<div class="dcw-fig-title">{title}</div>'
        if text: cap += f'<p class="dcw-fig-text">{text}</p>'
        cap += "</div>"
    return f'<div class="dcw-fig">{mock(asset_id, extra_mock)}{cap}</div>'

def head(num, label, h2, lede=None, dark=False):
    d = " is-on-dark" if dark else ""
    out = (f'<div class="dcw-head"><div class="dcw-eyebrow{d}"><span class="dcw-eyebrow-num{d}">{num}</span>{label}</div>'
           f'<h2 class="dcw-h2{d}">{h2}</h2><div class="dcw-h2-bar"></div>')
    if lede: out += f'<p class="dcw-lede{d}">{lede}</p>'
    return out + "</div>"

def tag(t): return f'<div class="dcw-tag">{t}</div>'

def chain(learned, changed, changed_key="What changed"):
    return ('<div class="dcw-chain">'
            f'<div class="dcw-chain-card"><div class="dcw-chain-k">What we learned</div><p class="dcw-chain-p">{learned}</p></div>'
            '<div class="dcw-chain-arrow">↓</div>'
            f'<div class="dcw-chain-card is-changed"><div class="dcw-chain-k is-changed">{changed_key}</div><p class="dcw-chain-p is-changed">{changed}</p></div>'
            '</div>')

def cmp_item(label, asset_id, caption=None, after=False):
    lab = f'<div class="dcw-cmp-label{" is-after" if after else ""}">{label}</div>'
    cap = f'<p class="dcw-fig-text">{caption}</p>' if caption else ""
    return f'<div class="dcw-cmp-item">{lab}{mock(asset_id)}{cap}</div>'

def decision(id_, title, learned, changed, items, changed_key="What changed", quad=False):
    cls = "dcw-cmp is-quad" if quad else "dcw-cmp"
    return (f'<div class="dcw-decision" id="{id_}"><div class="dcw-decision-text">'
            f'<h4 class="dcw-decision-title">{title}</h4>{chain(learned, changed, changed_key)}</div>'
            f'<div class="{cls}">{"".join(items)}</div></div>')

def results(wins, opps, callout=None):
    def card(kind, icon, kicker, title, items, mark, extra=""):
        li = "".join(f'<li class="dcw-rc-item is-{kind}"><span class="dcw-rc-mark is-{kind}" aria-hidden="true">{mark}</span>'
                     f'<span class="dcw-rc-text is-{kind}">{x}</span></li>' for x in items)
        return (f'<div class="dcw-rc is-{kind}"><div class="dcw-rc-head is-{kind}">'
                f'<div class="dcw-rc-icon is-{kind}" aria-hidden="true">{icon}</div>'
                f'<div class="dcw-rc-titles"><div class="dcw-rc-kicker is-{kind}">{kicker}</div><h4 class="dcw-rc-title is-{kind}">{title}</h4></div>'
                f'<div class="dcw-rc-count is-{kind}" aria-hidden="true">{len(items):02d}</div></div>'
                f'<ul class="dcw-rc-list">{li}</ul>{extra}</div>')
    c = (f'<div class="dcw-callout is-light"><span class="dcw-callout-num is-light">{callout[0]}</span>'
         f'<span class="dcw-callout-text is-light">{callout[1]}</span></div>') if callout else ""
    return ('<div class="dcw-results">'
            + card("wins", "✓", "What worked", "Wins", wins, "✓", c)
            + card("opps", "↗", "What to improve", "Opportunities", opps, "→")
            + '</div>')

def wireframes():
    screens = ["Choice between form and camera", "Camera view", "Problem details: drawer or full page", "Submission confirmation", "Ticket number"]
    li = "".join(f'<li class="dcw-wf-item"><span class="dcw-wf-n">{i:02d}</span>{t}</li>' for i, t in enumerate(screens, 1))
    return ('<div class="dcw-block" id="ir-wireframes"><div class="dcw-wf">'
            '<div class="dcw-wf-copy"><div class="dcw-tag">Wireframes · Sprint 5</div><h3 class="dcw-h3">Wireframing the main screens</h3>'
            '<p class="dcw-p">The team then wireframed the main screens of the image recognition design. They included:</p>'
            f'<ol class="dcw-wf-list">{li}</ol></div>'
            f'<div class="dcw-wf-frame">{img("ir-wireframes", "dcw-wf-img")}'
            '<p class="dcw-fig-text">Wireframes of the main image recognition screens.</p></div>'
            '</div></div>')

def goals(items):
    out = '<div class="dcw-goals">'
    for i, (t, link) in enumerate(items, 1):
        l = f'<a class="dcw-goal-link" href="{link[1]}">{link[0]} →</a>' if link else ""
        out += f'<div class="dcw-goal"><div class="dcw-goal-num">{i:02d}</div><div class="dcw-goal-text">{t}</div>{l}</div>'
    return out + "</div>"

def numbered(items):
    out = '<div class="dcw-numbered">'
    for i, (h, p) in enumerate(items, 1):
        hh = f'<h4 class="dcw-num-h">{h}</h4>' if h else ""
        out += f'<div class="dcw-num-item"><div class="dcw-num-n">{i:02d}</div><div class="dcw-num-body">{hh}<p class="dcw-p is-sm">{p}</p></div></div>'
    return out + "</div>"

def stats(items):
    return '<div class="dcw-stats">' + "".join(
        f'<div class="dcw-stat"><div class="dcw-stat-n">{n}</div><div class="dcw-stat-l">{l}</div></div>' for n, l in items) + "</div>"

def screens(items, cols=""):
    return f'<div class="dcw-screens{(" " + cols) if cols else ""}">' + "".join(fig(*it) for it in items) + "</div>"

def strip(label, ids_caps, extra=""):
    figs = "".join(
        f'<div class="dcw-strip-item">{mock(a)}<div class="dcw-fig-text is-xs">{c}</div></div>' for a, c in ids_caps)
    return (f'<div class="dcw-strip-wrap"><div class="dcw-strip-label">{label} <span class="dcw-strip-hint">Scroll →</span></div>'
            f'<div class="dcw-strip{(" " + extra) if extra else ""}">{figs}</div></div>')

def board(asset_id, caption=None):
    cap = f'<p class="dcw-fig-text">{caption}</p>' if caption else ""
    return f'<div class="dcw-artifact">{img(asset_id, "dcw-board-img")}{cap}</div>'


# ---------------------------------------------------------------- sections
S = {}

S["hero"] = f'''<header class="dcw-section is-hero" id="top">
<div class="dcw-hero-dots"></div>
<div class="dcw-wrap"><div class="dcw-hero-grid">
<div class="dcw-hero-copy">
<div class="dcw-eyebrow is-on-dark">UX case study · HCIM capstone · 2022</div>
<h1 class="dcw-h1">DC Water</h1>
<p class="dcw-hero-tagline">Helping District of Columbia residents and visitors report water-related problems.</p>
<p class="dcw-p is-on-dark">A redesigned, mobile-responsive Report a Problem form, a new Customer Service form, and an image recognition concept, designed with DC Water over Sprints 3–5 of a five-sprint capstone project.</p>
<div class="dcw-hero-actions"><a class="dcw-btn is-hero" href="#prototypes">View finished designs ↓</a></div>
<div class="dcw-facts">
<div class="dcw-fact"><div class="dcw-chip is-on-dark"><span class="dcw-chip-dot"></span>My role</div><div class="dcw-fact-v">UX designer · Sprint 4 facilitator</div></div>
<div class="dcw-fact"><div class="dcw-chip is-on-dark"><span class="dcw-chip-dot"></span>Client</div><div class="dcw-fact-v">DC Water</div></div>
<div class="dcw-fact"><div class="dcw-chip is-on-dark"><span class="dcw-chip-dot"></span>Timeline</div><div class="dcw-fact-v">January – May 2022</div></div>
<div class="dcw-fact"><div class="dcw-chip is-on-dark"><span class="dcw-chip-dot"></span>Status</div><div class="dcw-fact-v">Development in progress</div></div>
</div></div>
<div class="dcw-hero-visual"><div class="dcw-hero-halo"></div>{mock("hero-mockup", "is-hero")}</div>
</div></div></header>'''

pills = ["User research", "Card sorting", "User scenarios", "User flows", "Wireframes", "Visual design",
         "Interaction design", "Prototyping", "User testing", "Figma"]
S["overview"] = f'''<section class="dcw-section" id="overview"><div class="dcw-wrap">
{head("01", "Project overview", "Most reports arrived by phone, not through the web form")}
<div class="dcw-split">
<div class="dcw-col">
<div class="dcw-kicker">The problem</div>
<p class="dcw-statement">DC Water has a web form for reporting problems, but most reports come in through the emergency hotline. That leads to a high volume of calls and slower response times.</p>
<p class="dcw-p">DC Water distributes drinking water and collects and treats wastewater for residents and visitors of the District of Columbia. Its web form lets people report issues such as leaks and broken fire hydrants, so customers and DC Water can resolve problems in homes and neighborhoods together.</p>
<div class="dcw-kicker is-spaced">Design challenge</div>
<p class="dcw-p">DC Water wants to drive users to its mobile-responsive web form and make reporting problems more efficient.</p>
</div>
<div class="dcw-meta">
<div class="dcw-meta-row"><div class="dcw-meta-k">Client</div><div class="dcw-meta-v">DC Water</div></div>
<div class="dcw-meta-row"><div class="dcw-meta-k">Context</div><div class="dcw-meta-v">HCIM Capstone Project</div></div>
<div class="dcw-meta-row"><div class="dcw-meta-k">Team</div><div class="dcw-meta-v">Niku Letang, Camila Velloso, Ruiqi Li, Saskia Beitzell, Carolyn Shipe, Aubrey Parrish</div></div>
<div class="dcw-meta-row"><div class="dcw-meta-k">Timeline</div><div class="dcw-meta-v">January – May 2022 · five 4-week sprints</div></div>
<div class="dcw-meta-row"><div class="dcw-meta-k">Project status</div><div class="dcw-meta-v">Development in progress</div></div>
<div class="dcw-meta-row"><div class="dcw-meta-k">Methods &amp; tools</div><div class="dcw-pills">{"".join(f'<div class="dcw-chip"><span class="dcw-chip-dot"></span>{p}</div>' for p in pills)}</div></div>
</div></div>
<div class="dcw-block">
<h3 class="dcw-h3">My role and the team's work</h3>
<p class="dcw-p is-measure">At the end of Sprint 2 the team changed, and I was one of the members who joined the project midway through the semester. <strong class="dcw-strong">Because I joined at the beginning of Sprint 3, this case study focuses on Sprints 3–5 only.</strong></p>
<div class="dcw-role-cols"><div class="dcw-who-card is-mine"><div class="dcw-role-head"><div class="dcw-role-kicker is-mine">My part · Sprints 3–5</div><h4 class="dcw-role-title is-mine">My contributions</h4></div><ol class="dcw-role-list"><li class="dcw-role-item is-mine"><span class="dcw-role-n is-mine">01</span><span class="dcw-role-text is-mine">Conducted card sorting activities, user interviews, user testing, and prototyping.</span></li><li class="dcw-role-item is-mine"><span class="dcw-role-n is-mine">02</span><span class="dcw-role-text is-mine">Worked on the visual and interactive designs.</span></li><li class="dcw-role-item is-mine"><span class="dcw-role-n is-mine">03</span><span class="dcw-role-text is-mine">As facilitator of Sprint 4, directed the course of the project, oversaw the schedule, and led client presentations.</span></li><li class="dcw-role-item is-mine"><span class="dcw-role-n is-mine">04</span><span class="dcw-role-text is-mine">In Sprint 5, the team divided the work and I worked only on the image recognition concept.</span></li></ol></div><div class="dcw-who-card is-team"><div class="dcw-role-head"><div class="dcw-role-kicker">Team of six</div><h4 class="dcw-role-title">Team process</h4><div class="dcw-team-dots" aria-hidden="true"><span class="dcw-team-dot is-me"></span><span class="dcw-team-dot"></span><span class="dcw-team-dot"></span><span class="dcw-team-dot"></span><span class="dcw-team-dot"></span><span class="dcw-team-dot"></span></div></div><ol class="dcw-role-list"><li class="dcw-role-item is-team"><span class="dcw-role-n is-team">01</span><span class="dcw-role-text is-team">The team of six worked in five 4-week sprints based on the Google Ventures Design Sprint process.</span></li><li class="dcw-role-item is-team"><span class="dcw-role-n is-team">02</span><span class="dcw-role-text is-team">Each sprint covered research and analysis, ideation, design, evaluation, and refinement.</span></li><li class="dcw-role-item is-team"><span class="dcw-role-n is-team">03</span><span class="dcw-role-text is-team">Research, design iterations, and testing described below were carried out as a team ("we") unless noted as mine.</span></li></ol></div></div>
</div></div>
<div class="dcw-block">
<div class="dcw-kicker">Where this case study sits</div>
<div class="dcw-timeline">
<div class="dcw-tl"><div class="dcw-tl-h">Sprint 1</div><div class="dcw-tl-t">Before I joined · user testing</div></div>
<div class="dcw-tl"><div class="dcw-tl-h">Sprint 2</div><div class="dcw-tl-t">Before I joined · user testing</div></div>
<div class="dcw-tl is-mine"><div class="dcw-tl-join">I joined</div><div class="dcw-tl-h is-mine">Sprint 3</div><div class="dcw-tl-t is-mine">Research, IA, and first reporting-form iteration</div></div>
<div class="dcw-tl is-lead"><div class="dcw-tl-h is-lead">Sprint 4</div><div class="dcw-tl-t is-lead">Second iteration and Customer Service form (I facilitated)</div></div>
<div class="dcw-tl is-mine"><div class="dcw-tl-h is-mine">Sprint 5</div><div class="dcw-tl-t is-mine">Alternative reporting methods: image recognition concept</div></div>
</div>
<p class="dcw-caption">Sprint numbers appear throughout as supporting context. The page is organized around the problem and the design decisions.</p>
</div></div></section>'''

def pv(asset_id, step, title, text):
    return (f'<div class="dcw-pv">{mock(asset_id, "is-pv")}<div class="dcw-pv-cap"><div class="dcw-pv-step">{step}</div>'
            f'<div class="dcw-fig-title">{title}</div><p class="dcw-fig-text">{text}</p></div></div>')

S["solution"] = f'''<section class="dcw-section is-tint" id="solution"><div class="dcw-wrap">
{head("02", "Solution preview", "Report a problem, receive updates, and track it to resolution", "The redesigned Report a Problem form separates water problems from general inquiries, lets people choose how they hear back, and gives every report a trackable ticket.")}
<div class="dcw-preview">
{pv("rap-04", "01 · Report", "Plain-language choices", "People locate the problem, then pick from everyday categories such as Flooding / Leaking or Damage, with an Other / Not Sure option.")}
{pv("rap-06", "02 · Receive updates", "Notifications on their terms", "Separate choices for receiving updates about the ticket and for letting DC Water get in touch with questions, by phone call or email.")}
{pv("rap-11", "03 · Track", "Ticket status and details", "A status bar, case history, and the details of what was submitted, plus a way to rate the experience once the case is resolved.")}
</div>
<p class="dcw-caption">Screens are from the team's Figma prototypes. Prototype testing results are reported below. They are not production metrics.</p>
</div></section>'''

words = ["water", "colorful water", "kitchen", "bathroom flooded", "cloudy water", "water bill", "water usage",
         "poor water quality", "water quality", "water meter", "polluted water", "water pressure", "plumbing", "bathroom",
         "no water", "basement flooded", "water outage", "frozen pipes", "pipe noise", "blocked drain", "basement",
         "rain water", "manhole cover", "standing water", "storm drain", "icy roads", "hazard", "pipe", "exposed pipe",
         "burst main break", "main break", "weather", "leaking", "flooding", "sidewalk", "sewage", "access cover",
         "[illegible note]", "fire hydrant", "damage", "street", "infrastructure damage", "ice"]

S["research"] = f'''<section class="dcw-section" id="research"><div class="dcw-wrap">
{head("03", "Understanding the problem", "Learning how people describe water problems", "The form used DC Water's terminology. To fix that, we first needed to understand how people themselves group and name the problems they see.")}
<div class="dcw-split">
<div class="dcw-col">{tag("Starting point · Findings from Sprints 1–2")}<h3 class="dcw-h3">What earlier testing revealed</h3><p class="dcw-p">User testing in Sprints 1 and 2, before I joined, surfaced three problems with the existing design:</p></div>
{numbered([("Terminology was too technical", "Users were unsure how to define the issue they wanted to report."),
           ("“Emergency” made people hesitate", "Users hesitated to use the Emergency form because they were not confident their issue was a “true emergency.”"),
           ("Some issues were missing", "Other possible issues were not represented in the design, and users had no way to select them.")])}
</div>
<div class="dcw-block">{tag("Sprint 3 goals")}<h3 class="dcw-h3">Improve the current design to…</h3>
{goals([("Help users build confidence in making selections in the form", None),
        ("Clearly communicate the criteria for real emergencies", None),
        ("Provide more possible combinations of issue types and affected equipment", None),
        ("Revise terminology to match users' mental model", None)])}</div>
<div class="dcw-block"><div class="dcw-split is-reverse">
{board("research-card-sort", "The 15 images came from past submissions to the Report a Problem form and Twitter.")}
<div class="dcw-col">{tag("Research · Sprint 3")}<h3 class="dcw-h3">Image card sorting</h3>
<p class="dcw-p"><strong class="dcw-strong">Question:</strong> Because users had difficulty matching the issues on the form with the issue they wanted to report, we ran an unmoderated card sort to learn how they define and categorize issues.</p>
<ul class="dcw-ul"><li class="dcw-li">We pulled images from past submissions reported through the “Report a Problem” form and Twitter.</li><li class="dcw-li">Participants grouped similar images together and gave each group a name.</li></ul>
{stats([("10", "Participants"), ("15", "Images"), ("40", "Categories created")])}</div>
</div></div>
<div class="dcw-block"><div class="dcw-split">
<div class="dcw-col">{tag("Research · Sprint 3")}<h3 class="dcw-h3">Word bank and image association</h3>
<p class="dcw-p"><strong class="dcw-strong">Question:</strong> Which words do people connect with each kind of problem?</p>
<p class="dcw-p">Once we knew how users categorized issues, we turned their category names into a word bank. We then asked participants to think aloud about what they saw in each image and match as many words as they liked to it.</p>
{stats([("13", "Participants"), ("18–55", "Age range"), ("8", "Renters"), ("5", "Homeowners")])}</div>
<div class="dcw-col">{board("research-word-bank", "Twelve photos, each tagged with word stickies. Prompts: “1) Think out loud. What are you seeing in this image? 2) Drag n drop word sticky notes to the images you associate them with.”")}
<div class="dcw-kicker is-spaced">Word bank used in the activity</div>
<div class="dcw-words">{"".join(f'<div class="dcw-word{" is-illegible" if w.startswith("[") else ""}">{w}</div>' for w in words)}</div></div>
</div></div>
<div class="dcw-block"><h3 class="dcw-h3">Key findings from card sorting and image association</h3><div class="dcw-findings">
<div class="dcw-finding"><div class="dcw-finding-what"><span class="dcw-finding-dot"></span>Categorization varied widely. “Flooding” and “fire hydrant” were the only categories users had in common.</div><div class="dcw-finding-so"><div class="dcw-finding-k">Where it shows up</div>Flooding / Leaking appears as a problem type in the information architecture and in every later iteration.</div></div>
<div class="dcw-finding"><div class="dcw-finding-what"><span class="dcw-finding-dot"></span>Participants associated issues with their setting: indoors or outdoors.</div><div class="dcw-finding-so"><div class="dcw-finding-k">Where it shows up</div>The top level of the information architecture is Indoor, Outdoor, and Not Sure / Other.</div></div>
<div class="dcw-finding"><div class="dcw-finding-what"><span class="dcw-finding-dot"></span>Users misidentified more technical objects, such as a manhole and a water meter.</div><div class="dcw-finding-so"><div class="dcw-finding-k">Where it shows up</div>Echoed in Sprint 5: participants valued object descriptions that taught them the terminology while reporting.</div></div>
</div></div>
<div class="dcw-block"><div class="dcw-split">
<div class="dcw-col">{tag("Synthesis · Sprint 3")}<h3 class="dcw-h3">The resulting information architecture</h3><p class="dcw-p">We used the card sorting results as the basis for the information architecture. Problems are first grouped by where they happen, then by a small set of plain-language problem types, with an escape hatch for people who aren't sure.</p></div>
<div class="dcw-artifact"><div class="dcw-ia">
<div class="dcw-ia-col"><div class="dcw-ia-root">Indoor</div><div class="dcw-ia-item">Flooding &amp; Leaking</div><div class="dcw-ia-item">Water Pressure</div><div class="dcw-ia-item">No Water</div><div class="dcw-ia-item">Water Quality</div><div class="dcw-ia-item">Other / Unsure</div></div>
<div class="dcw-ia-col"><div class="dcw-ia-root">Outdoor</div><div class="dcw-ia-item">Flooding or Leaking</div><div class="dcw-ia-item">Damage</div><div class="dcw-ia-item">Other / Unsure</div></div>
<div class="dcw-ia-col"><div class="dcw-ia-root">Not Sure / Other</div><div class="dcw-ia-empty">No sub-categories</div></div>
</div><p class="dcw-fig-text">Rebuilt from the team's IA board.</p></div>
</div></div>
</div></section>'''

S["reporting"] = f'''<section class="dcw-section" id="reporting"><div class="dcw-wrap">
{head("04", "Designing and refining the reporting experience", "From an emergency form to a problem report people trust", "The first iteration put the new IA into a step-by-step form. Testing showed where language, privacy, and tracking still got in the way.")}
<div class="dcw-col">{tag("Iteration 1 · Sprint 3")}<h3 class="dcw-h3">The first redesigned form</h3><p class="dcw-p is-measure">A short, guided flow: say where the problem is, choose what it is, optionally add details and contact information, review, and get a ticket to track.</p></div>
{screens([("rap-v1-landing", "Landing page", "Detailed instructions for how to get started.", "01"),
          ("rap-v1-category", "Problem category", "An easy point of entry based on where the problem occurred, with the option to select “Other.”", "02"),
          ("rap-v1-subcategory", "Sub-category: Outdoors", "Common problem types based on the location of the issue.", "03"),
          ("rap-v1-details", "Problem details", "An optional opportunity to add a photo, suggested tags, and a description.", "04"),
          ("rap-v1-review", "Review", "The ability to correct information before submitting.", "05")], "is-5")}
<p class="dcw-caption">The contact information and tracking screens from this iteration are shown in the comparisons below.</p>
<div class="dcw-block">{tag("Usability testing · Sprint 3")}<h3 class="dcw-h3">What testing the first iteration showed</h3>
{results(["The form met user expectations and was understandable and easy to use.",
          "Most participants added their contact information and agreed to receive alerts.",
          "Users appreciated being able to add tags to give their issue more context.",
          "Participants found the ticket tracking process helpful.",
          "Users appreciated being able to review and edit their information before submitting."],
         ["“Emergency” language may cause hesitancy to fill out the form.",
          "Ticket status: users wanted to be reminded of what they submitted.",
          "Data privacy: some worried their contact information or data could be used to send unrelated alerts later.",
          "Users were initially unsure how to categorize a problem that could fit several categories.",
          "There was no option to choose a notification preference.",
          "Users wanted to add a comment after submitting the form.",
          "Most users couldn't think of a scenario where they'd use “Other” for a problem that is neither indoors nor outdoors."],
         ("4.6 / 5", "average confidence score"))}</div>
<div class="dcw-block" id="sprint-4"><div class="dcw-split is-even">
<div class="dcw-col">{tag("Sprint 4 design challenge")}<h3 class="dcw-h3">Sprint 4 goals</h3></div>
<p class="dcw-p">As facilitator of Sprint 4, I directed the course of the project, oversaw the schedule, and led client presentations. The sprint set four goals:</p></div>
{goals([("Update the web form to incorporate findings and recommendations from user testing", ("Design decisions below", "#d1")),
        ("Design a customer service form to redirect miscellaneous issues such as billing inquiries", ("Customer Service form", "#customer-service")),
        ("Hand off deliverables to developers and collaborate with them regularly, so the final product represents both users' and DC Water's needs", ("Outcomes", "#outcomes")),
        ("Design an artificial intelligence application that gives users an alternative, more efficient way to report a problem", ("Photo-based reporting", "#photo-reporting"))])}</div>
<div class="dcw-block">{tag("Iteration 2 · Sprint 4")}<h3 class="dcw-h3">Design decisions in the second iteration</h3><p class="dcw-p is-measure">We updated the web form based on the testing results. Each change below traces from a finding to the redesign.</p>
{decision("d1", "Terminology: from “Report an Emergency” to “Report a Problem”",
          "“Emergency” language may make people hesitate, and earlier testing showed users weren't sure their issue was a true emergency.",
          "The form title changed from “Report an Emergency” to “Report a Problem,” to make users less likely to abandon the form when they aren't sure their issue is a true emergency.",
          [cmp_item("Before · Iteration 1", "rap-v1-category"), cmp_item("After · Iteration 2", "rap-v2-title", after=True)])}
{decision("d2", "Notifications: preferences and clearer consent",
          "There was no way to choose a notification preference, and some participants worried their data could be used for unrelated alerts.",
          "A simpler, more concise contact form with notification preferences. Receiving updates was separated from allowing DC Water to make contact, and the screen states that DC Water will only contact the user about this ticket.",
          [cmp_item("Before · Iteration 1", "rap-v1-contact", "One yes/no question about status alerts."), cmp_item("After · Iteration 2", "rap-v2-notifications", "Updates and contact permissions chosen separately, by phone call or email.", True)])}
{decision("d3", "Ticket tracking: show what was submitted",
          "Participants found ticket tracking helpful but wanted to be reminded of what they had submitted.",
          "The ticket status page was redesigned to show the ticket's status and a new “Ticket Details” tab with the submitted information. An option to rate the experience and leave feedback was also added.",
          [cmp_item("Before · Iteration 1", "rap-v1-tracking", "Current status and generalized next steps."), cmp_item("After · Iteration 2", "rap-v2-ticket", "Case History and Ticket Details tabs, plus rating and feedback.", True)])}
{decision("d4", "Categories: fewer choices up front, a clear route when unsure",
          "Users were unsure how to categorize problems that fit several categories, and most couldn't imagine using “Other” for a problem that was neither indoors nor outdoors.",
          "“Where is the problem?” offers only Outdoors and Indoors, with a link to describe the issue if unsure. “Other / Not Sure” moves to the problem-type step. The final flow also starts with a location step.",
          [cmp_item("Before · Iteration 1", "rap-v1-category", "Outdoors, Indoors, Other."), cmp_item("Final", "rap-03", "Outdoors and Indoors, with a link for anyone who's unsure.", True)],
          changed_key="What the final screens show")}
</div>
<div class="dcw-block" id="customer-service"><div class="dcw-split">
<div class="dcw-col">{tag("Customer Service form · Sprint 4")}<h3 class="dcw-h3">Separating problems from inquiries</h3>
<p class="dcw-p">DC Water's previous form combined emergency issues and miscellaneous inquiries in one form, which confused users. We decided to direct people to two different forms based on their issue or inquiry, and designed a new Customer Service form for miscellaneous issues such as billing inquiries.</p>
<p class="dcw-p">First, we worked with DC Water to decide which options could be left out of the new form because they were covered elsewhere on its website.</p></div>
<div class="dcw-artifact"><div class="dcw-sort">
<div class="dcw-sort-col"><div class="dcw-sort-h">Remove</div><div class="dcw-sort-item">Installment Plan</div><div class="dcw-sort-item">CSO Tunnel</div><div class="dcw-sort-item">Service Restoration</div></div>
<div class="dcw-sort-col"><div class="dcw-sort-h">Other page</div><div class="dcw-sort-item">Employment opportunity</div><div class="dcw-sort-item">School Project</div><div class="dcw-sort-item">For Kids</div><div class="dcw-sort-item">Backwater valve request</div><div class="dcw-sort-item">Business opportunity</div></div>
<div class="dcw-sort-col is-keep"><div class="dcw-sort-h is-keep">Keep</div><div class="dcw-sort-item">Billing Inquiry</div><div class="dcw-sort-item">Request for Repair</div><div class="dcw-sort-item">GIS Map Issue</div><div class="dcw-sort-item">Pavement / Sidewalk / Tree box</div><div class="dcw-sort-item">Construction / Restoration</div></div>
</div><p class="dcw-fig-text">Rebuilt from the sorting activity with DC Water.</p></div></div>
{screens([("cs-01", "Select a topic", "Billing Inquiry, Damage, or Other.", "01"),
          ("cs-03", "Additional details", "“How can we help you?”, location, suggested tags, and a file.", "02"),
          ("cs-05", "Contact information", "Optional, for a reply, with an account number if applicable.", "03"),
          ("cs-06", "Review", "Every answer can be edited before submitting.", "04")])}
</div></div></section>'''

def idea(t, s, picked=False):
    p = " is-picked" if picked else ""
    return f'<div class="dcw-idea{p}"><div class="dcw-idea-t">{t}</div><div class="dcw-idea-s{p}">{s}</div></div>'

def ab_opt(asset_id, opt, title, text):
    return (f'<div class="dcw-fig">{mock(asset_id)}<div class="dcw-fig-cap"><div class="dcw-fig-num is-teal">{opt}</div>'
            f'<div class="dcw-fig-title">{title}</div><p class="dcw-fig-text">{text}</p></div></div>')

S["photo"] = f'''<section class="dcw-section is-tint" id="photo-reporting"><div class="dcw-wrap">
{head("05", "Exploring photo-based reporting", "Could a photo do the describing for you?", "We finished the Report a Problem and Customer Service forms earlier than expected, so in Sprint 5 we designed alternative ways to report a problem.")}
<div class="dcw-notice"><div class="dcw-badge">Concept</div><p class="dcw-p is-sm">Image recognition is a <strong class="dcw-strong">concept</strong>, designed and tested as a Figma prototype. The recognition shown is simulated, not working functionality.</p></div>
<div class="dcw-block"><div class="dcw-split">
<div class="dcw-col">{tag("Exploration brief · Sprint 5")}<h3 class="dcw-h3">The brief</h3><p class="dcw-p">Sprint 4's plan included designing an artificial intelligence application to give users an alternative, more efficient way to report a problem. Sprint 5 set out to:</p></div>
{numbered([(None, "Research existing products that use machine learning and artificial intelligence to see whether there's an opportunity for a new Report a Problem solution."),
           (None, "Run lightning demos on alternative products."), (None, "Sketch new ideas."), (None, "Design new products.")])}
</div></div>
<div class="dcw-block"><div class="dcw-grid-2">
<div class="dcw-col"><h3 class="dcw-h3">Lightning demos</h3><p class="dcw-p"><strong class="dcw-strong">Purpose:</strong> find inspiring products, services, or experiences that could be adapted to DC Water's need for reporting water-related issues.</p><p class="dcw-p">Standout examples included, but weren't limited to:</p>
<div class="dcw-ideas">{idea("Waze", "Real-time traffic reporting")}{idea("Chipotle", "Chatbot")}{idea("Google Lens", "&nbsp;")}{idea("Apple", "Text support")}</div></div>
<div class="dcw-col"><h3 class="dcw-h3">Sketching and alternatives considered</h3><p class="dcw-p">The lightning demos triggered a wide range of ideas. The team brought them to DC Water, who voted for the ones they believed would meet users' needs while being logistically and financially feasible.</p>
<div class="dcw-ideas">{idea("Public kiosk", "Not pursued")}{idea("Image recognition", "Selected by DC Water · my focus", True)}{idea("Chatbot", "Selected by DC Water", True)}{idea("SMS solution", "Not pursued")}{idea("Video conferencing", "Not pursued")}</div>
<p class="dcw-p is-spaced">The team divided the work. I worked only on image recognition, so it's the only concept in this case study.</p></div>
</div></div>
<div class="dcw-block"><div class="dcw-split is-center">
<div class="dcw-col"><h3 class="dcw-h3">From sketch to wireframes</h3>
<p class="dcw-p"><strong class="dcw-strong">Sketch:</strong> the core idea in a single screen. Point the camera at the problem, let the product name the object (“Object Detected: Fire Hydrant”) with a short definition, then confirm or try again.</p>
</div>
<div class="dcw-sketch">{img("ir-sketch", "dcw-sketch-img")}<p class="dcw-fig-text">Sketch for reporting a problem using image recognition.</p></div>
</div></div>
{wireframes()}
<div class="dcw-block">{tag("Iteration 1 · Sprint 5")}<h3 class="dcw-h3">Initial polished designs</h3><p class="dcw-p is-measure">Photograph or upload the problem, see what the product recognized, and submit pre-filled details.</p>
{screens([("ir-v1-landing", "Landing page", "Similar to the Report a Problem form, with split buttons for choosing how to report.", "01"),
          ("ir-v1-camera", "Camera view", "The user opens the camera and aims it at the object.", "02"),
          ("ir-v1-description", "Object description", "The product identifies the object and describes it.", "03"),
          ("ir-v1-drawer", "Problem details", "Details about the issue are filled in automatically in a drawer.", "04")])}
{strip("5 more screens from iteration 1", [("ir-v1-upload", "Upload: take a photo or choose one"), ("ir-v1-collapsed", "Collapsible drawer"), ("ir-v1-library", "Photo library"), ("ir-v1-confirm", "Confirmation after “Submit”"), ("ir-v1-ticket", "Ticket number")], "is-scroll")}
</div>
<div class="dcw-block">{tag("Comparative testing · Sprint 5")}<h3 class="dcw-h3">Testing two directions for the landing and details screens</h3>
<p class="dcw-p is-measure">After the first iteration, we had different ideas for the interface and interactions, especially for the landing page and the problem details page. The team couldn't agree on the best options, so we tested both versions of each pair of screens with users.</p>
<p class="dcw-p is-sm"><strong class="dcw-strong">6 participants</strong>, all of whom had tested the Report a Problem form. Goals: overall impressions of image recognition, and how it compares with the Report a Problem form for ease of use and effectiveness.</p>
<div class="dcw-ab">
<div class="dcw-col"><h4 class="dcw-h4">Landing page</h4><div class="dcw-ab-opts">
{ab_opt("ab-landing-a", "Option A", "Split button", "Like the Report a Problem landing page, but “Report a Problem” splits into two buttons: fill out the traditional form or use image recognition.")}
{ab_opt("ab-landing-b", "Option B", "Photo layout", "Image recognition is the default. “Show us the issue” then offers image recognition or the traditional form. This assumed image recognition would be the easiest, most efficient option and that users would want to start with the fastest one.")}</div></div>
<div class="dcw-col"><h4 class="dcw-h4">Problem details</h4><div class="dcw-ab-opts">
{ab_opt("ab-details-a", "Option A", "Interaction drawer", "A drawer pattern we found in existing image recognition products. We liked its modern look but worried drawers are native to apps and might not translate well to responsive web pages.")}
{ab_opt("ab-details-b", "Option B", "Full page", "A more classic layout, which we liked because the “Add Photo” button is very visible.")}</div></div>
</div>
{results(["The photo layout landing page was simple and easy to use.",
          "Users noticed and used the additional photo button on the full-page problem details layout.",
          "The design met users' expectations about what would happen after uploading a photo.",
          "Users appreciated the object descriptions after uploading a photo because they could learn the terminology while reporting.",
          "Users liked that tags were selected automatically after uploading a photo, and appreciated being able to select more."],
         ["The “Image Identifier” label on the split-button landing page confused some users, who didn't know what to expect.",
          "Users were unlikely to close the drawer on the problem details page unless they wanted a full view of their image.",
          "Users didn't notice the additional photo button in the drawer layout.",
          "Users found the confirmation message after selecting “Submit” unnecessary.",
          "Users didn't know how to save the ticket number after submitting."],
         ("6 of 6", "participants said they'd prefer image recognition over the Report a Problem form (prototype preference)"))}
</div>
<div class="dcw-block">{tag("Iteration 2 · Sprint 5")}<h3 class="dcw-h3">Revisions after testing</h3>
{decision("ir-d1", "Submitting and tracking without a ticket number",
          "The confirmation message after “Submit” felt unnecessary, and users didn't know how to save the ticket number.",
          "The extra submit step was removed: users get a thank-you message and can exit right away. The copy-ticket-number option was removed, and users track their report by uploading the original photo.",
          [cmp_item("Before · Iteration 1", "ir-v1-confirm"), cmp_item("Before · Iteration 1", "ir-v1-ticket"),
           cmp_item("After · Iteration 2", "ir-v2-thanks", after=True), cmp_item("After · Iteration 2", "ir-v2-tracking", after=True)], quad=True)}
{decision("ir-d2", "Landing page and problem details layouts",
          "The photo layout landing page was simple and easy to use, while “Image Identifier” confused some users. Users noticed the additional photo button on the full-page layout but not in the drawer.",
          "The final prototype uses the photo layout landing page (“Show Us The Issue”) and the full-page problem details, where users can add another photo.",
          [cmp_item("Final landing", "ir-01", after=True), cmp_item("Additional photo uploaded", "ir-v2-photo", "The view after the user selects “Add Photo.”", True)],
          changed_key="What the final screens show")}
<h4 class="dcw-decision-title is-spaced">Other additions in the second iteration <span class="dcw-strip-hint" aria-hidden="true">Scroll →</span></h4>
{screens([("ir-v2-error", "Error", "A message when an uploaded photo isn't recognized as an eligible DC Water object."),
          ("ir-v2-form-option", "Form option", "“No photo? Fill out a form.” sends users to the Report a Problem form when image recognition isn't suitable."),
          ("ir-v2-outline", "Object outline", "A label and an outline around the object make it easy to identify."),
          ("ir-v2-location", "Location", "Users can edit their location if the detected location is inaccurate.")], "is-scroll")}
</div>
</div></section>'''

RAP_ALL = [("rap-01", "Landing"), ("rap-02", "Location"), ("rap-03", "Where is the problem?"), ("rap-04", "What is the problem?"),
           ("rap-05", "Additional details"), ("rap-06", "Notifications"), ("rap-07", "Review"), ("rap-08", "Submitted"),
           ("rap-09", "Track your report"), ("rap-10", "Ticket opened"), ("rap-11", "Ticket closed"), ("rap-12", "Experience rated"),
           ("rap-13", "Feedback"), ("rap-14", "Feedback sent")]
CS_ALL = [("cs-01", "Select a topic"), ("cs-02", "Topic selected"), ("cs-03", "Additional details"), ("cs-04", "Details filled in"),
          ("cs-05", "Contact information"), ("cs-06", "Review"), ("cs-07", "Submitted")]
IR_ALL = [("ir-01", "Landing"), ("ir-02", "Photo options"), ("ir-03", "Camera"), ("ir-04", "Not recognized"), ("ir-05", "Aiming at a hydrant"),
          ("ir-06", "Outlined and described"), ("ir-07", "Problem details"), ("ir-08", "Edit location"), ("ir-09", "Photo library"),
          ("ir-10", "Second photo"), ("ir-11", "Second photo recognized"), ("ir-12", "Details, two photos"), ("ir-13", "Thank you"),
          ("ir-14", "Track by photo"), ("ir-15", "Ticket status")]

def flow(id_, title, badge, poster, steps, trio, all_screens, concept=False):
    st = "".join(f'<div class="dcw-step"><div class="dcw-step-n">{i}</div><div class="dcw-step-t">{s}</div></div>' for i, s in enumerate(steps, 1))
    tr = "".join(f'<div class="dcw-fig">{mock(a)}<div class="dcw-fig-title is-on-dark">{c}</div></div>' for a, c in trio)
    strip_items = "".join(f'<div class="dcw-strip-item">{mock(a)}<div class="dcw-fig-text is-xs is-on-dark">{i:02d} · {c}</div></div>' for i, (a, c) in enumerate(all_screens, 1))
    b = "dcw-badge is-on-dark" if concept else "dcw-badge is-muted-dark"
    return f'''<div class="dcw-flow" id="{id_}"><div class="dcw-flow-head"><h3 class="dcw-h3 is-on-dark">{title}</h3><div class="{b}">{badge}</div></div>
<div class="dcw-flow-grid"><div class="dcw-proto"><div class="dcw-proto-stage">{mock(poster, "is-poster")}</div>
<a class="dcw-btn is-ghost-dark" href="#" data-figma-link="{id_}">Open prototype in Figma ↗</a>
<p class="dcw-proto-note">Figma link to be added: select this button and set its link in the Settings panel.</p></div>
<div class="dcw-col"><div class="dcw-steps">{st}</div><div class="dcw-screens is-3">{tr}</div></div></div>
<div class="dcw-strip-wrap"><div class="dcw-strip-label is-on-dark">All {len(all_screens)} screens <span class="dcw-strip-hint is-on-dark">Scroll →</span></div><div class="dcw-strip">{strip_items}</div></div></div>'''

S["prototypes"] = f'''<section class="dcw-section is-dark" id="prototypes"><div class="dcw-wrap">
{head("06", "Final experience and prototypes", "Three flows, prototyped in Figma", "Explore each prototype or browse the complete set of screens.", dark=True)}
{flow("flow-rap", "Report a Problem", "Designed · tested in Sprint 3 · refined in Sprint 4", "rap-01",
      ["Choose Report a Problem, Track Your Report, or Customer Service.", "Set the location by address, current location, or a dropped pin.",
       "Say whether the problem is outdoors or indoors, then choose the problem type.", "Optionally add a photo, tags, and a description.",
       "Choose how to receive updates and whether DC Water may make contact.", "Review, submit, and receive a ticket number.",
       "Track the ticket, rate the experience, and leave feedback."],
      [("rap-02", "Location"), ("rap-07", "Review"), ("rap-08", "Submitted")], RAP_ALL)}
{flow("flow-cs", "Customer Service Form", "Designed in Sprint 4", "cs-01",
      ["Select a topic: Billing Inquiry, Damage, or Other.", "Describe the request, add a location, tags, and an optional file.",
       "Optionally provide contact information for a reply.", "Review and submit."],
      [("cs-04", "Details"), ("cs-06", "Review"), ("cs-07", "Submitted")], CS_ALL)}
{flow("flow-ir", "Image Recognition", "Concept · prototype only", "ir-01",
      ["Choose “Show Us The Issue.”", "Take a photo, choose one from the library, or switch to the form.",
       "The object is outlined, labelled, and described. Unrecognized images prompt a retake.",
       "Review pre-filled details, edit the location, add photos or tags, and submit.", "Track the report later by uploading the original photo."],
      [("ir-06", "Recognized"), ("ir-07", "Details"), ("ir-15", "Track")], IR_ALL, concept=True)}
</div></section>'''

REFL = [
 ("Seeing the design become a usable product is rewarding",
  ["This project challenged me intellectually and creatively and pushed me to use my analytical skills in every sprint. Before it, I had very little experience working with an external client and translating their business needs into a usable product that also met users' expectations.",
   "The most rewarding part is that, with the help of developers, our designs will become a live product on DC Water's website for anyone who lives in or visits the District of Columbia. I enjoyed learning strategies for a successful hand-off to developers, but I wish we'd explored this area more. I would have liked more engagement with the client team across iterations, and in particular, it would have helped to know the financial possibilities and constraints while designing."]),
 ("Being adaptable and flexible is a must",
  ["Because I joined after Sprint 2 ended, I wasn't part of the client kick-off meeting or the expert interviews. Information from those meetings would have given me a deeper understanding of the business need and problem area.",
   "But this is how work happens outside the classroom: UX teams must be adaptable and flexible as client and user needs change and new trends emerge. I'm grateful to the team members from earlier sprints for providing context and bringing me up to speed."]),
 ("Teamwork wins",
  ["I learned to collaborate more effectively with a team. In my professional career I've mostly been responsible for coming up with creative, technology-based solutions. Working with this team challenged me to be open-minded and sometimes consider the big picture instead of every detail.",
   "The team's size was challenging at times: there were many different opinions, sometimes conflicting, which left us short on time. I'm very appreciative of everyone's diverse experiences, skills, and strengths, and proud of the work we all contributed to deliver a great product to our client."]),
]
pages = "".join(
    f'<div class="dcw-nb-page" data-nb-page="{i}"><div class="dcw-nb-front"><div class="dcw-nb-label">Reflection {i:02d}</div>'
    f'<h4 class="dcw-nb-title">{t}</h4>' + "".join(f'<p class="dcw-nb-p">{p}</p>' for p in ps) +
    f'<div class="dcw-nb-num">{i} / 3</div><div class="dcw-nb-corner"></div></div></div>'
    for i, (t, ps) in enumerate(REFL, 1))

def status(h, items, mod):
    return (f'<div class="dcw-status{(" " + mod) if mod else ""}"><div class="dcw-status-h">{h}</div><ul class="dcw-ul">'
            + "".join(f'<li class="dcw-li is-sm">{x}</li>' for x in items) + "</ul></div>")

S["outcomes"] = f'''<section class="dcw-section is-quiet" id="outcomes"><div class="dcw-wrap">
{head("07", "Outcomes, limitations, and reflection", "What was designed, tested, delivered, and left as a recommendation")}
<div class="dcw-status-grid">
{status("Designed", ["Report a Problem form: research-based IA and two iterations", "New Customer Service form", "Image recognition concept: two iterations"], "")}
{status("Tested (prototypes)", ["Report a Problem iteration 1: usability testing, average confidence 4.6 / 5", "Image recognition iteration 1: A/B testing with 6 participants; 6 of 6 preferred it over the form", "Participants came from the team's personal network"], "is-tested")}
{status("Delivered", ["Sprint 4 goals included handing deliverables off to developers and collaborating with them regularly", "Project status: development in progress"], "is-delivered")}
{status("Concept / recommendation", ["Image recognition (not implemented)", "Explore a public kiosk", "Consider an app for customers with online accounts"], "is-concept")}
</div>
<div class="dcw-block"><div class="dcw-split">
<div class="dcw-col"><h3 class="dcw-h3">Limitations and future recommendations</h3><p class="dcw-p">Constraints that shaped the research and design, and where I'd take the work next.</p></div>
{numbered([("Research participants weren't DC Water's target users", "Anyone can use the Report a Problem form, but we didn't have access to target users who live in DC and, ideally, have reported a problem to DC Water before, and the client couldn't provide them. The participants in user testing and research came from the team's personal network. We did, however, have access to previously submitted reports, which we used to create user scenarios and the content for the card sorting activity."),
           ("A responsive web form instead of an app", "After consulting with the client, the team designed a responsive web form instead of a mobile app, assuming that most people who come across an outdoor issue once won't be invested enough to download an app just to report it. However, this design doesn't address DC Water customers with online accounts, who might be more invested and more willing to use an app for easy access."),
           ("Tracking depends on the original photo", "The image recognition design needs the original photo to track a report. If the user loses the photo, they have no way to track their report."),
           ("People without mobile devices", "Accessibility and inclusion are very important to me, and I try to build them into my work. When considering who the product might exclude, I thought about people experiencing homelessness. They may encounter outdoor issues that affect them but likely don't have mobile devices to report a problem. I think a public kiosk should be explored as an alternative because it isn't individually owned.")])}
</div></div>
<div class="dcw-block"><div class="dcw-reflect">
<div class="dcw-col"><h3 class="dcw-h3">Reflection</h3><p class="dcw-p">Three lessons from the project, one per page. Use the arrows, the page tabs, or your keyboard's arrow keys to turn the page.</p></div>
<div class="dcw-notebook" data-notebook="" role="region" aria-label="Reflections">
<div class="dcw-nb-spiral"></div>
<div class="dcw-nb-pages" tabindex="0">{pages}</div>
<div class="dcw-nb-controls">
<a class="dcw-nb-btn" href="#" data-nb-prev="" aria-label="Previous page">←</a>
<a class="dcw-nb-tab" href="#" data-nb-go="0" aria-label="Page 1">1</a><a class="dcw-nb-tab" href="#" data-nb-go="1" aria-label="Page 2">2</a><a class="dcw-nb-tab" href="#" data-nb-go="2" aria-label="Page 3">3</a>
<a class="dcw-nb-btn" href="#" data-nb-next="" aria-label="Next page">→</a>
</div><div class="dcw-sr" aria-live="polite" data-nb-status=""></div>
</div></div></div>
</div></section>'''

S["closing"] = '''<section class="dcw-section is-closing"><div class="dcw-wrap"><div class="dcw-closing">
<a class="dcw-back" href="/" data-back-link="">← Back to projects</a>
<div class="dcw-closing-note">DC Water · HCIM Capstone Project · 2022</div>
</div></div></section>'''


# ---------------------------------------------------------------- CSS
TEAL, TEAL_S, TINT, MINT, DEEP = "#0f6e68", "#0a524e", "#e3f2ef", "#eef7f5", "#062b2a"
INK, INK2, INK3, LINE = "#111111", "#3d3d3d", "#5f5f5f", "#e2e2e2"
LT, LT2, LT3, LTEAL = "#ffffff", "rgba(255,255,255,0.86)", "rgba(255,255,255,0.72)", "#6fd9cb"
GRAD = "linear-gradient(160deg, #e3f2ef, #d2ebe5)"
SHADOW = "0 1px 2px rgba(6,43,42,0.05), 0 12px 28px -18px rgba(6,43,42,0.35)"

BASE = f"""
.dcw-page {{ font-family: Inter, sans-serif; color: {INK2}; font-size: 17px; line-height: 1.65; background-color: #ffffff; }}
.dcw-wrap {{ max-width: 1200px; margin-left: auto; margin-right: auto; padding-left: 40px; padding-right: 40px; position: relative; }}
.dcw-section {{ padding-top: clamp(64px, 9vw, 128px); padding-bottom: clamp(64px, 9vw, 128px); position: relative; background-color: #ffffff; }}
.dcw-section.is-tint {{ background-color: {MINT}; }}
.dcw-section.is-quiet {{ background-color: #f6f6f5; }}
.dcw-section.is-dark {{ background-color: #0a1c1c; color: {LT2}; }}
.dcw-section.is-hero {{ overflow: hidden; color: {LT2}; background-image: radial-gradient(1200px 600px at 85% 20%, rgba(47,179,163,0.32), transparent 60%), radial-gradient(800px 500px at 0% 100%, rgba(15,110,104,0.35), transparent 60%), linear-gradient(160deg, #041d1c 0%, #062b2a 45%, #0b4643 100%); }}
.dcw-section.is-closing {{ padding-top: 72px; padding-bottom: 72px; background-image: linear-gradient(160deg, #041d1c 0%, #062b2a 45%, #0b4643 100%); }}
.dcw-block {{ margin-top: clamp(48px, 6vw, 88px); }}
.dcw-col {{ display: flex; flex-direction: column; align-items: flex-start; }}
.dcw-split {{ display: grid; grid-template-columns: 5fr 7fr; grid-column-gap: clamp(28px, 5vw, 72px); grid-row-gap: 32px; align-items: start; }}
.dcw-split.is-even {{ grid-template-columns: 1fr 1fr; align-items: end; margin-bottom: 8px; }}
.dcw-split.is-reverse {{ grid-template-columns: 7fr 5fr; align-items: center; }}
.dcw-split.is-center {{ align-items: center; }}
.dcw-grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; grid-column-gap: 48px; grid-row-gap: 40px; }}
.dcw-head {{ max-width: 760px; margin-bottom: clamp(32px, 5vw, 56px); }}
.dcw-eyebrow {{ display: flex; align-items: center; grid-column-gap: 10px; margin-bottom: 16px; color: {TEAL}; font-size: 13px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; }}
.dcw-eyebrow.is-on-dark {{ color: {LTEAL}; }}
.dcw-eyebrow-num {{ display: flex; justify-content: center; align-items: center; min-width: 28px; height: 28px; padding-left: 6px; padding-right: 6px; border-radius: 999px; background-color: {TEAL}; color: #ffffff; font-size: 12px; font-weight: 700; letter-spacing: 0; }}
.dcw-eyebrow-num.is-on-dark {{ background-color: {LTEAL}; color: {DEEP}; }}
.dcw-h1 {{ margin-top: 0; margin-bottom: 20px; font-family: Poppins, sans-serif; color: #ffffff; font-size: clamp(52px, 9vw, 112px); line-height: 1; font-weight: 700; letter-spacing: -0.03em; }}
.dcw-h2 {{ margin-top: 0; margin-bottom: 0; font-family: Poppins, sans-serif; color: {INK}; font-size: clamp(30px, 3.6vw, 44px); line-height: 1.15; font-weight: 600; letter-spacing: -0.02em; }}
.dcw-h2.is-on-dark {{ color: #ffffff; }}
.dcw-h2-bar {{ width: 56px; height: 4px; margin-top: 18px; border-radius: 4px; background-image: linear-gradient(90deg, {TEAL}, #2fb3a6); }}
.dcw-h3 {{ margin-top: 0; margin-bottom: 12px; font-family: Inter, sans-serif; color: {INK}; font-size: clamp(20px, 2vw, 24px); line-height: 1.25; font-weight: 600; letter-spacing: -0.01em; }}
.dcw-h3.is-on-dark {{ color: #ffffff; margin-bottom: 0; font-size: clamp(22px, 2.4vw, 30px); }}
.dcw-h4 {{ margin-top: 0; margin-bottom: 12px; font-family: Inter, sans-serif; color: {INK}; font-size: 18px; line-height: 1.3; font-weight: 600; letter-spacing: 0; }}
.dcw-lede {{ margin-top: 20px; margin-bottom: 0; color: {INK2}; font-size: clamp(18px, 1.6vw, 21px); line-height: 1.55; }}
.dcw-lede.is-on-dark {{ color: {LT2}; }}
.dcw-p {{ margin-top: 0; margin-bottom: 16px; color: {INK2}; font-size: 17px; line-height: 1.65; letter-spacing: 0; }}
.dcw-p.is-on-dark {{ color: {LT2}; max-width: 54ch; }}
.dcw-p.is-sm {{ font-size: 15px; line-height: 1.6; margin-bottom: 0; }}
.dcw-p.is-measure {{ max-width: 66ch; }}
.dcw-p.is-spaced {{ margin-top: 16px; }}
.dcw-strong {{ color: {INK}; font-weight: 600; }}
.dcw-kicker {{ margin-bottom: 8px; color: {INK3}; font-size: 13px; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; }}
.dcw-kicker.is-spaced {{ margin-top: 28px; }}
.dcw-tag {{ display: inline-block; margin-bottom: 14px; padding: 4px 12px; border-radius: 999px; background-color: {TINT}; color: {TEAL_S}; font-size: 12px; font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase; }}
.dcw-caption {{ margin-top: 14px; margin-bottom: 0; color: {INK3}; font-size: 14px; line-height: 1.5; }}
.dcw-ul {{ margin-top: 0; margin-bottom: 0; padding-left: 20px; }}
.dcw-li {{ margin-bottom: 6px; color: {INK2}; font-size: 16px; line-height: 1.55; }}
.dcw-li.is-sm {{ font-size: 14.5px; }}
.dcw-chip {{ display: inline-flex; align-items: center; grid-column-gap: 7px; padding: 5px 13px 5px 10px; border: 1px solid rgba(15,110,104,0.28); border-radius: 999px; background-color: {TINT}; color: {TEAL_S}; font-size: 13px; font-weight: 600; line-height: 1.3; }}
.dcw-chip.is-on-dark {{ margin-bottom: 9px; border-color: rgba(111,217,203,0.3); background-color: rgba(111,217,203,0.14); color: #9be7dc; }}
.dcw-chip-dot {{ width: 6px; height: 6px; flex: none; border-radius: 50%; background-color: #2fb3a6; box-shadow: 0 0 0 3px rgba(47,179,163,0.22); }}
.dcw-pills {{ display: flex; flex-wrap: wrap; grid-column-gap: 8px; grid-row-gap: 8px; }}
.dcw-btn {{ display: inline-flex; align-items: center; padding: 12px 18px; border: 1px solid {TEAL}; border-radius: 8px; background-color: {TEAL}; color: #ffffff; font-size: 15px; font-weight: 600; line-height: 1; text-decoration: none; transition: background-color 200ms ease; }}
.dcw-btn:hover {{ background-color: {TEAL_S}; border-color: {TEAL_S}; }}
.dcw-btn.is-hero {{ padding: 15px 24px; border-radius: 999px; border-color: {LTEAL}; background-color: {LTEAL}; color: {DEEP}; font-size: 16px; box-shadow: 0 10px 28px -10px rgba(111,217,203,0.55); }}
.dcw-btn.is-ghost-dark {{ border-color: rgba(255,255,255,0.3); background-color: transparent; color: #ffffff; }}
.dcw-badge {{ display: inline-block; padding: 4px 10px; border: 1px solid {TEAL_S}; border-radius: 999px; color: {TEAL_S}; font-size: 11px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; white-space: nowrap; }}
.dcw-badge.is-on-dark {{ border-color: {LTEAL}; color: {LTEAL}; }}
.dcw-badge.is-muted-dark {{ border-color: rgba(255,255,255,0.3); color: {LT3}; white-space: normal; }}

.dcw-hero-dots {{ position: absolute; left: 0; top: 0; right: 0; bottom: 0; background-image: radial-gradient(rgba(255,255,255,0.09) 1px, transparent 1.2px); background-size: 22px 22px; }}
.dcw-hero-grid {{ display: grid; grid-template-columns: 7fr 5fr; grid-column-gap: clamp(40px, 6vw, 96px); align-items: center; }}
.dcw-hero-copy {{ position: relative; }}
.dcw-hero-tagline {{ max-width: 30ch; margin-top: 0; margin-bottom: 16px; color: #ffffff; font-size: clamp(20px, 2.2vw, 28px); line-height: 1.35; }}
.dcw-hero-actions {{ margin-top: 12px; margin-bottom: 32px; }}
.dcw-facts {{ display: grid; grid-template-columns: repeat(4, 1fr); grid-column-gap: 12px; grid-row-gap: 12px; }}
.dcw-fact {{ padding: 14px 16px; border: 1px solid rgba(255,255,255,0.12); border-radius: 12px; background-color: rgba(255,255,255,0.06); }}
.dcw-fact-v {{ color: #ffffff; font-size: 15px; line-height: 1.45; }}
.dcw-hero-visual {{ position: relative; display: flex; justify-content: center; align-items: center; }}
.dcw-hero-halo {{ position: absolute; width: 120%; aspect-ratio: 1; border-radius: 50%; background-image: radial-gradient(circle, rgba(111,217,203,0.35) 0%, rgba(111,217,203,0.08) 40%, transparent 68%); }}

.dcw-mock {{ position: relative; width: 100%; }}
.dcw-mock.is-hero {{ max-width: 300px; z-index: 1; }}
.dcw-mock.is-pv {{ max-width: 250px; }}
.dcw-mock.is-poster {{ max-width: 250px; }}
.dcw-mock-body {{ position: relative; padding: {V["pad"]}; border: 1.5px solid {V["rim"]}; border-radius: {V["rad"]}; background-color: {V["body"]}; box-shadow: 0 2px 4px rgba(0,0,0,0.14), 0 30px 60px -22px rgba(6,43,42,0.55); }}
.dcw-mock-screen {{ display: block; width: 100%; aspect-ratio: 9 / 19.5; object-fit: cover; object-position: 50% 0%; border-radius: {V["srad"]}; }}
.dcw-mock-island {{ position: absolute; left: 50%; top: 18px; z-index: 2; width: 30%; height: {V["island"]}; border-radius: 999px; background-color: #000000; transform: translate(-50%, 0px); }}
.dcw-mock-btn {{ position: absolute; right: -3px; top: 25%; width: {V["btn"]}; height: 14%; border-radius: 0 3px 3px 0; background-color: #4a4f53; }}
.dcw-mock-btn-l {{ position: absolute; left: -3px; top: 20%; width: {V["btn"]}; height: 9%; border-radius: 3px 0 0 3px; background-color: #4a4f53; }}
.dcw-fig {{ display: flex; flex-direction: column; min-width: 0; }}
.dcw-fig-cap {{ margin-top: 14px; }}
.dcw-fig-num {{ margin-bottom: 3px; color: {INK3}; font-family: Inconsolata, monospace; font-size: 12px; }}
.dcw-fig-num.is-teal {{ color: {TEAL}; }}
.dcw-fig-title {{ margin-bottom: 3px; color: {INK}; font-size: 15px; font-weight: 600; line-height: 1.35; }}
.dcw-fig-title.is-on-dark {{ margin-top: 12px; color: #ffffff; }}
.dcw-fig-text {{ margin-top: 10px; margin-bottom: 0; color: {INK3}; font-size: 14px; line-height: 1.5; }}
.dcw-fig-text.is-xs {{ font-size: 12.5px; }}
.dcw-fig-text.is-on-dark {{ color: {LT3}; }}
.dcw-screens {{ display: grid; grid-template-columns: repeat(4, 1fr); grid-column-gap: clamp(16px, 2.5vw, 32px); grid-row-gap: 32px; margin-top: 28px; }}
.dcw-screens.is-5 {{ grid-template-columns: repeat(5, 1fr); }}
.dcw-screens.is-3 {{ grid-template-columns: repeat(3, 1fr); margin-top: 8px; }}
.dcw-strip-wrap {{ margin-top: 32px; padding-top: 18px; border-top: 1px solid {LINE}; }}
.dcw-strip-label {{ margin-bottom: 14px; color: {INK}; font-size: 15px; font-weight: 600; }}
.dcw-strip-label.is-on-dark {{ color: #ffffff; }}
.dcw-strip-hint {{ margin-left: 8px; color: {INK3}; font-size: 13px; font-weight: 400; }}
.dcw-strip-hint.is-on-dark {{ color: {LT3}; }}
.dcw-strip {{ display: flex; grid-column-gap: 18px; overflow-x: auto; padding-bottom: 14px; scroll-snap-type: x mandatory; }}
.dcw-strip-item {{ flex: 0 0 150px; scroll-snap-align: start; }}
.dcw-artifact {{ padding: clamp(16px, 2.5vw, 28px); border: 1px solid {LINE}; border-radius: 16px; background-color: #ffffff; }}
.dcw-board-img {{ display: block; width: 100%; aspect-ratio: 16 / 10; object-fit: cover; border-radius: 8px; }}
.dcw-sketch {{ max-width: 420px; padding: clamp(16px, 2.5vw, 28px); border: 1px solid {LINE}; border-radius: 16px; background-color: #ffffff; }}
.dcw-sketch-img {{ display: block; width: 100%; aspect-ratio: 4 / 5; object-fit: cover; border-radius: 8px; }}

.dcw-statement {{ margin-top: 0; margin-bottom: 24px; padding-left: 20px; border-left: 4px solid {TEAL}; color: {INK}; font-size: clamp(20px, 2.2vw, 26px); line-height: 1.4; }}
.dcw-meta {{ display: flex; flex-direction: column; }}
.dcw-meta-row {{ display: grid; grid-template-columns: 150px 1fr; grid-column-gap: 12px; padding-top: 16px; padding-bottom: 16px; border-bottom: 1px solid {LINE}; }}
.dcw-meta-k {{ padding-top: 2px; color: {INK3}; font-size: 13px; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; }}
.dcw-meta-v {{ color: {INK}; font-size: 16px; }}
.dcw-role-cols {{ display: grid; grid-template-columns: 1fr 1fr; grid-column-gap: 32px; grid-row-gap: 24px; margin-top: 24px; }}
.dcw-who-card {{ position: relative; overflow: hidden; padding: clamp(24px, 3vw, 36px); border-radius: 20px; }}
.dcw-who-card.is-mine {{ background-color: {TEAL}; background-image: radial-gradient(circle at 100% 0%, rgba(111,217,203,0.35), transparent 50%), linear-gradient(150deg, #0f6e68, #084844); box-shadow: 0 26px 50px -26px rgba(6,43,42,0.65); color: #ffffff; }}
.dcw-who-card.is-team {{ border: 1px solid {LINE}; background-color: #ffffff; background-image: radial-gradient(circle, rgba(15,110,104,0.09) 1px, transparent 1.5px); background-size: 18px 18px; box-shadow: 0 18px 40px -30px rgba(0,0,0,0.35); }}
.dcw-role-head {{ margin-bottom: 22px; padding-bottom: 18px; border-bottom: 1px solid rgba(15,110,104,0.18); }}
.dcw-role-kicker {{ margin-bottom: 6px; color: {TEAL}; font-size: 12px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; }}
.dcw-role-kicker.is-mine {{ color: {LTEAL}; }}
.dcw-role-title {{ margin-top: 0; margin-bottom: 0; color: {INK}; font-size: clamp(22px, 2.2vw, 26px); font-weight: 700; line-height: 1.2; }}
.dcw-role-title.is-mine {{ color: #ffffff; }}
.dcw-team-dots {{ display: flex; grid-column-gap: 6px; margin-top: 14px; }}
.dcw-team-dot {{ width: 22px; height: 22px; border: 2px solid #ffffff; border-radius: 50%; background-color: #cfe6e2; box-shadow: 0 0 0 1px #b9ddd6; }}
.dcw-team-dot.is-me {{ background-color: {TEAL}; box-shadow: 0 0 0 1px {TEAL}; }}
.dcw-role-list {{ display: flex; flex-direction: column; grid-row-gap: 14px; margin-top: 0; margin-bottom: 0; padding-left: 0; list-style-type: none; }}
.dcw-role-item {{ display: flex; align-items: flex-start; grid-column-gap: 14px; }}
.dcw-role-n {{ flex: none; display: flex; justify-content: center; align-items: center; width: 34px; height: 34px; border: 1.5px solid {TEAL}; border-radius: 10px; background-color: #ffffff; color: {TEAL}; font-size: 13px; font-weight: 700; }}
.dcw-role-n.is-mine {{ border-color: transparent; background-color: rgba(255,255,255,0.14); color: #ffffff; }}
.dcw-role-text {{ padding-top: 5px; color: {INK2}; font-size: 15.5px; line-height: 1.55; }}
.dcw-role-text.is-mine {{ color: rgba(255,255,255,0.92); }}
.dcw-timeline {{ display: grid; grid-template-columns: repeat(5, 1fr); grid-column-gap: 8px; padding-top: 12px; }}
.dcw-tl {{ position: relative; padding: 14px 14px 16px; border-radius: 10px; background-color: #f6f6f5; }}
.dcw-tl.is-mine {{ background-image: {GRAD}; }}
.dcw-tl.is-lead {{ background-image: linear-gradient(160deg, {TEAL}, {TEAL_S}); }}
.dcw-tl-h {{ color: {INK3}; font-size: 15px; font-weight: 600; }}
.dcw-tl-h.is-mine {{ color: {TEAL_S}; }}
.dcw-tl-h.is-lead {{ color: #ffffff; }}
.dcw-tl-t {{ color: {INK3}; font-size: 13.5px; line-height: 1.4; }}
.dcw-tl-t.is-mine {{ color: {INK2}; }}
.dcw-tl-t.is-lead {{ color: rgba(255,255,255,0.88); }}
.dcw-tl-join {{ position: absolute; left: 12px; top: -10px; padding: 2px 8px; border-radius: 999px; background-color: {TEAL}; color: #ffffff; font-size: 11px; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; }}

.dcw-preview {{ display: grid; grid-template-columns: repeat(3, 1fr); grid-column-gap: clamp(24px, 4vw, 56px); grid-row-gap: 48px; }}
.dcw-pv {{ display: flex; flex-direction: column; align-items: center; }}
.dcw-pv-cap {{ width: 100%; max-width: 300px; margin-top: 16px; }}
.dcw-pv-step {{ margin-bottom: 4px; color: {TEAL}; font-family: Inconsolata, monospace; font-size: 13px; }}

.dcw-numbered {{ display: flex; flex-direction: column; }}
.dcw-num-item {{ display: flex; grid-column-gap: 22px; padding-top: 20px; padding-bottom: 20px; border-top: 1px solid {LINE}; }}
.dcw-num-n {{ flex: none; width: 28px; padding-top: 2px; color: {TEAL}; font-family: Inconsolata, monospace; font-size: 14px; }}
.dcw-num-h {{ margin-top: 0; margin-bottom: 6px; color: {INK}; font-size: 17px; font-weight: 600; line-height: 1.35; }}
.dcw-goals {{ display: grid; grid-template-columns: repeat(4, 1fr); grid-column-gap: 14px; grid-row-gap: 14px; margin-top: 20px; }}
.dcw-goal {{ display: flex; flex-direction: column; grid-row-gap: 14px; padding: 20px 20px 18px; border: 1px solid {LINE}; border-radius: 14px; background-color: #ffffff; box-shadow: {SHADOW}; }}
.dcw-goal-num {{ padding-bottom: 12px; border-bottom: 1px solid {LINE}; color: {TEAL}; font-family: Inconsolata, monospace; font-size: 13px; font-weight: 700; }}
.dcw-goal-text {{ flex: 1; color: {INK}; font-size: 16px; font-weight: 600; line-height: 1.45; }}
.dcw-goal-link {{ color: {TEAL}; font-size: 14px; font-weight: 600; text-decoration: none; }}
.dcw-stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(110px, 1fr)); grid-column-gap: 16px; grid-row-gap: 16px; width: 100%; margin-top: 20px; }}
.dcw-stat {{ padding-top: 14px; border-top: 3px solid {TEAL}; }}
.dcw-stat-n {{ color: {TEAL}; font-family: Poppins, sans-serif; font-size: clamp(32px, 3.6vw, 44px); font-weight: 700; line-height: 1.05; white-space: nowrap; }}
.dcw-stat-l {{ margin-top: 4px; color: {INK3}; font-size: 14px; }}
.dcw-words {{ display: flex; flex-wrap: wrap; grid-column-gap: 6px; grid-row-gap: 6px; }}
.dcw-word {{ padding: 3px 9px; border: 1px solid #c9c9c9; border-radius: 4px; background-color: #fff8c9; color: {INK2}; font-size: 13px; }}
.dcw-word.is-illegible {{ border-style: dashed; background-color: #ffffff; color: {INK3}; font-style: italic; }}
.dcw-findings {{ display: flex; flex-direction: column; margin-top: 16px; }}
.dcw-finding {{ display: grid; grid-template-columns: 1fr 1fr; grid-column-gap: 40px; grid-row-gap: 8px; padding-top: 22px; padding-bottom: 22px; border-top: 1px solid {LINE}; }}
.dcw-finding-what {{ position: relative; padding-left: 20px; color: {INK}; font-size: 17px; font-weight: 600; line-height: 1.45; }}
.dcw-finding-dot {{ position: absolute; left: 0; top: 9px; width: 8px; height: 8px; border-radius: 50%; background-color: {TEAL}; }}
.dcw-finding-so {{ color: {INK2}; font-size: 15px; line-height: 1.55; }}
.dcw-finding-k {{ margin-bottom: 4px; color: {TEAL}; font-size: 11px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; }}
.dcw-ia {{ display: grid; grid-template-columns: repeat(3, 1fr); grid-column-gap: 16px; grid-row-gap: 16px; margin-bottom: 12px; }}
.dcw-ia-col {{ padding: 16px; border: 1px solid {LINE}; border-radius: 12px; background-color: #ffffff; }}
.dcw-ia-root {{ margin-bottom: 10px; padding-bottom: 10px; border-bottom: 3px solid {TEAL}; color: {INK}; font-weight: 700; }}
.dcw-ia-item {{ padding: 6px 0 6px 14px; border-left: 1px solid #c9c9c9; color: {INK2}; font-size: 15px; }}
.dcw-ia-empty {{ color: {INK3}; font-size: 14px; }}

.dcw-results {{ display: grid; grid-template-columns: 1fr 1fr; grid-column-gap: clamp(20px, 3vw, 32px); grid-row-gap: 20px; margin-top: 20px; }}
.dcw-rc {{ position: relative; overflow: hidden; padding: clamp(24px, 3vw, 36px); border-radius: 20px; }}
.dcw-rc.is-wins {{ background-color: {DEEP}; background-image: radial-gradient(circle at 100% 0%, rgba(111,217,203,0.28), transparent 55%), linear-gradient(160deg, #0a3b39, #041d1c); box-shadow: 0 26px 50px -26px rgba(6,43,42,0.7); }}
.dcw-rc.is-opps {{ border: 1.5px dashed #9cc9c2; background-color: #ffffff; background-image: repeating-linear-gradient(135deg, rgba(15,110,104,0.045) 0px, rgba(15,110,104,0.045) 2px, transparent 2px, transparent 12px); }}
.dcw-rc-head {{ display: flex; align-items: center; grid-column-gap: 14px; margin-bottom: 20px; padding-bottom: 18px; border-bottom: 1px solid {LINE}; }}
.dcw-rc-head.is-wins {{ border-bottom-color: rgba(255,255,255,0.14); }}
.dcw-rc-icon {{ flex: none; display: flex; justify-content: center; align-items: center; width: 48px; height: 48px; border-radius: 14px; font-size: 22px; font-weight: 700; }}
.dcw-rc-icon.is-wins {{ background-color: {LTEAL}; color: {DEEP}; }}
.dcw-rc-icon.is-opps {{ border: 1px solid #b9ddd6; background-color: {TINT}; color: {TEAL_S}; }}
.dcw-rc-titles {{ flex: 1; }}
.dcw-rc-kicker {{ color: {TEAL}; font-size: 12px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; }}
.dcw-rc-kicker.is-wins {{ color: {LTEAL}; }}
.dcw-rc-title {{ margin-top: 2px; margin-bottom: 0; color: {INK}; font-size: 24px; font-weight: 700; line-height: 1.2; }}
.dcw-rc-title.is-wins {{ color: #ffffff; }}
.dcw-rc-count {{ color: rgba(15,110,104,0.28); font-size: 44px; font-weight: 700; line-height: 1; }}
.dcw-rc-count.is-wins {{ color: rgba(111,217,203,0.35); }}
.dcw-rc-list {{ display: flex; flex-direction: column; grid-row-gap: 10px; margin-top: 0; margin-bottom: 0; padding-left: 0; list-style-type: none; }}
.dcw-rc-item {{ display: flex; align-items: flex-start; grid-column-gap: 12px; padding: 12px 14px; border-radius: 12px; }}
.dcw-rc-item.is-wins {{ border: 1px solid rgba(255,255,255,0.08); background-color: rgba(255,255,255,0.06); }}
.dcw-rc-item.is-opps {{ border: 1px solid {LINE}; background-color: #ffffff; }}
.dcw-rc-mark {{ flex: none; display: flex; justify-content: center; align-items: center; width: 24px; height: 24px; margin-top: 1px; border-radius: 50%; font-size: 13px; font-weight: 700; }}
.dcw-rc-mark.is-wins {{ background-color: {LTEAL}; color: {DEEP}; }}
.dcw-rc-mark.is-opps {{ border: 1.5px solid {TEAL}; background-color: #ffffff; color: {TEAL}; }}
.dcw-rc-text {{ font-size: 15px; line-height: 1.55; }}
.dcw-rc-text.is-wins {{ color: rgba(255,255,255,0.9); }}
.dcw-rc-text.is-opps {{ color: {INK2}; }}
.dcw-callout {{ display: flex; align-items: center; grid-column-gap: 12px; margin-top: 18px; padding: 12px 16px; border-radius: 12px; background-color: {DEEP}; }}
.dcw-callout-num {{ flex: none; color: {LTEAL}; font-size: 24px; font-weight: 700; white-space: nowrap; }}
.dcw-callout-text {{ color: rgba(255,255,255,0.85); font-size: 15px; line-height: 1.4; }}
.dcw-callout.is-light {{ margin-top: 20px; background-color: {LTEAL}; }}
.dcw-callout-num.is-light {{ color: {DEEP}; }}
.dcw-callout-text.is-light {{ color: {DEEP}; }}
.dcw-strip.is-scroll {{ grid-auto-flow: column; grid-auto-columns: clamp(200px, 24vw, 260px); grid-template-columns: none; grid-template-rows: auto; overflow-x: auto; padding-bottom: 16px; }}
.dcw-screens.is-scroll {{ grid-auto-flow: column; grid-auto-columns: clamp(200px, 24vw, 260px); grid-template-columns: none; grid-template-rows: auto; overflow-x: auto; padding-bottom: 16px; scroll-snap-type: x proximity; }}
.dcw-wf {{ display: grid; grid-template-columns: 5fr 7fr; grid-column-gap: clamp(28px, 5vw, 64px); grid-row-gap: 28px; align-items: center; }}
.dcw-wf-list {{ display: flex; flex-direction: column; grid-row-gap: 8px; margin-top: 18px; margin-bottom: 0; padding-left: 0; list-style-type: none; }}
.dcw-wf-item {{ display: flex; align-items: center; grid-column-gap: 12px; padding: 10px 14px; border: 1px solid {LINE}; border-radius: 10px; background-color: #ffffff; color: {INK}; font-size: 15px; font-weight: 500; }}
.dcw-wf-n {{ flex: none; color: {TEAL}; font-size: 13px; font-weight: 700; }}
.dcw-wf-frame {{ position: relative; padding: clamp(16px, 2.5vw, 28px); border: 1px solid {LINE}; border-radius: 16px; background-color: #ffffff; }}
.dcw-wf-img {{ display: block; width: 100%; aspect-ratio: 16 / 10; object-fit: cover; border-radius: 8px; }}

.dcw-decision {{ display: grid; grid-template-columns: 5fr 6fr; grid-column-gap: clamp(28px, 5vw, 72px); grid-row-gap: 28px; margin-top: clamp(40px, 5vw, 64px); padding-top: clamp(40px, 5vw, 64px); border-top: 1px solid {LINE}; }}
.dcw-decision-title {{ margin-top: 0; margin-bottom: 18px; color: {INK}; font-size: 20px; font-weight: 600; line-height: 1.3; }}
.dcw-decision-title.is-spaced {{ margin-top: clamp(40px, 5vw, 64px); padding-top: clamp(40px, 5vw, 64px); border-top: 1px solid {LINE}; }}
.dcw-chain {{ display: flex; flex-direction: column; }}
.dcw-chain-card {{ padding: 16px 18px; border: 1px solid {LINE}; border-radius: 10px; background-color: #ffffff; }}
.dcw-chain-card.is-changed {{ border-color: transparent; background-image: linear-gradient(160deg, {TEAL}, {TEAL_S}); }}
.dcw-chain-k {{ margin-bottom: 6px; color: {TEAL_S}; font-size: 11px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; }}
.dcw-chain-k.is-changed {{ color: #bff0e8; }}
.dcw-chain-p {{ margin-top: 0; margin-bottom: 0; color: {INK2}; font-size: 15px; line-height: 1.55; }}
.dcw-chain-p.is-changed {{ color: rgba(255,255,255,0.94); }}
.dcw-chain-arrow {{ padding-left: 18px; color: {TEAL}; font-weight: 700; line-height: 26px; }}
.dcw-cmp {{ display: grid; grid-template-columns: repeat(2, minmax(0, 260px)); grid-column-gap: clamp(16px, 3vw, 40px); grid-row-gap: 28px; align-items: start; }}
.dcw-cmp-item {{ display: flex; flex-direction: column; align-items: flex-start; min-width: 0; }}
.dcw-cmp-label {{ margin-bottom: 10px; padding: 2px 0; color: {INK3}; font-size: 12px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; }}
.dcw-cmp-label.is-after {{ padding: 2px 8px; border-radius: 999px; background-color: {TINT}; color: {TEAL}; }}

.dcw-sort {{ display: grid; grid-template-columns: repeat(3, 1fr); grid-column-gap: 12px; grid-row-gap: 12px; margin-bottom: 12px; }}
.dcw-sort-col {{ padding: 14px; border: 1px solid {LINE}; border-radius: 10px; background-color: #ffffff; }}
.dcw-sort-col.is-keep {{ border-color: {TEAL}; background-color: {TINT}; }}
.dcw-sort-h {{ margin-bottom: 8px; color: {INK3}; font-size: 13px; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; }}
.dcw-sort-h.is-keep {{ color: {TEAL_S}; }}
.dcw-sort-item {{ padding-top: 6px; padding-bottom: 6px; border-top: 1px solid {LINE}; color: {INK2}; font-size: 14px; }}

.dcw-notice {{ display: flex; align-items: flex-start; grid-column-gap: 14px; max-width: 760px; padding: 16px 18px; border: 1px solid #c9c9c9; border-left: 4px solid {TEAL}; border-radius: 8px; background-color: #ffffff; }}
.dcw-ideas {{ display: grid; grid-template-columns: 1fr 1fr; grid-column-gap: 10px; grid-row-gap: 10px; width: 100%; }}
.dcw-idea {{ padding: 12px 14px; border: 1px solid {LINE}; border-radius: 10px; background-color: #ffffff; }}
.dcw-idea.is-picked {{ border-color: {TEAL}; background-image: {GRAD}; }}
.dcw-idea-t {{ color: {INK}; font-size: 15px; font-weight: 500; }}
.dcw-idea-s {{ color: {INK3}; font-size: 13px; }}
.dcw-idea-s.is-picked {{ color: {TEAL_S}; }}
.dcw-ab {{ display: grid; grid-template-columns: 1fr 1fr; grid-column-gap: clamp(24px, 4vw, 56px); grid-row-gap: 40px; margin-top: 32px; }}
.dcw-ab-opts {{ display: grid; grid-template-columns: 1fr 1fr; grid-column-gap: clamp(14px, 2vw, 24px); width: 100%; }}

.dcw-flow {{ margin-top: 32px; padding: clamp(24px, 4vw, 48px); border: 1px solid rgba(255,255,255,0.14); border-radius: 18px; background-image: linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02)); }}
.dcw-flow-head {{ display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; grid-column-gap: 24px; grid-row-gap: 10px; margin-bottom: 24px; }}
.dcw-flow-grid {{ display: grid; grid-template-columns: 5fr 7fr; grid-column-gap: clamp(24px, 4vw, 56px); grid-row-gap: 32px; align-items: start; }}
.dcw-proto {{ display: flex; flex-direction: column; align-items: flex-start; grid-row-gap: 14px; }}
.dcw-proto-stage {{ display: flex; justify-content: center; width: 100%; padding: clamp(20px, 3vw, 32px); border: 1px solid rgba(255,255,255,0.14); border-radius: 14px; background-image: radial-gradient(circle at 50% 40%, rgba(111,217,203,0.22), transparent 65%); }}
.dcw-proto-note {{ margin-top: 0; margin-bottom: 0; color: {LT3}; font-size: 13px; }}
.dcw-steps {{ display: flex; flex-direction: column; grid-row-gap: 12px; margin-bottom: 24px; }}
.dcw-step {{ display: flex; align-items: flex-start; grid-column-gap: 12px; }}
.dcw-step-n {{ display: flex; flex: none; justify-content: center; align-items: center; width: 24px; height: 24px; border-radius: 50%; background-color: {LTEAL}; color: {DEEP}; font-size: 12px; font-weight: 700; }}
.dcw-step-t {{ color: {LT2}; font-size: 15px; line-height: 1.5; }}

.dcw-status-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); grid-column-gap: 12px; grid-row-gap: 12px; }}
.dcw-status {{ padding: 20px; border: 1px solid {LINE}; border-top: 4px solid {INK}; border-radius: 12px; background-color: #ffffff; }}
.dcw-status.is-tested {{ border-top-color: {TEAL}; }}
.dcw-status.is-delivered {{ border-top-color: #2fb3a6; }}
.dcw-status.is-concept {{ border-top-style: dashed; border-top-color: {INK3}; }}
.dcw-status-h {{ margin-bottom: 12px; color: {INK}; font-size: 16px; font-weight: 600; }}

.dcw-reflect {{ display: grid; grid-template-columns: 4fr 8fr; grid-column-gap: clamp(28px, 5vw, 72px); grid-row-gap: 28px; align-items: start; }}
.dcw-notebook {{ position: relative; max-width: 680px; padding-top: 22px; }}
.dcw-nb-spiral {{ position: absolute; left: 24px; right: 24px; top: 4px; z-index: 400; height: 36px; background-image: radial-gradient(circle at 50% 70%, #062b2a 0 4px, transparent 4.5px), linear-gradient(90deg, transparent 0 9px, #8f9aa0 9px 11px, #e6ecee 11px 15px, #8f9aa0 15px 17px, transparent 17px); background-size: 30px 36px, 30px 26px; background-position: 0px 0px, 4px 0px; background-repeat: repeat-x, repeat-x; }}
.dcw-nb-pages {{ position: relative; display: flex; flex-direction: column; grid-row-gap: 24px; }}
.dcw-nb-page {{ position: relative; }}
.dcw-nb-front {{ position: relative; height: 100%; padding: 48px 44px 40px 92px; border-radius: 4px 4px 14px 14px; background-color: #fffdf6; background-image: linear-gradient(90deg, transparent 74px, rgba(15,110,104,0.5) 74px 76px, transparent 76px), repeating-linear-gradient(180deg, transparent 0px 31px, #cfe6e2 31px 32px); background-position: 0px 0px, 0px 22px; box-shadow: 0 1px 2px rgba(0,0,0,0.08), 0 24px 40px -18px rgba(6,43,42,0.35); }}
.dcw-nb-label {{ color: {TEAL}; font-size: 12px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; line-height: 32px; }}
.dcw-nb-title {{ margin-top: 0; margin-bottom: 16px; color: #10403d; font-family: Caveat, 'Segoe Print', cursive; font-size: clamp(28px, 3.4vw, 36px); font-weight: 700; line-height: 40px; }}
.dcw-nb-p {{ margin-top: 0; margin-bottom: 32px; color: #26302f; font-size: 16px; line-height: 32px; }}
.dcw-nb-num {{ position: absolute; left: 50%; bottom: 8px; color: #6b7a78; font-family: Caveat, cursive; font-size: 18px; transform: translate(-50%, 0px); }}
.dcw-nb-corner {{ position: absolute; right: 0; bottom: 0; width: 34px; height: 34px; border-radius: 0 0 14px 0; background-image: linear-gradient(315deg, #f6f6f5 0 50%, #e9e3cf 50% 56%, #f7f3e6 56%); }}
.dcw-nb-controls {{ display: flex; justify-content: center; align-items: center; grid-column-gap: 10px; margin-top: 30px; }}
.dcw-nb-btn {{ display: flex; justify-content: center; align-items: center; width: 44px; height: 44px; border: 1px solid #c9c9c9; border-radius: 50%; background-color: #ffffff; color: {INK}; font-size: 18px; text-decoration: none; }}
.dcw-nb-btn:hover {{ border-color: {TEAL}; background-color: {TEAL}; color: #ffffff; }}
.dcw-nb-tab {{ display: flex; justify-content: center; align-items: center; min-width: 36px; height: 36px; border: 1px solid {LINE}; border-radius: 999px; background-color: #ffffff; color: {INK3}; font-size: 14px; font-weight: 600; text-decoration: none; }}
.dcw-sr {{ position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0px, 0px, 0px, 0px); white-space: nowrap; }}

.dcw-closing {{ display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; grid-column-gap: 16px; grid-row-gap: 16px; }}
.dcw-back {{ color: #ffffff; font-size: clamp(20px, 2.4vw, 28px); font-weight: 600; text-decoration: none; }}
.dcw-back:hover {{ color: {LTEAL}; }}
.dcw-closing-note {{ color: {LT3}; font-size: 13px; }}
"""

MED = """
.dcw-screens.is-scroll { grid-template-columns: none; }
.dcw-wf { grid-template-columns: 1fr; }
.dcw-hero-grid { grid-template-columns: 1fr; grid-row-gap: 48px; }
.dcw-split { grid-template-columns: 1fr; }
.dcw-split.is-even { grid-template-columns: 1fr; }
.dcw-split.is-reverse { grid-template-columns: 1fr; }
.dcw-flow-grid { grid-template-columns: 1fr; }
.dcw-decision { grid-template-columns: 1fr; }
.dcw-reflect { grid-template-columns: 1fr; }
.dcw-ab { grid-template-columns: 1fr; }
.dcw-goals { grid-template-columns: repeat(2, 1fr); }
.dcw-status-grid { grid-template-columns: repeat(2, 1fr); }
.dcw-screens { grid-template-columns: repeat(3, 1fr); }
.dcw-screens.is-5 { grid-template-columns: repeat(3, 1fr); }
.dcw-timeline { grid-template-columns: repeat(5, minmax(132px, 1fr)); overflow-x: auto; }
"""
SMALL = """
.dcw-wrap { padding-left: 16px; padding-right: 16px; }
.dcw-page { font-size: 16px; }
.dcw-facts { grid-template-columns: repeat(2, 1fr); }
.dcw-preview { grid-template-columns: 1fr; }
.dcw-mock.is-hero { max-width: 240px; }
.dcw-mock.is-pv { max-width: 230px; }
.dcw-mock.is-poster { max-width: 210px; }
.dcw-role-cols { grid-template-columns: 1fr; }
.dcw-results { grid-template-columns: 1fr; }
.dcw-grid-2 { grid-template-columns: 1fr; }
.dcw-finding { grid-template-columns: 1fr; }
.dcw-ia { grid-template-columns: 1fr; }
.dcw-sort { grid-template-columns: 1fr; }
.dcw-ideas { grid-template-columns: 1fr; }
.dcw-goals { grid-template-columns: 1fr; }
.dcw-status-grid { grid-template-columns: 1fr; }
.dcw-meta-row { grid-template-columns: 1fr; grid-row-gap: 4px; }
.dcw-screens { grid-template-columns: repeat(2, 1fr); }
.dcw-screens.is-5 { grid-template-columns: repeat(2, 1fr); }
.dcw-screens.is-3 { grid-template-columns: repeat(3, 1fr); grid-column-gap: 10px; }
.dcw-cmp { grid-template-columns: repeat(2, 1fr); grid-column-gap: 14px; }
.dcw-flow { padding: 20px 16px; border-radius: 12px; }
.dcw-nb-front { padding: 44px 18px 36px 64px; background-image: linear-gradient(90deg, transparent 50px, rgba(15,110,104,0.5) 50px 52px, transparent 52px), repeating-linear-gradient(180deg, transparent 0px 27px, #cfe6e2 27px 28px); }
.dcw-nb-p { font-size: 15px; line-height: 28px; margin-bottom: 28px; }
.dcw-nb-label { line-height: 28px; }
"""


def parse_rules(css):
    out = []
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", css):
        sel, body = m.group(1).strip(), m.group(2).strip()
        if sel:
            out.append((sel, body))
    return out

RULES = {"base": parse_rules(BASE), "med": parse_rules(MED), "small": parse_rules(SMALL)}
MQ = {"med": "@media screen and (max-width: 991px)", "small": "@media screen and (max-width: 767px)"}

def css_for(html, done=None):
    """CSS rules whose classes all appear in html; skip selectors already sent (done)."""
    classes = set(c for attr in re.findall(r'class="([^"]+)"', html) for c in attr.split())
    def used(sel):
        sel_classes = re.findall(r"\.([\w-]+)", sel.split(":")[0])
        if not sel_classes or not all(c in classes for c in sel_classes):
            return False
        if done is not None and sel in done:
            return False
        return True
    parts = [f"{s} {{ {b} }}" for s, b in RULES["base"] if used(s)]
    for k in ("med", "small"):
        rs = [f"{s} {{ {b} }}" for s, b in RULES[k] if used(s)]
        if rs:
            parts.append(MQ[k] + " { " + " ".join(rs) + " }")
    return "\n".join(parts)

def compact(h):
    return re.sub(r">\s+<", "><", h).strip()

if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    order = ["hero", "overview", "solution", "research", "reporting", "photo", "prototypes", "outcomes", "closing"]
    out = []
    done = set()
    for k in order:
        h = compact(S[k])
        if k == "hero":
            h = '<main class="dcw-page">' + h + "</main>"
        css = css_for(h, done)
        for part in (RULES["base"], RULES["med"], RULES["small"]):
            for sel, _ in part:
                if (sel + " {") in css:
                    done.add(sel)
        out.append({"label": k, "html": h, "css": css})
    json.dump(out, open(os.path.join(HERE, "out/sections.json"), "w"), ensure_ascii=False)
    # standalone preview for checking the look outside Webflow
    page = ('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@600;700&family=Caveat:wght@700&display=swap">'
            '<style>:root{--_dcw-phone-frame---dcw-phone-pad:9px;--_dcw-phone-frame---dcw-phone-radius:40px;--_dcw-phone-frame---dcw-phone-screen-radius:31px;'
            '--_dcw-phone-frame---dcw-phone-island-h:20px;--_dcw-phone-frame---dcw-phone-btn-w:3px;--_dcw-phone-frame---dcw-phone-body:#0b0c0d;--_dcw-phone-frame---dcw-phone-rim:#6d7377}'
            'body{margin:0}*{box-sizing:border-box}' + css_for("".join(o["html"] for o in out)) +
            '</style></head><body>' + out[0]["html"].replace("</main>", "") + "".join(o["html"] for o in out[1:]) + "</main></body></html>")
    open(os.path.join(HERE, "out/check.html"), "w").write(page)
    for o in out:
        print(o["label"], len(o["html"]), len(o["css"]))
