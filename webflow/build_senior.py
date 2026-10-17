"""Generate Webflow-compatible HTML/CSS chunks for the Senior Services case study.

Same approach as build.py (DC Water) and build_grove.py (Grove): flat classes, no
descendant selectors. Shared building blocks reuse the `dcw-` and `gfh-` classes
that already exist on the site, so their CSS is NOT re-sent and nothing shared is
restyled. Everything specific to this page uses `ssv-` classes, and only those
rules are included in the payloads.

Content comes from the original Senior Services portfolio page (PDF export) and
is framed as a University of Maryland HCI course project with proposed designs.
Images are the original team artifacts, cropped from that export and uploaded to
the asset library (sources in webflow/senior-assets/).

Usage: python3 webflow/build_senior.py
  -> webflow/out/senior-sections.json   payloads for the Webflow HTML builder
  -> webflow/out/senior-check.html      standalone preview for checking layouts
"""
import json, os, re, html as H

HERE = os.path.dirname(os.path.abspath(__file__))
CDN = "https://cdn.prod.website-files.com/68caf66283367e4c3b2f3706/"
e = H.escape

# asset id, file, natural size, alt text
A = {
    "wf-landing": ("6ad3cefb7fd6a69c04777173", "ssv-wf-landing.png", (1170, 981),
                   "Wireframe of the proposed Senior ID landing page: quick links including Am I Eligible?, Activity Schedule, Mental Health Support and Senior Ambassadors; a Sign Up button; a Learn More video; and a list of upcoming events and activities."),
    "wf-overview": ("6ad3cefb5ea7d930ca05b8fa", "ssv-wf-overview.jpg", (2940, 2173),
                    "Overview of all nine proposed wireframes arranged in a grid, from the landing page through registration, confirmation, the activity list and login."),
    "wf-demographic": ("6ad3cefb7fd6a69c0477715e", "ssv-wf-demographic.png", (1170, 966),
                       "Wireframe of registration step 1, Demographic Information: fields for first and last name, date of birth, address, city, state, zip code, phone number and email."),
    "wf-activities": ("6ad3cedf01a8c2da92c94ddb", "ssv-wf-activities.png", (1170, 976),
                      "Wireframe of registration step 2, Event and Activities Sign Up: opportunities the person is eligible for, Senior ID, Green Team and Club 300, each with a Sign Up checkbox."),
    "wf-communication": ("6ad3cefb5ea7d930ca05b88e", "ssv-wf-communication.png", (1170, 761),
                         "Wireframe of registration step 3, Communication Preferences: receive information on paper or by email, and notifications about upcoming events, volunteer opportunities and program updates."),
    "wf-review": ("6ad3cefbf0a6fd4b3a70e1f9", "ssv-wf-review.png", (1170, 760),
                  "Wireframe of registration step 4, Review: a summary of demographic information, the activities signed up for and communication preferences."),
    "wf-password": ("6ad3cefbf68b8eb5950b6878", "ssv-wf-password.png", (1170, 690),
                    "Wireframe of registration step 5, Create Password: password and confirm password fields, the password rules, and a Create Account button."),
    "wf-confirmation": ("6ad3cefbf76eadd687b7b080", "ssv-wf-confirmation.png", (1170, 746),
                        "Wireframe of the confirmation page: Congrats, the account has been created; pick up the Senior ID at a rec center; bring or upload proof of residency, age and identity."),
    "wf-activity-list": ("6ad3cedfd9050dcc39687019", "ssv-wf-activity-list.png", (1170, 1009),
                         "Wireframe of the Events and Activities list for returning users: filters for age, location, type and format, and listings such as Computer Skills: Seniors and Aerobics: Seniors, each with Add to Calendar and Sign Up."),
    "wf-login": ("6ad3cefbdf96bdd5bc942ca0", "ssv-wf-login.png", (1170, 658),
                 "Wireframe of the Log in page with a Log in button and a link to sign up for people who don't have an account."),
    "affinity": ("6ad3cede326cff6f74fd0582", "ssv-affinity.jpg", (2940, 274),
                 "The team's affinity diagram: rows of sticky notes from the five interviews grouped under theme headers."),
    "relationship": ("6ad3cedfcafbb31a12cb7d2f", "ssv-relationship.jpg", (2438, 2401),
                     "Relationship model: three nested levels around the senior, Senior Program Activity Buddies, Senior Program Acquaintances and External Activity Influencers, with an arrow showing more to less shared interaction with the Parks and Recreation department."),
    "journey": ("6ad3cedfcafbb31a12cb7d1a", "ssv-journey.jpg", (2438, 2370),
                "Journey map for the persona Active Agatha signing up for an activity online, across four phases: consult friends and family, search online, call the department, and assess the ID program, with thoughts, touchpoints, opportunities and proposed metrics."),
    "identity": ("6ad3cedff0a6fd4b3a70d6e3", "ssv-identity.jpg", (2438, 1410),
                 "Identity model with three groups, I like, I do and I am, each holding traits such as The Outdoors, Social Interaction, Family Time, Morning Activities, Web Searches, In the Dark, An Eager Learner and Proudly Analog."),
    "sketch-isolation": ("6ad3cedfcafbb31a12cb7d44", "ssv-sketch-isolation.jpg", (1480, 775),
                         "Hand-drawn storyboard of a person seeking mental health resources to address social isolation."),
    "sketch-senior-id": ("6ad3cedfcafbb31a12cb7d59", "ssv-sketch-senior-id.jpg", (2460, 1225),
                         "Hand-drawn storyboard of a person learning about the Senior ID card through an ambassador and then signing up, with notes for a landing page, a program sign-up page and a redesigned upcoming events page."),
}

def url(k): return CDN + A[k][0] + "_" + A[k][1]

def img(k, cls="ssv-img"):
    _, _, (w, h), alt = A[k]
    return f'<img class="{cls}" src="{url(k)}" alt="{e(alt)}" width="{w}" height="{h}" loading="lazy" data-asset="{A[k][0]}">'

def open_link(k, what):
    return (f'<a class="ssv-open" href="{url(k)}" target="_blank" rel="noopener" '
            f'aria-label="Open the {what} at full size (opens in a new tab)">Open full size ↗</a>')

