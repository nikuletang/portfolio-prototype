/*
 * Page configuration: edit these values, no other code changes needed.
 *
 * backToProjectsUrl
 *   Where the "Back to projects" links go. Replace "#" with the real
 *   URL of your portfolio's projects page.
 *
 * figma.<flow>.url
 *   The share link for each Figma prototype, e.g.
 *   "https://www.figma.com/proto/XXXX/DC-Water?node-id=...".
 *   While a url is empty, the page shows a clearly labelled
 *   "URL not configured" state instead of a link.
 *
 * figma.<flow>.embed
 *   true  – show a "Load interactive prototype" button that loads the
 *           Figma embed in place (only once a url is set).
 *   false – show the static poster image only and keep the external link.
 */
window.CASE_STUDY_CONFIG = {
  backToProjectsUrl: "#",

  figma: {
    reportProblem: {
      title: "Report a Problem prototype",
      url: "",
      embed: true
    },
    customerService: {
      title: "Customer Service Form prototype",
      url: "",
      embed: true
    },
    imageRecognition: {
      title: "Image Recognition concept prototype",
      url: "",
      embed: true
    }
  }
};
