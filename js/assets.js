/*
 * Image asset manifest
 * ---------------------------------------------------------------
 * Every image slot on the page is a <div class="ph" data-asset="ID">.
 * To add an image:
 *   1. Export the image and save it in /assets/images/ using the
 *      `file` name below (or change `file` to match your file).
 *   2. Reload the page. The placeholder is swapped for the image
 *      automatically, using `alt` as its alternative text.
 *
 * kind controls the placeholder proportions before an image exists:
 *   phone  – a single mobile screen (approx. 9:19.5)
 *   crop   – a cropped mobile screen (approx. 9:16)
 *   board  – a research board or whiteboard (16:10)
 *   wide   – a wide showcase image (16:9)
 *   sketch – a hand sketch (4:5)
 */
window.CASE_STUDY_ASSETS = {
  /* ---------- Hero ---------- */
  "hero-mockup": {
    file: "hero-final-mockup.png", kind: "phone",
    label: "Hero: final Report a Problem landing screen",
    note: "Final landing screen with Report a Problem Form, Track Your Report and Customer Service Form buttons. Screen only. The page draws the device frame.",
    alt: "The final Report a Problem landing screen on DC Water's mobile site, with buttons to start a report, track a report, or open the customer service form."
  },

  /* ---------- Research ---------- */
  "research-card-sort": {
    file: "research-image-card-sort.png", kind: "board",
    label: "Image card sorting board or results",
    note: "Optional. The PDF reports the card sort's numbers but doesn't show the board. Add a results board or a sample of the 15 photos if you have one.",
    alt: "Image card sorting activity: photos of water-related problems grouped and named by a participant."
  },
  "research-word-bank": {
    file: "research-word-bank-board.png", kind: "board",
    label: "Word bank and image association board",
    note: "Board with Photos #1–12, their word stickies, the two prompts and the word bank. A high-resolution export keeps the stickies legible.",
    alt: "Word bank and image association board: twelve photos of water problems, each surrounded by word sticky notes participants dragged from a word bank."
  },

  /* ---------- Report a Problem: 1st iteration (Sprint 3) ---------- */
  "rap-v1-landing": {
    file: "rap-v1-01-landing.png", kind: "phone",
    label: "Iteration 1: Landing page",
    alt: "Iteration 1 landing page explaining that DC Water monitors the system 24/7, with Track Status and Start Report buttons."
  },
  "rap-v1-category": {
    file: "rap-v1-02-problem-category.png", kind: "phone",
    label: "Iteration 1: Problem category (Report an Emergency)",
    alt: "Iteration 1 'Report an Emergency', step 2 of 3: 'Where is the problem?' with Outdoors, Indoors and Other options."
  },
  "rap-v1-subcategory": {
    file: "rap-v1-03-subcategory-outdoors.png", kind: "phone",
    label: "Iteration 1: Problem sub-category (Outdoors)",
    alt: "Iteration 1 step 3 of 3: 'What is the problem?' with Flooding/Leaking, Damage and Other options."
  },
  "rap-v1-details": {
    file: "rap-v1-04-problem-details.png", kind: "phone",
    label: "Iteration 1: Problem details",
    alt: "Iteration 1 additional details screen with optional photo, suggested tags and description."
  },
  "rap-v1-contact": {
    file: "rap-v1-05-contact-information.png", kind: "phone",
    label: "Iteration 1: Contact information",
    alt: "Iteration 1 contact information form with name, phone and email fields and a single question about receiving status alerts."
  },
  "rap-v1-review": {
    file: "rap-v1-06-review.png", kind: "phone",
    label: "Iteration 1: Review",
    alt: "Iteration 1 review screen showing location on a map, issue type and photos, each with an Edit link."
  },
  "rap-v1-tracking": {
    file: "rap-v1-07-tracking.png", kind: "phone",
    label: "Iteration 1: Tracking / confirmation",
    alt: "Iteration 1 confirmation screen with a ticket number, an 'Under review' progress bar, case history and next steps."
  },

  /* ---------- Report a Problem: 2nd iteration (Sprint 4) ---------- */
  "rap-v2-title": {
    file: "rap-v2-01-form-title.png", kind: "phone",
    label: "Iteration 2: Form title (Report a Problem)",
    alt: "Iteration 2 landing page titled 'Report a Problem' instead of 'Report an Emergency'."
  },
  "rap-v2-notifications": {
    file: "rap-v2-02-notifications.png", kind: "phone",
    label: "Iteration 2: Notifications",
    alt: "Iteration 2 notifications screen with separate choices for receiving ticket updates and for letting DC Water make contact, each by phone call or email."
  },
  "rap-v2-ticket": {
    file: "rap-v2-03-ticket-status.png", kind: "phone",
    label: "Iteration 2: Ticket status",
    alt: "Iteration 2 ticket status page: a resolved ticket with a five-star rating, a Leave feedback button, and Case History and Ticket Details tabs."
  },

  /* ---------- Image recognition: ideation ---------- */
  "ir-wireframes": {
    file: "ir-wireframes.jpg", kind: "board",
    label: "Wireframes: image recognition main screens",
    note: "Photo or export of the team's wireframes for the image recognition design.",
    alt: "Wireframes of the main image recognition screens: a choice between form and camera, the camera view, problem details as a drawer or a full page, submission confirmation and a ticket number."
  },
  "ir-sketch": {
    file: "ir-sketch-object-detected.jpg", kind: "sketch",
    label: "Sketch: reporting a problem using image recognition",
    note: "Hand sketch showing 'Object Detected: Fire Hydrant' with Confirm and Try Again.",
    alt: "Hand-drawn phone screen showing a leaking fire hydrant, an 'Object Detected: Fire Hydrant' panel with a short definition, and Confirm and Try Again buttons."
  },

  /* ---------- Image recognition: 1st iteration ---------- */
  "ir-v1-landing": { file: "ir-v1-01-landing.png", kind: "phone", label: "IR iteration 1: Landing page (split buttons)", alt: "Welcome to Report a Problem screen with Fill Form and Image Identifier buttons side by side." },
  "ir-v1-upload": { file: "ir-v1-02-upload.png", kind: "phone", label: "IR iteration 1: Upload options", alt: "Action sheet offering Take Photo, Choose From Library and Cancel." },
  "ir-v1-camera": { file: "ir-v1-03-camera-view.png", kind: "phone", label: "IR iteration 1: Camera view", alt: "Camera view aimed at a fire hydrant spraying water onto the street, with the hint 'Tap the button below to start.'" },
  "ir-v1-description": { file: "ir-v1-04-object-description.png", kind: "phone", label: "IR iteration 1: Object description", alt: "Captured photo with the message 'A fire hydrant has been detected. A fire hydrant is a connection point by which firefighters can tap into a water supply.'" },
  "ir-v1-drawer": { file: "ir-v1-05-problem-details-drawer.png", kind: "phone", label: "IR iteration 1: Problem details (drawer)", alt: "Drawer over the photo: 'Object recognized: Fire Hydrant', an editable address, pre-selected Flooding tag and a Submit Report button." },
  "ir-v1-collapsed": { file: "ir-v1-06-collapsible-drawer.png", kind: "phone", label: "IR iteration 1: Collapsed drawer", alt: "The details drawer collapsed, showing the full photo." },
  "ir-v1-library": { file: "ir-v1-07-photo-library.png", kind: "phone", label: "IR iteration 1: Photo library", alt: "Native photo library picker." },
  "ir-v1-confirm": { file: "ir-v1-08-confirmation.png", kind: "phone", label: "IR iteration 1: Confirmation dialog", alt: "Confirm Submission dialog asking the user to select submit if they have reviewed their information." },
  "ir-v1-ticket": { file: "ir-v1-09-ticket-number.png", kind: "phone", label: "IR iteration 1: Ticket number", alt: "Thank-you dialog with ticket number #21-00541774 and Copy Ticket Number and Exit options." },

  /* ---------- A/B test pairs ---------- */
  "ab-landing-a": { file: "ab-landing-a-split-button.png", kind: "phone", label: "Landing, Option A: split button", alt: "Option A landing page with Fill Form and Image Identifier split buttons above Track Your Report and Customer Service Form." },
  "ab-landing-b": { file: "ab-landing-b-photo-layout.png", kind: "phone", label: "Landing, Option B: photo layout", alt: "Option B landing page with a collage of problem photos, a 'Show Us The Issue' button and Track Your Report." },
  "ab-details-a": { file: "ab-details-a-drawer.png", kind: "phone", label: "Problem details, Option A: interaction drawer", alt: "Option A problem details shown in a drawer over the photo." },
  "ab-details-b": { file: "ab-details-b-full-page.png", kind: "phone", label: "Problem details, Option B: full page", alt: "Option B problem details on a full page, with the photo thumbnail and a prominent Add Photo tile." },

  /* ---------- Image recognition: 2nd iteration ---------- */
  "ir-v2-error": { file: "ir-v2-01-error.png", kind: "phone", label: "IR iteration 2: Image not recognized", alt: "'Image Not Recognized' alert: 'This is not a DC Water object. Please take another photo.' with Retake." },
  "ir-v2-form-option": { file: "ir-v2-02-form-option.png", kind: "phone", label: "IR iteration 2: 'No photo? Fill out a form.'", alt: "Action sheet with Take Photo, Choose From Library and a new 'No photo? Fill out a form.' option." },
  "ir-v2-outline": { file: "ir-v2-03-object-outline.png", kind: "phone", label: "IR iteration 2: Object outline", alt: "Photo with a labelled outline drawn around the fire hydrant and spraying water." },
  "ir-v2-location": { file: "ir-v2-04-edit-location.png", kind: "phone", label: "IR iteration 2: Edit location", alt: "Edit location screen with a search field, a map and an Update Location button." },
  "ir-v2-thanks": { file: "ir-v2-05-thank-you.png", kind: "phone", label: "IR iteration 2: Thank-you message", alt: "Thank-you dialog: 'You can follow up on your report by uploading your image on the tracking page.' with Exit." },
  "ir-v2-photo": { file: "ir-v2-06-additional-photo.png", kind: "phone", label: "IR iteration 2: Additional photo uploaded", alt: "Full-page problem details with two uploaded photos of fire hydrants." },
  "ir-v2-tracking": { file: "ir-v2-07-tracking.png", kind: "phone", label: "IR iteration 2: Track by uploading the original photo", alt: "Track Your Report screen asking the user to upload the original photo submitted with the report." },

  /* ---------- Final: Report a Problem (14 screens) ---------- */
  "rap-01": { file: "final-rap-01-landing.png", kind: "phone", label: "Report a Problem: Landing", alt: "Report a Problem landing page with Report a Problem Form, Track Your Report and Customer Service Form buttons." },
  "rap-02": { file: "final-rap-02-location.png", kind: "phone", label: "Report a Problem: Step 1, location", alt: "Step 1 of 3, 'What is your location?', with an address field, Use my location and Drop a Pin buttons, and a map." },
  "rap-03": { file: "final-rap-03-where.png", kind: "phone", label: "Report a Problem: Step 2, where is the problem?", alt: "Step 2 of 3, 'Where is the problem?', with Outdoors and Indoors options and a link to describe the issue if unsure." },
  "rap-04": { file: "final-rap-04-what.png", kind: "phone", label: "Report a Problem: What is the problem?", alt: "'What is the problem?' with Flooding / Leaking, Damage and Other / Not Sure options." },
  "rap-05": { file: "final-rap-05-additional-details.png", kind: "phone", label: "Report a Problem: Additional details", alt: "Optional additional details: add a photo, suggested tags and a description." },
  "rap-06": { file: "final-rap-06-notifications.png", kind: "phone", label: "Report a Problem: Notifications", alt: "Optional notifications: choose phone call or email for ticket updates and for questions from DC Water, then enter contact details." },
  "rap-07": { file: "final-rap-07-review.png", kind: "phone", label: "Report a Problem: Review", alt: "Review screen listing location, issue and photos, each with an Edit link." },
  "rap-08": { file: "final-rap-08-submitted.png", kind: "phone", label: "Report a Problem: Submitted", alt: "Thank-you screen with ticket number #21-00541774 and buttons to view ticket status, report another problem or share." },
  "rap-09": { file: "final-rap-09-track-your-report.png", kind: "phone", label: "Track Your Report: Enter ticket number", alt: "Track Your Report screen with a ticket number field and help text." },
  "rap-10": { file: "final-rap-10-ticket-opened.png", kind: "phone", label: "Ticket status: Opened", alt: "Ticket status showing 'Ticket Opened', next steps and case history." },
  "rap-11": { file: "final-rap-11-ticket-closed.png", kind: "phone", label: "Ticket status: Closed, rate your experience", alt: "Closed ticket: 'Your case has been resolved' with a five-star rating and a Leave feedback button." },
  "rap-12": { file: "final-rap-12-rated.png", kind: "phone", label: "Ticket status: Rated", alt: "Closed ticket after rating: five filled stars and 'Thank you for rating your experience!'" },
  "rap-13": { file: "final-rap-13-feedback.png", kind: "phone", label: "Feedback form", alt: "Feedback dialog: 'Your feedback is important to us!' with a text field and Submit button." },
  "rap-14": { file: "final-rap-14-feedback-thanks.png", kind: "phone", label: "Feedback submitted", alt: "Confirmation dialog: 'Thank you for submitting your feedback!'" },

  /* ---------- Final: Customer Service (7 screens) ---------- */
  "cs-01": { file: "final-cs-01-topic.png", kind: "phone", label: "Customer Service: Select a topic", alt: "Customer Service Form: 'Please select a topic' with Billing Inquiry, Damage and Other." },
  "cs-02": { file: "final-cs-02-topic-selected.png", kind: "phone", label: "Customer Service: Topic selected", alt: "Billing Inquiry selected and the Next button enabled." },
  "cs-03": { file: "final-cs-03-details.png", kind: "phone", label: "Customer Service: Additional details", alt: "'How can we help you?' text field, location field, suggested billing tags and file upload." },
  "cs-04": { file: "final-cs-04-details-filled.png", kind: "phone", label: "Customer Service: Details filled in", alt: "Completed details describing an unusually high bill, with the Billing tag selected." },
  "cs-05": { file: "final-cs-05-contact.png", kind: "phone", label: "Customer Service: Contact information", alt: "Contact information form with name, email, phone and optional account number." },
  "cs-06": { file: "final-cs-06-review.png", kind: "phone", label: "Customer Service: Review", alt: "Review screen listing description, topic, location and tags, each with Edit." },
  "cs-07": { file: "final-cs-07-submitted.png", kind: "phone", label: "Customer Service: Submitted", alt: "Thank-you screen with a Submit Another Request button." },

  /* ---------- Final: Image Recognition concept (15 screens) ---------- */
  "ir-01": { file: "final-ir-01-landing.png", kind: "phone", label: "Image Recognition: Landing (photo layout)", alt: "'Welcome to Report a Problem' with a photo collage, a 'Show Us The Issue' button and Track Your Report." },
  "ir-02": { file: "final-ir-02-photo-options.png", kind: "phone", label: "Image Recognition: Photo options", alt: "Action sheet with Take Photo, Choose From Library, 'No photo? Fill out a form.' and Cancel." },
  "ir-03": { file: "final-ir-03-camera.png", kind: "phone", label: "Image Recognition: Camera", alt: "Camera view with the hint 'Tap the button below to start.'" },
  "ir-04": { file: "final-ir-04-not-recognized.png", kind: "phone", label: "Image Recognition: Image not recognized", alt: "'Image Not Recognized' alert with a Retake button." },
  "ir-05": { file: "final-ir-05-camera-hydrant.png", kind: "phone", label: "Image Recognition: Aiming at a hydrant", alt: "Camera aimed at a fire hydrant spraying water." },
  "ir-06": { file: "final-ir-06-object-outline.png", kind: "phone", label: "Image Recognition: Object outlined and described", alt: "Fire hydrant outlined and labelled, with a short description and Retake / Use Photo." },
  "ir-07": { file: "final-ir-07-details.png", kind: "phone", label: "Image Recognition: Problem details", alt: "Full-page details: photo, Add Photo tile, 'Fire Hydrant', editable address, pre-selected Flooding tag and Submit Report." },
  "ir-08": { file: "final-ir-08-edit-location.png", kind: "phone", label: "Image Recognition: Edit location", alt: "Edit location screen with a search field, a map and Update Location." },
  "ir-09": { file: "final-ir-09-photo-library.png", kind: "phone", label: "Image Recognition: Photo library", alt: "Native photo library picker for adding a second photo." },
  "ir-10": { file: "final-ir-10-camera-second.png", kind: "phone", label: "Image Recognition: Second photo", alt: "Camera view of a green fire hydrant leaking at the base." },
  "ir-11": { file: "final-ir-11-outline-second.png", kind: "phone", label: "Image Recognition: Second photo recognized", alt: "Green fire hydrant outlined and labelled with a short description." },
  "ir-12": { file: "final-ir-12-details-two-photos.png", kind: "phone", label: "Image Recognition: Details with two photos", alt: "Problem details showing two uploaded photos, address, tags and Submit Report." },
  "ir-13": { file: "final-ir-13-thank-you.png", kind: "phone", label: "Image Recognition: Thank you", alt: "Thank-you dialog explaining the user can follow up by uploading their image on the tracking page." },
  "ir-14": { file: "final-ir-14-track-upload.png", kind: "phone", label: "Image Recognition: Track by photo", alt: "Track Your Report: 'Please upload the original photo you submitted with your report.' with an Add Photo area." },
  "ir-15": { file: "final-ir-15-track-status.png", kind: "phone", label: "Image Recognition: Ticket status", alt: "Track Your Report status: Ticket Opened, next steps, the submitted photo and a summary of the flooding fire hydrant report." }
};