def head(num, label, h2, lede=None, dark=False):
    d = " is-on-dark" if dark else ""
    num_html = f'<span class="dcw-eyebrow-num{d}">{num}</span>' if num else ""
    out = (f'<div class="dcw-head"><div class="dcw-eyebrow{d}">{num_html}{label}</div>'
           f'<h2 class="dcw-h2{d}">{h2}</h2><div class="dcw-h2-bar"></div>')
    if lede: out += f'<p class="dcw-lede{d}">{lede}</p>'
    return out + "</div>"

def credit(text, mine=False):
    return f'<div class="ssv-credit{" is-mine" if mine else ""}">{text}</div>'

def frame(k, extra=""):
    """Restrained frame for a wireframe. The wireframes already draw their own browser bar."""
    return f'<div class="ssv-frame{(" " + extra) if extra else ""}">{img(k)}</div>'

def artifact(k, title, what, cap, by, mine=False, scroll=None):
    """A diagram with its title, credit, caption and a full-size link."""
    scroll = scroll or "is-zoom"  # is-zoom: fits on desktop, scrolls sideways at a readable size on phones
    media = (f'<div class="ssv-scroll" tabindex="0" role="region" aria-label="{e(title)}, scrolls sideways">'
             f'{img(k, "ssv-img " + scroll)}</div>')
    hint = '<div class="ssv-hint">Scroll sideways to see the whole diagram.</div>' if scroll == "is-zoom" else ""
    return (f'<figure class="ssv-artifact"><div class="ssv-artifact-media">{media}</div>'
            f'<figcaption class="ssv-artifact-cap"><div class="ssv-artifact-row"><div class="ssv-artifact-title">{title}</div>{credit(by, mine)}</div>'
            f'<p class="dcw-fig-text">{cap}</p>{hint}{open_link(k, what)}</figcaption></figure>')

# ---------------------------------------------------------------- sections
S = {}

S["hero"] = f'''<header class="dcw-section is-hero" id="top">
<div class="dcw-hero-dots"></div>
<div class="dcw-wrap"><div class="dcw-hero-grid">
<div class="dcw-hero-copy">
<div class="dcw-eyebrow is-on-dark">Academic project · HCI · Fall 2020</div>
<h1 class="dcw-h1">Senior Services</h1>
<p class="dcw-hero-tagline">Understanding how older residents find and join county programs, and proposing a simpler way to sign up.</p>
<p class="dcw-p is-on-dark">An HCI course project at the University of Maryland. Our team of five interviewed five senior residents of Prince George's County, modeled what we heard, and proposed wireframes for signing up for the Senior ID card and activities online. The designs are proposals from a class project, not a launched product.</p>
<div class="dcw-hero-actions"><a class="dcw-btn is-hero" href="#wireframes">See the proposed wireframes ↓</a></div>
<div class="dcw-facts">
<div class="dcw-fact"><div class="dcw-chip is-on-dark"><span class="dcw-chip-dot"></span>My role</div><div class="dcw-fact-v">Research, data interpretation &amp; design</div></div>
<div class="dcw-fact"><div class="dcw-chip is-on-dark"><span class="dcw-chip-dot"></span>Context</div><div class="dcw-fact-v">UMD HCI · User Research Methods</div></div>
<div class="dcw-fact"><div class="dcw-chip is-on-dark"><span class="dcw-chip-dot"></span>Timeline</div><div class="dcw-fact-v">9 weeks · Fall 2020</div></div>
<div class="dcw-fact"><div class="dcw-chip is-on-dark"><span class="dcw-chip-dot"></span>Outcome</div><div class="dcw-fact-v">Research models &amp; proposed wireframes</div></div>
</div></div>
<div class="dcw-hero-visual"><div class="dcw-hero-halo"></div><div class="ssv-hero-frame">{frame("wf-landing", "is-hero")}<div class="ssv-hero-tag">Proposed wireframe · Senior ID landing page</div></div></div>
</div></div></header>'''

pills = ["Interviews", "Affinity diagram", "Relationship model", "Journey map", "Identity model",
         "Wall walk", "Visioning", "Sketching", "Wireframes"]
team_dots = '<span class="dcw-team-dot is-me"></span>' + '<span class="dcw-team-dot"></span>' * 4

def role_list(kind, items):
    return '<ol class="dcw-role-list">' + "".join(
        f'<li class="dcw-role-item is-{kind}"><span class="dcw-role-n is-{kind}">{i:02d}</span><span class="dcw-role-text is-{kind}">{t}</span></li>'
        for i, t in enumerate(items, 1)) + "</ol>"

