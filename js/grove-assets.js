/*
 * Grove Family Health: image asset manifest
 * ---------------------------------------------------------------
 * Every image slot on grove-family-health.html is a
 * <div class="ph" data-asset="ID">. To add an image:
 *   1. Save it in /assets/images/grove/ using the `file` name below
 *      (or change `file` to match your file).
 *   2. Reload the page. The placeholder is swapped for the image
 *      automatically, using `alt` as its alternative text.
 *
 * Images keep their own proportions once loaded, so a tall full-page
 * screenshot stays tall. `kind` only sets the placeholder shape:
 *   tall    – full-page desktop screenshot (portrait, any height)
 *   section – a cropped part of a page (any proportions)
 *   board   – sitemap, mood board, branding sheet (any proportions)
 *
 * Export screenshots WITHOUT a browser frame: the page draws it.
 * Keep Grove's original site colors; don't recolor screenshots.
 * Each image is used once on the page (no repeats).
 */
window.CASE_STUDY_ASSETS = {
  /* ---------- Hero ---------- */
  "hero-mockup": {
    file: "grove/hero-page.png", kind: "tall",
    label: "Hero: a key page of the final website",
    note: "Full-page desktop screenshot, portrait. The homepage is shown in the Solution preview, so pick a different page here, or swap them.",
    alt: "A full-page view of a page on the redesigned Grove Family Health website."
  },

  /* ---------- Solution preview ---------- */
  "solution-home": {
    file: "grove/final-homepage.png", kind: "tall",
    label: "Final homepage",
    note: "Full-page desktop screenshot of the launched homepage.",
    alt: "The redesigned Grove Family Health homepage, from the top navigation to the footer."
  },
  "solution-patients": {
    file: "grove/final-patients.png", kind: "tall",
    label: "Final page with patient-focused information",
    note: "Page name to confirm. The page a patient or non-member uses to understand care and membership.",
    alt: "A page of the redesigned Grove Family Health website with information for patients."
  },
  "solution-employers": {
    file: "grove/final-employers.png", kind: "tall",
    label: "Final page with employer-focused information",
    note: "Page name to confirm. The page employers use to evaluate a plan for their team.",
    alt: "A page of the redesigned Grove Family Health website with information for employers."
  },

  /* ---------- Understanding the challenge ---------- */
  "original-site": {
    file: "grove/original-homepage.png", kind: "tall",
    label: "Original website (before the redesign)",
    note: "Full-page screenshot of the previous homepage, or the page that best shows the challenge.",
    alt: "Grove Family Health's previous website homepage, before the redesign."
  },

  /* ---------- Site architecture ---------- */
  "sitemap": {
    file: "grove/sitemap.png", kind: "board",
    label: "Sitemap",
    note: "Export at high resolution so page names stay legible. Any proportions.",
    alt: "Sitemap of the redesigned Grove Family Health website, showing how pages are organized for patients and employers."
  },

  /* ---------- Visual direction ---------- */
  "moodboard": {
    file: "grove/mood-board.png", kind: "board",
    label: "Mood board",
    alt: "Mood board for the Grove Family Health website: imagery, color and type references within the practice's existing brand."
  },
  "branding-sheet": {
    file: "grove/branding-sheet.png", kind: "board",
    label: "Branding sheet",
    alt: "Branding sheet for the Grove Family Health website, showing how the existing brand is applied to typography, color and interface elements."
  },

  /* ---------- Wireframes ---------- */
  "wf-home": {
    file: "grove/wireframe-homepage.png", kind: "tall",
    label: "Wireframe: homepage",
    alt: "Homepage wireframe for the Grove Family Health website."
  },
  "wf-patients": {
    file: "grove/wireframe-patients.png", kind: "tall",
    label: "Wireframe: patient-focused page",
    note: "Page name to confirm.",
    alt: "Wireframe of a patient-focused page for the Grove Family Health website."
  },
  "wf-employers": {
    file: "grove/wireframe-employers.png", kind: "tall",
    label: "Wireframe: employer-focused page",
    note: "Page name to confirm.",
    alt: "Wireframe of an employer-focused page for the Grove Family Health website."
  },

  /* ---------- Key decisions: before / after ----------
   * "Before" can be the original site OR the wireframe. Update the
   * label in the HTML (compare__label) to say which. */
  "cmp-find-before": {
    file: "grove/compare-find-before.png", kind: "section",
    label: "Before: finding relevant information",
    note: "Original site or wireframe. E.g. the original navigation or homepage entry points.",
    alt: "Before the redesign: how patients and employers reached information on the site."
  },
  "cmp-find-after": {
    file: "grove/compare-find-after.png", kind: "section",
    label: "After: separate paths for patients and employers",
    note: "Crop of the final design showing navigation or audience entry points.",
    alt: "After the redesign: separate paths for patients and employers in the navigation."
  },
  "cmp-model-before": {
    file: "grove/compare-model-before.png", kind: "section",
    label: "Before: services and care model",
    note: "Original site or wireframe. How services were grouped and the model was explained.",
    alt: "Before the redesign: services grouped together, with little explanation of direct primary care."
  },
  "cmp-model-after": {
    file: "grove/compare-model-after.png", kind: "section",
    label: "After: dedicated service content",
    note: "Crop of the final design showing a dedicated service page or the care-model explanation.",
    alt: "After the redesign: a dedicated service page that explains the care option in plain language."
  },
  "cmp-next-before": {
    file: "grove/compare-next-before.png", kind: "section",
    label: "Before: next steps",
    note: "Original site or wireframe. Where calls to action appeared, or didn't.",
    alt: "Before the redesign: a page section without a clear next step."
  },
  "cmp-next-after": {
    file: "grove/compare-next-after.png", kind: "section",
    label: "After: visible next steps",
    note: "Crop of the final design showing the enrollment pathway or a visible call to action.",
    alt: "After the redesign: a visible call to action leading toward enrollment."
  },

  /* ---------- Final website gallery ----------
   * Pages not already shown above. Delete unused slots in the HTML. */
  "final-1": {
    file: "grove/final-page-1.png", kind: "tall",
    label: "Final page 1 (page name to confirm)",
    alt: "A page of the redesigned Grove Family Health website."
  },
  "final-2": {
    file: "grove/final-page-2.png", kind: "tall",
    label: "Final page 2 (page name to confirm)",
    alt: "A page of the redesigned Grove Family Health website."
  },
  "final-3": {
    file: "grove/final-page-3.png", kind: "tall",
    label: "Final page 3 (page name to confirm)",
    alt: "A page of the redesigned Grove Family Health website."
  },
  "final-4": {
    file: "grove/final-page-4.png", kind: "tall",
    label: "Final page 4 (page name to confirm)",
    alt: "A page of the redesigned Grove Family Health website."
  },
  "final-5": {
    file: "grove/final-page-5.png", kind: "tall",
    label: "Final page 5 (optional)",
    alt: "A page of the redesigned Grove Family Health website."
  }
};