S["overview"] = f'''<section class="dcw-section" id="overview"><div class="dcw-wrap">
{head("01", "Project overview", "A free program that many eligible residents weren't using")}
<div class="dcw-split">
<div class="dcw-col">
<div class="dcw-kicker">The program and its audience</div>
<p class="dcw-p">The Prince George's County Department of Parks and Recreation runs a Senior Services program for residents aged 60 and older. It offers free activities, events, nutrition services, and access to pools and fitness rooms across the county's 40 community centers. Seniors can sign up for a physical Senior ID card, which the department uses to track visits to its facilities. The card isn't required to enter a building or join an event.</p>
<div class="dcw-kicker is-spaced">The challenge</div>
<p class="dcw-statement">The department wanted more eligible residents to hold a Senior ID card, while offering services that fit the wide range of seniors' needs and lifestyles.</p>
<p class="dcw-p">At the time of the project, the brief stated that between 100,000 and 125,000 county residents were eligible, and that 15,000 to 17,000 held a Senior ID card.</p>
<p class="ssv-fineprint">These figures are as stated in the project materials in fall 2020. They aren't current, and the original source isn't cited here.</p>
</div>
<div class="dcw-col">
<div class="dcw-meta ssv-meta">
<div class="dcw-meta-row"><div class="dcw-meta-k">Project context</div><div class="dcw-meta-v">Senior Services, Prince George's County Department of Parks and Recreation</div></div>
<div class="dcw-meta-row"><div class="dcw-meta-k">Academic context</div><div class="dcw-meta-v">User Research Methods, a graduate course in the University of Maryland HCI program</div></div>
<div class="dcw-meta-row"><div class="dcw-meta-k">Team</div><div class="dcw-meta-v">Niku Letang, Camila Velloso, Brandon Cooper, Ruiqi, Matthew Alexander</div></div>
<div class="dcw-meta-row"><div class="dcw-meta-k">Timeline</div><div class="dcw-meta-v">9 weeks, fall 2020</div></div>
<div class="dcw-meta-row"><div class="dcw-meta-k">Methods</div><div class="dcw-pills">{"".join(f'<div class="dcw-chip"><span class="dcw-chip-dot"></span>{p}</div>' for p in pills)}</div></div>
<div class="dcw-meta-row"><div class="dcw-meta-k">Status</div><div class="dcw-meta-v">Academic research and proposed designs. Not built or launched.</div></div>
</div>
<div class="ssv-academic"><div class="ssv-academic-k">An academic project</div><p class="ssv-academic-t">This was coursework. The department's Senior Services program was the subject of the project, and nothing here suggests the department commissioned, reviewed or adopted the work.</p></div>
</div>
</div>
<div class="dcw-block">
<h3 class="dcw-h3">My role and the team's work</h3>
<div class="dcw-role-cols"><div class="dcw-who-card is-mine"><div class="dcw-role-head"><div class="dcw-role-kicker is-mine">My part</div><h4 class="dcw-role-title is-mine">My contributions</h4></div>
{role_list("mine", ["Took part in every stage: research planning, interview questions, interviews, data interpretation and design.",
                    "Conducted one of the five user interviews.",
                    "Created the relationship model."])}</div>
<div class="dcw-who-card is-team"><div class="dcw-role-head"><div class="dcw-role-kicker">Team of five</div><h4 class="dcw-role-title">Team process</h4><div class="dcw-team-dots" aria-hidden="true">{team_dots}</div></div>
{role_list("team", ["Wrote the research plan and interview questions together.",
                    "Interviewed five senior residents and interpreted the data with an affinity diagram, journey map and identity model.",
                    "Ran a wall walk and a visioning exercise, sketched concepts, and designed wireframes.",
                    "Work described as “we” or “the team” was collaborative unless it is credited to a person."])}</div></div>
</div>
<div class="dcw-block">
<div class="dcw-kicker">Process</div>
<ol class="ssv-steps">
<li class="ssv-step"><div class="ssv-step-n">01</div><div class="ssv-step-h">Research</div><p class="ssv-step-t">Five interviews with senior residents.</p></li>
<li class="ssv-step"><div class="ssv-step-n">02</div><div class="ssv-step-h">Data interpretation</div><p class="ssv-step-t">Affinity diagram, relationship model, journey map and identity model.</p></li>
<li class="ssv-step"><div class="ssv-step-n">03</div><div class="ssv-step-h">Design</div><p class="ssv-step-t">Wall walk, visioning sketches and wireframes.</p></li>
</ol>
</div>
</div></section>'''

S["preview"] = f'''<section class="dcw-section is-tint" id="preview"><div class="dcw-wrap">
{head("02", "Proposed experience preview", "A clearer path to the Senior ID card and activities", "Our proposal: a Senior ID landing page, a five-step online registration that also signs people up for activities, and pages for returning users to find and join activities.")}
<div class="ssv-board">{img("wf-overview")}</div>
<div class="ssv-board-cap"><div class="ssv-label">Proposed wireframes</div><p class="dcw-fig-text">All nine wireframes from the team's concept. Each screen is shown larger, in order, in section 07.</p></div>
<div class="ssv-points">
<div class="ssv-point"><div class="ssv-point-n">01</div><div class="ssv-point-h">Learn</div><p class="ssv-point-t">A Senior ID page answers "Am I eligible?", links to the activity schedule, and offers a short video.</p></div>
<div class="ssv-point"><div class="ssv-point-n">02</div><div class="ssv-point-h">Register</div><p class="ssv-point-t">Five steps with a progress indicator, including activity sign-up and a choice of paper or email.</p></div>
<div class="ssv-point"><div class="ssv-point-n">03</div><div class="ssv-point-h">Come back</div><p class="ssv-point-t">Returning users log in and sign up for activities from a filterable list.</p></div>
</div>
</div></section>'''

findings = [
    ("Finding information online was hard",
     "Participants struggled to navigate the department's website and find what they were looking for.",
     "A user-friendly website with a streamlined process for the most important tasks."),
    ("The pandemic left many feeling isolated",
     "Many participants described feeling socially isolated during the COVID-19 pandemic.",
     "Ways to connect with others through events and activities."),
    ("Staying active mattered",
     "Participants said that staying active was important to them.",
     "Activities that keep them physically active."),
    ("Strong ties to the community",
     "Participants were community-oriented and had strong ties to Prince George's County.",
     "Opportunities to serve their community, and activities to do with family and friends."),
]
S["research"] = f'''<section class="dcw-section" id="research"><div class="dcw-wrap">
{head("03", "Research", "Five conversations with senior residents", "We interviewed five senior residents about how they find, choose and sign up for activities, and how the department's Senior Services fit into their lives.")}
<div class="dcw-split">
<div class="dcw-col">
<div class="dcw-stats">
<div class="dcw-stat"><div class="dcw-stat-n">5</div><div class="dcw-stat-l">Interviews</div></div>
<div class="dcw-stat"><div class="dcw-stat-n">5</div><div class="dcw-stat-l">Team members</div></div>
<div class="dcw-stat"><div class="dcw-stat-n">9</div><div class="dcw-stat-l">Weeks, fall 2020</div></div>
</div>
<div class="ssv-academic is-spaced"><div class="ssv-academic-k">About the sample</div><p class="ssv-academic-t">Five interviews is a small, qualitative sample. The findings describe what these participants told us. They don't speak for all older adults or for every Senior Services member.</p></div>
</div>
<div class="dcw-col">
<h3 class="dcw-h3">What participants told us, and what we took from it</h3>
<p class="dcw-p">Each finding is what we heard in the interviews. The need beside it is the team's interpretation.</p>
<div class="ssv-findings">{"".join(f'<div class="ssv-finding"><div class="ssv-finding-n">{i:02d}</div><div class="ssv-finding-body"><h4 class="ssv-finding-h">{h}</h4><div class="ssv-finding-k">What participants described</div><p class="ssv-finding-t">{t}</p><div class="ssv-finding-k is-need">Need we identified</div><p class="ssv-finding-t is-need">{n}</p></div></div>' for i, (h, t, n) in enumerate(findings, 1))}</div>
</div>
</div>
</div></section>'''

S["synthesis"] = f'''<section class="dcw-section is-quiet" id="synthesis"><div class="dcw-wrap">
{head("04", "Synthesis", "Turning interviews into models", "We used several UX models to find patterns in the interview data: shared themes, the people who shape seniors' engagement, the steps of signing up, and who seniors are. These insights then shaped the designs.")}
<div class="ssv-model">
<div class="ssv-model-text"><div class="dcw-tag">Team artifact</div><h3 class="dcw-h3">Affinity diagram</h3><p class="dcw-p">We grouped notes from the five interviews into an affinity diagram to find common themes, attitudes and needs across participants. The four findings in section 03 came from this board.</p></div>
{artifact("affinity", "Affinity diagram", "affinity diagram", "Notes from the five interviews, grouped by theme. Scroll sideways to see the whole board.", "Team artifact", scroll="is-strip")}
</div>
<div class="ssv-feature">
<div class="ssv-feature-text"><div class="ssv-feature-intro">
<div class="dcw-tag">My model</div><h3 class="dcw-h3">Relationship model</h3>
<p class="dcw-p">The interviews showed that the people in seniors' lives influence whether they engage with Senior Services. I created a relationship model that maps three levels of relationships that influence participants' engagement with the department and the kinds of activities they do, and shows how those relationships could be used to meet their needs.</p></div>
<div class="ssv-feature-side"><div class="ssv-levels">
<div class="ssv-level is-1"><div class="ssv-level-h is-1">Senior program activity buddies</div><p class="ssv-level-t is-1">Spouse, Club 300 buddies, Senior Green Team, grandkids</p></div>
<div class="ssv-level is-2"><div class="ssv-level-h">Senior program acquaintances</div><p class="ssv-level-t">Parks &amp; Rec staff, golfers</p></div>
<div class="ssv-level is-3"><div class="ssv-level-h">External activity influencers</div><p class="ssv-level-t">Neighbors, local friends</p></div>
</div>
<p class="ssv-fineprint">From the inner level to the outer one, people share less interaction with the Parks and Recreation department.</p></div>
</div>
{artifact("relationship", "Relationship model", "relationship model", "Three levels of relationships around the senior, from activity buddies to outside influencers.", "Created by Niku Letang", mine=True)}
</div>
<div class="ssv-model is-wide">
<div class="ssv-model-text"><div class="dcw-tag">Team artifact</div><h3 class="dcw-h3">Journey map</h3>
<p class="dcw-p">We mapped how a senior might sign up for an activity online, with their thoughts and emotions, pain points and opportunities at each step: consulting friends and family, searching online, calling the department, and assessing the ID program.</p>
<p class="dcw-p"><strong class="dcw-strong">Active Agatha is a persona,</strong> a composite we built from the interview data. She isn't one of the participants, and the quotes on the map are the persona's synthesized thoughts.</p>
<p class="ssv-fineprint">The map's "Opportunities" and "Metrics" boxes were proposals. The metrics were suggested ways to measure a future program. They weren't collected.</p>
</div>
{artifact("journey", "Journey map", "journey map", "Active Agatha's journey to sign up for an activity, in four phases.", "Team artifact")}
</div>
<div class="ssv-model is-wide">
<div class="ssv-model-text"><div class="dcw-tag">Team artifact</div><h3 class="dcw-h3">Identity model</h3>
<p class="dcw-p">The identity model groups traits we heard into three parts, I like, I do and I am, with what each trait asks of a service:</p>
<div class="ssv-ids">
<div class="ssv-id"><div class="ssv-id-h">I like</div><p class="ssv-id-t">The outdoors, social interaction, family time</p></div>
<div class="ssv-id"><div class="ssv-id-h">I do</div><p class="ssv-id-t">Morning activities, web searches</p></div>
<div class="ssv-id"><div class="ssv-id-h">I am</div><p class="ssv-id-t">In the dark, an eager learner, proudly analog</p></div>
</div>
</div>
{artifact("identity", "Identity model", "identity model", "Traits grouped as I like, I do and I am.", "Illustration by Camila Velloso")}
</div>
</div></section>'''

issues = ["Couldn't find the activity list or schedule on the website.",
          "Didn't know how to sign up for the Senior ID online.",
          "Didn't receive mail or email from the department.",
          "Felt socially isolated during the pandemic."]
ideas = [("Streamlined online registration for all programming", "Wireframed", "is-done"),
         ("A video guide to signing up for the Senior ID and activities", "Video slot on the landing page", "is-part"),
         ("A prospect form", "Not developed further", "is-none"),
         ("A Senior Ambassador program", "Sketched · landing page link", "is-part"),
         ("Mental health resources and group therapy sessions", "Sketched · landing page link", "is-part")]
S["opportunity"] = f'''<section class="dcw-section" id="opportunity"><div class="dcw-wrap">
{head("05", "Opportunity framing", "From what we heard to what we could build", "We did a wall walk of the affinity diagram, asking what we must address, support or solve to add value to participants' lives. Most issues were about the website and about social isolation during the pandemic. We then listed “hot ideas”: possible design solutions.")}
<div class="ssv-frame3">
<div class="ssv-col"><div class="ssv-col-k">1 · What participants described</div><h3 class="ssv-col-h">Issues</h3>
<ol class="ssv-list">{"".join(f'<li class="ssv-li"><span class="ssv-li-n">{i:02d}</span><span class="ssv-li-t">{t}</span></li>' for i, t in enumerate(issues, 1))}</ol>
<p class="ssv-fineprint">Compiled by the team from the interviews.</p></div>
<div class="ssv-col is-team"><div class="ssv-col-k">2 · Team opportunity</div><h3 class="ssv-col-h">What to address</h3>
<p class="ssv-col-t">Make programs and schedules easy to find and join online, guide people through Senior ID sign-up, let people choose how they hear from the department, and help seniors connect during the pandemic.</p>
<p class="ssv-fineprint">This is a summary of the wall walk's focus, not a separate team artifact.</p></div>
<div class="ssv-col is-proposal"><div class="ssv-col-k">3 · Team proposals</div><h3 class="ssv-col-h">Hot ideas</h3>
<ol class="ssv-list">{"".join(f'<li class="ssv-li is-idea"><span class="ssv-li-t">{t}</span><span class="ssv-status {c}">{s}</span></li>' for t, s, c in ideas)}</ol>
<p class="ssv-fineprint">Not every idea was developed. The labels show where each one appears later on this page.</p></div>
</div>
</div></section>'''

S["ideation"] = f'''<section class="dcw-section is-tint" id="ideation"><div class="dcw-wrap">
{head("06", "Ideation and visioning", "Sketching the most promising ideas", "With the issues and hot ideas in hand, we chose three hot ideas for a visioning exercise and sketched how each could work. We then decided which would add the most value to seniors' lives and designed wireframes for those.")}
<div class="ssv-sketches">
<figure class="ssv-sketch">{img("sketch-isolation")}<figcaption class="ssv-sketch-cap"><div class="ssv-label">Vision 1 · Social isolation</div><p class="dcw-fig-text">A user's experience seeking mental health resources to address social isolation.</p>{open_link("sketch-isolation", "social isolation sketch")}</figcaption></figure>
<figure class="ssv-sketch">{img("sketch-senior-id")}<figcaption class="ssv-sketch-cap"><div class="ssv-label">Vision 2 · Senior ID</div><p class="dcw-fig-text">A user's experience learning about the Senior ID card and then signing up, with notes for a landing page, a program sign-up page and a redesigned upcoming events page.</p>{open_link("sketch-senior-id", "Senior ID sketch")}</figcaption></figure>
</div>
<div class="dcw-block"><h3 class="dcw-h3">Which ideas reached the wireframes</h3>
<div class="dcw-status-grid ssv-reach">
<div class="dcw-status is-tested"><div class="dcw-status-h">Wireframed</div><ul class="dcw-ul"><li class="dcw-li is-sm">The Senior ID vision: a landing page, a five-step registration with activity sign-up, and returning-user pages.</li></ul></div>
<div class="dcw-status is-concept"><div class="dcw-status-h">Linked, not designed</div><ul class="dcw-ul"><li class="dcw-li is-sm">Mental health support and Senior Ambassadors appear as quick links on the landing page. Their pages weren't wireframed.</li><li class="dcw-li is-sm">A Learn More video slot stands in for the video guide.</li></ul></div>
<div class="dcw-status is-concept"><div class="dcw-status-h">Not carried forward</div><ul class="dcw-ul"><li class="dcw-li is-sm">The prospect form doesn't appear in the sketches or wireframes shown here.</li></ul></div>
</div></div>
</div></section>'''

flow = [("wf-demographic", "Step 1", "Demographic information", "Name, date of birth, address and contact details. A progress indicator shows all five steps."),
        ("wf-activities", "Step 2", "Event and activities sign-up", "Shows the opportunities the person is eligible for, Senior ID, Green Team and Club 300, each with a sign-up checkbox."),
        ("wf-communication", "Step 3", "Communication preferences", "Choose paper or email, and what to hear about: upcoming events, volunteer opportunities and program updates."),
        ("wf-review", "Step 4", "Review", "One summary of the details, activities and communication choices before the account is created."),
        ("wf-password", "Step 5", "Create password", "Password rules are listed next to the fields, before Create Account."),
        ("wf-confirmation", "Done", "Confirmation", "Confirms the sign-ups, explains where to pick up the Senior ID, and asks for proof of residency, age and identity, in person or by upload.")]
returning = [("wf-activity-list", "Events and activities", "A list filtered by age, location, type and format, with Add to Calendar and Sign Up on each activity."),
             ("wf-login", "Log in", "Returning users log in. A link leads new users to sign up.")]
S["wireframes"] = f'''<section class="dcw-section" id="wireframes"><div class="dcw-wrap">
{head("07", "Proposed wireframes", "Registering for the Senior ID and activities", "The flow starts from the Senior ID landing page at the top of this page. These are the team's proposed wireframes from a course project. They weren't built or usability-tested.")}
<ol class="ssv-progress" aria-label="Registration steps">{"".join(f'<li class="ssv-progress-i"><span class="ssv-progress-n">{s if s != "Done" else "✓"}</span><span class="ssv-progress-t">{t}</span></li>' for s, t in [("1", "Demographic info"), ("2", "Events &amp; activities"), ("3", "Communication"), ("4", "Review"), ("5", "Create password"), ("Done", "Confirmation")])}</ol>
<div class="ssv-flow">{"".join(f'<figure class="ssv-fig">{frame(k)}<figcaption class="ssv-fig-cap"><div class="ssv-label">{s}</div><div class="ssv-fig-h">{h}</div><p class="dcw-fig-text">{t}</p>{open_link(k, h + " wireframe")}</figcaption></figure>' for k, s, h, t in flow)}</div>
<div class="dcw-block"><div class="ssv-gallery-head"><div class="dcw-kicker">Returning users</div><h3 class="dcw-h3">Finding and joining activities later</h3></div>
<div class="ssv-flow is-pair">{"".join(f'<figure class="ssv-fig">{frame(k)}<figcaption class="ssv-fig-cap"><div class="ssv-fig-h">{h}</div><p class="dcw-fig-text">{t}</p>{open_link(k, h + " wireframe")}</figcaption></figure>' for k, h, t in returning)}</div></div>
</div></section>'''

S["summary"] = f'''<section class="dcw-section is-quiet" id="summary"><div class="dcw-wrap">
{head("08", "Summary", "What the project produced")}
<div class="dcw-status-grid">
<div class="dcw-status is-tested"><div class="dcw-status-h">Research</div><ul class="dcw-ul"><li class="dcw-li is-sm">Five interviews with senior residents</li><li class="dcw-li is-sm">Four findings and four needs</li></ul></div>
<div class="dcw-status is-tested"><div class="dcw-status-h">Models</div><ul class="dcw-ul"><li class="dcw-li is-sm">Affinity diagram</li><li class="dcw-li is-sm">Relationship model (mine)</li><li class="dcw-li is-sm">Journey map with a persona</li><li class="dcw-li is-sm">Identity model</li></ul></div>
<div class="dcw-status is-delivered"><div class="dcw-status-h">Concepts</div><ul class="dcw-ul"><li class="dcw-li is-sm">Issues list and five hot ideas</li><li class="dcw-li is-sm">Visioning sketches</li></ul></div>
<div class="dcw-status is-concept"><div class="dcw-status-h">Proposed designs</div><ul class="dcw-ul"><li class="dcw-li is-sm">Nine wireframes: landing page, five-step registration, confirmation, activity list and login</li></ul></div>
</div>
<p class="ssv-fineprint is-wide">This page covers research and proposed designs from a course project. No usability testing, accessibility evaluation or outcome data is reported.</p>
</div></section>'''

S["reflection"] = '''<section class="dcw-section is-draft" id="reflection"><div class="dcw-wrap">
<div class="gfh-draft-banner"><strong>Draft only.</strong> Hidden on the live site until it has content: remove the is-draft class from this section to show it.</div>
<div class="dcw-head"><div class="dcw-eyebrow"><span class="dcw-eyebrow-num">09</span>Reflection</div><h2 class="dcw-h2">What I learned</h2><div class="dcw-h2-bar"></div></div>
<div class="gfh-draft"><div class="gfh-draft-k">Drafting placeholder</div><div class="gfh-draft-t">Prompts to answer:</div><ul class="gfh-draft-list"><li class="gfh-draft-li">What did interviewing older adults during the pandemic teach you?</li><li class="gfh-draft-li">What did building the relationship model change in how the team saw the problem?</li><li class="gfh-draft-li">What would you test or change if the project continued?</li></ul></div>
</div></section>'''

S["closing"] = '''<section class="dcw-section is-closing"><div class="dcw-wrap"><div class="dcw-closing">
<div class="gfh-closing-links"><a class="dcw-back" href="/#work">← Back to projects</a><a class="gfh-next" href="/dc-water">Next case study: DC Water →</a></div>
<div class="dcw-closing-note">Senior Services · HCI academic project · Fall 2020</div>
</div></div></section>'''

# ---------------------------------------------------------------- CSS (ssv- only)
TEAL, TEAL_S, TINT, MINT, DEEP, LTEAL = "#0f6e68", "#0a524e", "#e3f2ef", "#eef7f5", "#062b2a", "#6fd9cb"
INK, INK2, INK3, LINE = "#111111", "#3d3d3d", "#5f5f5f", "#e2e2e2"
SHADOW = "0 1px 2px rgba(6,43,42,0.05), 0 12px 28px -18px rgba(6,43,42,0.35)"

BASE = f"""
.ssv-img {{ display: block; width: 100%; max-width: 100%; height: auto; }}
.ssv-img.is-strip {{ width: auto; max-width: none; height: 274px; }}
.ssv-frame {{ padding: 8px; border: 1px solid #d9dddc; border-radius: 12px; background-color: #ffffff; box-shadow: 0 1px 2px rgba(0,0,0,0.05), 0 18px 36px -24px rgba(6,43,42,0.35); }}
.ssv-frame.is-hero {{ border-color: rgba(255,255,255,0.2); box-shadow: 0 30px 60px -30px rgba(0,0,0,0.6); }}
.ssv-hero-frame {{ position: relative; z-index: 1; width: 100%; max-width: 520px; }}
.ssv-hero-tag {{ margin-top: 12px; color: rgba(255,255,255,0.72); font-size: 13px; text-align: center; }}
.ssv-fineprint {{ margin-top: 12px; margin-bottom: 0; color: {INK3}; font-size: 13.5px; line-height: 1.5; }}
.ssv-fineprint.is-wide {{ max-width: 760px; margin-top: 24px; }}
.dcw-meta.ssv-meta {{ width: 100%; }}
.ssv-academic {{ width: 100%; margin-top: 24px; padding: 16px 18px; border: 1px solid {LINE}; border-left: 4px solid {TEAL}; border-radius: 10px; background-color: #ffffff; }}
.ssv-academic.is-spaced {{ margin-top: 28px; }}
.ssv-academic-k {{ margin-bottom: 4px; color: {TEAL_S}; font-size: 12px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; }}
.ssv-academic-t {{ margin-top: 0; margin-bottom: 0; color: {INK2}; font-size: 15px; line-height: 1.55; }}
.ssv-steps {{ display: grid; grid-template-columns: repeat(3, 1fr); grid-column-gap: 14px; grid-row-gap: 14px; margin-top: 8px; margin-bottom: 0; padding-left: 0; list-style-type: none; }}
.ssv-step {{ padding: 20px; border: 1px solid {LINE}; border-top: 4px solid {TEAL}; border-radius: 14px; background-color: #ffffff; box-shadow: {SHADOW}; }}
.ssv-step-n {{ color: {TEAL}; font-family: Inconsolata, monospace; font-size: 13px; font-weight: 700; }}
.ssv-step-h {{ margin-top: 6px; color: {INK}; font-size: 17px; font-weight: 600; }}
.ssv-step-t {{ margin-top: 4px; margin-bottom: 0; color: {INK2}; font-size: 15px; line-height: 1.5; }}
.ssv-board {{ padding: clamp(10px, 2vw, 20px); border: 1px solid {LINE}; border-radius: 16px; background-color: #ffffff; box-shadow: {SHADOW}; }}
.ssv-board-cap {{ margin-top: 14px; }}
.ssv-label {{ color: {TEAL_S}; font-size: 12px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; }}
.ssv-points {{ display: grid; grid-template-columns: repeat(3, 1fr); grid-column-gap: 14px; grid-row-gap: 14px; margin-top: 32px; }}
.ssv-point {{ padding: 20px; border-radius: 14px; background-color: #ffffff; }}
.ssv-point-n {{ display: inline-flex; justify-content: center; align-items: center; width: 32px; height: 32px; border-radius: 10px; background-color: {TEAL}; color: #ffffff; font-size: 13px; font-weight: 700; }}
.ssv-point-h {{ margin-top: 12px; color: {INK}; font-size: 17px; font-weight: 600; }}
.ssv-point-t {{ margin-top: 4px; margin-bottom: 0; color: {INK2}; font-size: 15px; line-height: 1.55; }}
.ssv-findings {{ display: flex; flex-direction: column; grid-row-gap: 12px; margin-top: 8px; }}
.ssv-finding {{ display: grid; grid-template-columns: 44px 1fr; padding: 18px 20px; border: 1px solid {LINE}; border-radius: 14px; background-color: #ffffff; box-shadow: {SHADOW}; }}
.ssv-finding-n {{ padding-top: 3px; color: {TEAL}; font-family: Inconsolata, monospace; font-size: 14px; font-weight: 700; }}
.ssv-finding-h {{ margin-top: 0; margin-bottom: 10px; color: {INK}; font-size: 17px; font-weight: 600; line-height: 1.35; }}
.ssv-finding-k {{ color: {INK3}; font-size: 11.5px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; }}
.ssv-finding-k.is-need {{ margin-top: 10px; padding-top: 10px; border-top: 1px dashed #cfd8d6; color: {TEAL_S}; }}
.ssv-finding-t {{ margin-top: 2px; margin-bottom: 0; color: {INK2}; font-size: 15.5px; line-height: 1.55; }}
.ssv-finding-t.is-need {{ color: {TEAL_S}; font-weight: 600; }}
.ssv-model {{ display: grid; grid-template-columns: 4fr 8fr; grid-column-gap: clamp(28px, 4vw, 56px); grid-row-gap: 24px; align-items: start; margin-top: clamp(48px, 6vw, 80px); }}
.ssv-model.is-wide {{ grid-template-columns: 1fr; }}
.ssv-model-text {{ display: flex; flex-direction: column; align-items: flex-start; max-width: 760px; }}
.ssv-feature {{ display: grid; grid-template-columns: 1fr; grid-column-gap: clamp(28px, 4vw, 56px); grid-row-gap: 24px; align-items: start; margin-top: clamp(48px, 6vw, 80px); padding: clamp(20px, 3vw, 40px); border-radius: 20px; background-color: #ffffff; box-shadow: 0 26px 50px -30px rgba(6,43,42,0.45); }}
.ssv-feature-text {{ display: grid; grid-template-columns: 7fr 5fr; grid-column-gap: clamp(28px, 4vw, 56px); grid-row-gap: 20px; align-items: start; }}
.ssv-feature-intro {{ display: flex; flex-direction: column; align-items: flex-start; }}
.ssv-feature-side {{ display: flex; flex-direction: column; padding-top: 8px; }}
.ssv-artifact {{ min-width: 0; margin-top: 0; margin-bottom: 0; margin-left: 0; margin-right: 0; padding: clamp(12px, 2vw, 20px); border: 1px solid {LINE}; border-radius: 16px; background-color: #ffffff; }}
.ssv-artifact-media {{ border-radius: 8px; overflow: hidden; }}
.ssv-artifact-cap {{ margin-top: 14px; }}
.ssv-artifact-row {{ display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; grid-column-gap: 12px; grid-row-gap: 6px; }}
.ssv-artifact-title {{ color: {INK}; font-size: 15px; font-weight: 600; }}
.ssv-credit {{ padding: 3px 10px; border: 1px solid {LINE}; border-radius: 999px; background-color: #f6f6f5; color: {INK3}; font-size: 12px; font-weight: 600; }}
.ssv-credit.is-mine {{ border-color: {TEAL}; background-color: {TEAL}; color: #ffffff; }}
.ssv-open {{ display: inline-block; margin-top: 10px; color: {TEAL}; font-size: 14px; font-weight: 600; text-decoration: none; border-bottom: 1px solid rgba(15,110,104,0.35); }}
.ssv-open:hover {{ color: {TEAL_S}; border-bottom-color: {TEAL_S}; }}
.ssv-open:focus {{ outline: 3px solid {LTEAL}; outline-offset: 3px; border-radius: 2px; }}
.ssv-hint {{ display: none; margin-top: 6px; color: {INK3}; font-size: 13px; }}
.ssv-scroll {{ overflow-x: auto; overflow-y: hidden; border-radius: 8px; background-color: #f6f6f5; }}
.ssv-scroll:focus {{ outline: 3px solid {TEAL}; outline-offset: 2px; }}
.ssv-levels {{ display: flex; flex-direction: column; grid-row-gap: 8px; width: 100%; margin-top: 4px; }}
.ssv-level {{ padding: 12px 14px; border-radius: 10px; }}
.ssv-level.is-1 {{ background-color: {TEAL}; }}
.ssv-level.is-2 {{ background-color: {TINT}; }}
.ssv-level.is-3 {{ border: 1px solid {LINE}; background-color: #ffffff; }}
.ssv-level-h {{ color: {INK}; font-size: 15px; font-weight: 600; }}
.ssv-level-t {{ margin-top: 2px; margin-bottom: 0; color: {INK2}; font-size: 14.5px; line-height: 1.45; }}
.ssv-level-h.is-1 {{ color: #ffffff; }}
.ssv-level-t.is-1 {{ color: rgba(255,255,255,0.88); }}
.ssv-ids {{ display: grid; grid-template-columns: repeat(3, 1fr); grid-column-gap: 10px; grid-row-gap: 10px; width: 100%; }}
.ssv-id {{ padding: 12px 14px; border: 1px solid {LINE}; border-radius: 10px; background-color: #ffffff; }}
.ssv-id-h {{ color: {TEAL_S}; font-size: 13px; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; }}
.ssv-id-t {{ margin-top: 4px; margin-bottom: 0; color: {INK2}; font-size: 15px; line-height: 1.45; }}
.ssv-frame3 {{ display: grid; grid-template-columns: 1fr 1fr 1fr; grid-column-gap: 14px; grid-row-gap: 14px; align-items: stretch; }}
.ssv-col {{ display: flex; flex-direction: column; padding: clamp(18px, 2.4vw, 28px); border: 1px solid {LINE}; border-radius: 16px; background-color: #ffffff; }}
.ssv-col.is-team {{ background-color: {MINT}; border-color: #cfe6e2; }}
.ssv-col.is-proposal {{ border-color: {TEAL}; box-shadow: {SHADOW}; }}
.ssv-col-k {{ color: {INK3}; font-size: 12px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; }}
.ssv-col-h {{ margin-top: 6px; margin-bottom: 14px; color: {INK}; font-size: 20px; font-weight: 600; line-height: 1.3; }}
.ssv-col-t {{ margin-top: 0; margin-bottom: 0; color: {INK2}; font-size: 15.5px; line-height: 1.6; }}
.ssv-list {{ display: flex; flex-direction: column; grid-row-gap: 10px; margin-top: 0; margin-bottom: 0; padding-left: 0; list-style-type: none; }}
.ssv-li {{ display: flex; align-items: flex-start; grid-column-gap: 10px; color: {INK2}; font-size: 15px; line-height: 1.5; }}
.ssv-li.is-idea {{ flex-direction: column; align-items: flex-start; grid-row-gap: 4px; padding-bottom: 10px; border-bottom: 1px solid {LINE}; }}
.ssv-li-n {{ flex: none; padding-top: 1px; color: {TEAL}; font-family: Inconsolata, monospace; font-size: 13px; font-weight: 700; }}
.ssv-li-t {{ color: {INK2}; }}
.ssv-status {{ display: inline-block; padding: 2px 8px; border-radius: 999px; font-size: 11.5px; font-weight: 700; letter-spacing: 0.04em; }}
.ssv-status.is-done {{ background-color: {TEAL}; color: #ffffff; }}
.ssv-status.is-part {{ background-color: {TINT}; color: {TEAL_S}; }}
.ssv-status.is-none {{ border: 1px dashed #b5b5b5; color: {INK3}; }}
.ssv-sketches {{ display: grid; grid-template-columns: 5fr 7fr; grid-column-gap: clamp(20px, 3vw, 40px); grid-row-gap: 32px; align-items: start; }}
.ssv-sketch {{ min-width: 0; margin-top: 0; margin-bottom: 0; margin-left: 0; margin-right: 0; padding: clamp(12px, 2vw, 20px); border-radius: 16px; background-color: #ffffff; box-shadow: {SHADOW}; }}
.ssv-sketch-cap {{ margin-top: 14px; }}
.dcw-status-grid.ssv-reach {{ grid-template-columns: repeat(3, 1fr); margin-top: 16px; }}
.ssv-progress {{ display: flex; flex-wrap: wrap; grid-column-gap: 8px; grid-row-gap: 8px; margin-top: 0; margin-bottom: 32px; padding-left: 0; list-style-type: none; }}
.ssv-progress-i {{ display: flex; align-items: center; grid-column-gap: 8px; padding: 6px 12px 6px 6px; border: 1px solid #cfe6e2; border-radius: 999px; background-color: {MINT}; }}
.ssv-progress-n {{ display: flex; justify-content: center; align-items: center; width: 24px; height: 24px; border-radius: 50%; background-color: {TEAL}; color: #ffffff; font-size: 12px; font-weight: 700; }}
.ssv-progress-t {{ color: {TEAL_S}; font-size: 13.5px; font-weight: 600; }}
.ssv-flow {{ display: grid; grid-template-columns: 1fr 1fr; grid-column-gap: clamp(24px, 4vw, 56px); grid-row-gap: clamp(36px, 5vw, 56px); align-items: start; }}
.ssv-fig {{ min-width: 0; margin-top: 0; margin-bottom: 0; margin-left: 0; margin-right: 0; }}
.ssv-fig-cap {{ margin-top: 14px; max-width: 520px; }}
.ssv-fig-h {{ margin-top: 4px; color: {INK}; font-size: 17px; font-weight: 600; line-height: 1.35; }}
.ssv-gallery-head {{ margin-bottom: 24px; }}
"""
MED = f"""
.ssv-model {{ grid-template-columns: 1fr; }}
.ssv-feature-text {{ grid-template-columns: 1fr; }}
.ssv-frame3 {{ grid-template-columns: 1fr; }}
.ssv-sketches {{ grid-template-columns: 1fr; }}
.dcw-status-grid.ssv-reach {{ grid-template-columns: 1fr; }}
.ssv-points {{ grid-template-columns: 1fr; }}
.ssv-hero-frame {{ max-width: 560px; }}
"""
SMALL = f"""
.ssv-steps {{ grid-template-columns: 1fr; }}
.ssv-flow {{ grid-template-columns: 1fr; }}
.ssv-ids {{ grid-template-columns: 1fr; }}
.ssv-img.is-strip {{ height: 220px; }}
.ssv-img.is-zoom {{ width: 760px; max-width: none; }}
.ssv-hint {{ display: block; }}
.ssv-finding {{ grid-template-columns: 1fr; grid-row-gap: 4px; }}
.ssv-frame {{ padding: 5px; border-radius: 10px; }}
"""
TINY = ""

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

ORDER = ["hero", "overview", "preview", "research", "synthesis", "opportunity", "ideation", "wireframes", "summary", "reflection", "closing"]

def preview_css():
    """Full CSS for the standalone check page: DC Water + Grove + Senior Services rules."""
    import importlib.util
    css = []
    for name in ("build", "build_grove"):
        spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + ".py"))
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        css.append(m.BASE)
        for bp in ("MED", "SMALL", "TINY"):
            if getattr(m, bp, ""):
                css.append(f'{MQ[{"MED": "med", "SMALL": "small", "TINY": "tiny"}[bp]]} {{ {getattr(m, bp)} }}')
    css += [BASE, f'{MQ["med"]} {{ {MED} }}', f'{MQ["small"]} {{ {SMALL} }}']
    return "\n".join(css)

if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    done, out = set(), []
    for k in ORDER:
        h = compact(S[k])
        out.append({"label": k, "html": h, "css": css_for(h, done)})
    json.dump(out, open(os.path.join(HERE, "out/senior-sections.json"), "w"), ensure_ascii=False, indent=1)
    page = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@600;700&display=swap">'
            '<style>body{margin:0}*{box-sizing:border-box}' + preview_css() + '</style></head><body><main class="dcw-page">'
            + "".join(o["html"] for o in out) + "</main></body></html>")
    open(os.path.join(HERE, "out/senior-check.html"), "w").write(page)
    for o in out:
        print(o["label"], len(o["html"]), len(o["css"]))
