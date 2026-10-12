(function () {
  "use strict";

  var ASSETS = window.CASE_STUDY_ASSETS || {};
  var CONFIG = window.CASE_STUDY_CONFIG || {};
  var IMAGE_DIR = "assets/images/";

  var KIND_HINT = {
    phone: "Mobile screen · approx. 1170 × 2532 px",
    crop: "Cropped mobile screen · approx. 9:16",
    board: "Board / artifact · 16:10, at least 1600 px wide",
    wide: "Showcase · 16:9, at least 2000 px wide",
    sketch: "Sketch photo · 4:5, at least 1200 px tall"
  };

  /* ------------------------------------------------------------
   * Image placeholders
   * Each .ph[data-asset] shows a labelled placeholder until the
   * matching file exists in /assets/images/, then swaps to the image.
   * ---------------------------------------------------------- */
  function el(tag, cls, text) {
    var node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text) node.textContent = text;
    return node;
  }

  function renderPlaceholder(slot) {
    var id = slot.getAttribute("data-asset");
    var asset = ASSETS[id];

    if (!asset) {
      slot.classList.add("ph--phone", "ph--missing");
      slot.appendChild(el("span", "ph__label", "Unknown asset id: " + id));
      return;
    }

    var kind = slot.getAttribute("data-kind") || asset.kind || "phone";
    slot.classList.add("ph--" + kind);
    slot.setAttribute("role", "img");
    slot.setAttribute("aria-label", "Image placeholder: " + asset.label);

    var inner = el("span", "ph__inner");
    inner.setAttribute("aria-hidden", "true");
    inner.appendChild(el("span", "ph__tag", "Image needed"));
    inner.appendChild(el("span", "ph__label", asset.label));
    if (asset.note && !slot.hasAttribute("data-compact")) {
      inner.appendChild(el("span", "ph__note", asset.note));
    }
    inner.appendChild(el("span", "ph__file", asset.file));
    if (!slot.hasAttribute("data-compact")) {
      inner.appendChild(el("span", "ph__hint", KIND_HINT[kind] || ""));
    }
    slot.appendChild(inner);

    // Try the real image; swap only if it loads.
    var probe = new Image();
    probe.onload = function () {
      var img = el("img", "ph__img");
      img.src = probe.src;
      img.alt = asset.alt || asset.label;
      img.width = probe.naturalWidth;
      img.height = probe.naturalHeight;
      img.loading = "lazy";
      img.decoding = "async";
      slot.removeAttribute("role");
      slot.removeAttribute("aria-label");
      slot.classList.add("ph--loaded");
      slot.textContent = "";
      slot.appendChild(img);
    };
    probe.src = IMAGE_DIR + asset.file;
  }

  document.querySelectorAll(".ph[data-asset]").forEach(renderPlaceholder);

  /* ------------------------------------------------------------
   * Figma prototype blocks
   * ---------------------------------------------------------- */
  function isFigmaUrl(url) {
    return /^https:\/\/([\w-]+\.)?figma\.com\//.test(url || "");
  }

  document.querySelectorAll("[data-figma]").forEach(function (block) {
    var key = block.getAttribute("data-figma");
    var cfg = (CONFIG.figma || {})[key] || {};
    var link = block.querySelector("[data-figma-link]");
    var loadBtn = block.querySelector("[data-figma-load]");
    var status = block.querySelector("[data-figma-status]");
    var stage = block.querySelector(".proto__stage");
    var configured = isFigmaUrl(cfg.url);

    if (configured) {
      link.href = cfg.url;
      link.removeAttribute("aria-disabled");
      link.classList.remove("is-disabled");
      if (status) status.hidden = true;
    } else {
      link.removeAttribute("href");
      link.setAttribute("aria-disabled", "true");
      link.classList.add("is-disabled");
      if (status) status.hidden = false;
    }

    if (!loadBtn) return;
    if (!configured || cfg.embed === false) {
      loadBtn.hidden = true;
      return;
    }
    loadBtn.hidden = false;
    loadBtn.addEventListener("click", function () {
      var frame = document.createElement("iframe");
      frame.className = "proto__iframe";
      frame.title = cfg.title || "Figma prototype";
      frame.src =
        "https://www.figma.com/embed?embed_host=share&url=" +
        encodeURIComponent(cfg.url);
      frame.setAttribute("allowfullscreen", "");
      frame.loading = "lazy";
      stage.classList.add("is-embedded");
      stage.textContent = "";
      stage.appendChild(frame);
      loadBtn.hidden = true;
      frame.focus();
    });
  });

  /* ------------------------------------------------------------
   * Mockup frame style: detailed phone or simple frame
   * ---------------------------------------------------------- */
  var FRAME_KEY = "dcwater-mockup-frame";
  var frameButtons = document.querySelectorAll("[data-frame-option]");

  function applyFrame(style) {
    if (style !== "simple") style = "detailed";
    document.documentElement.setAttribute("data-frame", style);
    frameButtons.forEach(function (btn) {
      btn.setAttribute("aria-pressed", String(btn.getAttribute("data-frame-option") === style));
    });
  }

  var savedFrame = null;
  try { savedFrame = localStorage.getItem(FRAME_KEY); } catch (e) { /* storage unavailable */ }
  applyFrame(savedFrame || CONFIG.mockupFrame);

  frameButtons.forEach(function (btn) {
    btn.addEventListener("click", function () {
      var style = btn.getAttribute("data-frame-option");
      applyFrame(style);
      try { localStorage.setItem(FRAME_KEY, style); } catch (e) { /* storage unavailable */ }
    });
  });

  /* ------------------------------------------------------------
   * Reflection notebook: one reflection per page, page-turn animation
   * ---------------------------------------------------------- */
  document.querySelectorAll("[data-notebook]").forEach(function (book) {
    var pages = Array.prototype.slice.call(book.querySelectorAll(".nb-page"));
    var prev = book.querySelector("[data-nb-prev]");
    var next = book.querySelector("[data-nb-next]");
    var tabs = Array.prototype.slice.call(book.querySelectorAll("[data-nb-go]"));
    var status = book.querySelector("[data-nb-status]");
    var stage = book.querySelector(".notebook__pages");
    var current = 0;
    if (!pages.length) return;

    function render(announce) {
      pages.forEach(function (page, k) {
        var flipped = k < current;
        page.classList.toggle("is-flipped", flipped);
        // Unflipped pages stack top-down; flipped pages sit above but are hidden.
        page.style.zIndex = flipped ? String(200 + k) : String(100 - k);
        var isCurrent = k === current;
        page.setAttribute("aria-hidden", String(!isCurrent));
        page.inert = !isCurrent;
      });
      prev.disabled = current === 0;
      next.disabled = current === pages.length - 1;
      tabs.forEach(function (tab, k) {
        if (k === current) tab.setAttribute("aria-current", "true");
        else tab.removeAttribute("aria-current");
      });
      if (announce && status) {
        var title = pages[current].querySelector(".nb-page__title");
        status.textContent = "Page " + (current + 1) + " of " + pages.length + ": " + (title ? title.textContent : "");
      }
    }

    function go(index) {
      index = Math.max(0, Math.min(pages.length - 1, index));
      if (index === current) return;
      current = index;
      render(true);
    }

    prev.addEventListener("click", function () { go(current - 1); });
    next.addEventListener("click", function () { go(current + 1); });
    tabs.forEach(function (tab) {
      tab.addEventListener("click", function () { go(Number(tab.getAttribute("data-nb-go"))); });
    });
    stage.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight" || e.key === "ArrowDown" || e.key === "PageDown") { e.preventDefault(); go(current + 1); }
      if (e.key === "ArrowLeft" || e.key === "ArrowUp" || e.key === "PageUp") { e.preventDefault(); go(current - 1); }
    });
    // Clicking the folded corner of the current page turns it.
    stage.addEventListener("click", function (e) {
      var rect = stage.getBoundingClientRect();
      if (e.clientX > rect.right - 48 && e.clientY > rect.bottom - 48) go(current + 1);
    });

    book.classList.add("is-ready");
    render(false);
  });

  /* ------------------------------------------------------------
   * Back to projects links
   * ---------------------------------------------------------- */
  document.querySelectorAll("[data-back-link]").forEach(function (a) {
    a.href = CONFIG.backToProjectsUrl || "#";
  });

  /* ------------------------------------------------------------
   * Section navigation: mobile toggle + current-section highlight
   * ---------------------------------------------------------- */
  var nav = document.querySelector(".secnav");
  var toggle = document.querySelector(".secnav__toggle");
  var list = document.getElementById("secnav-list");
  var currentLabel = document.querySelector(".secnav__current");

  function setOpen(open) {
    if (!toggle) return;
    toggle.setAttribute("aria-expanded", String(open));
    nav.classList.toggle("is-open", open);
  }

  if (toggle) {
    toggle.addEventListener("click", function () {
      setOpen(toggle.getAttribute("aria-expanded") !== "true");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("is-open")) {
        setOpen(false);
        toggle.focus();
      }
    });
    document.addEventListener("click", function (e) {
      if (!nav.contains(e.target)) setOpen(false);
    });
  }

  var links = list ? Array.prototype.slice.call(list.querySelectorAll("a")) : [];
  links.forEach(function (a) {
    a.addEventListener("click", function () { setOpen(false); });
  });

  var sections = links
    .map(function (a) { return document.querySelector(a.getAttribute("href")); })
    .filter(Boolean);

  function markCurrent(id) {
    links.forEach(function (a) {
      var on = a.getAttribute("href") === "#" + id;
      if (on) {
        a.setAttribute("aria-current", "true");
        if (currentLabel) currentLabel.textContent = a.textContent;
      } else {
        a.removeAttribute("aria-current");
      }
    });
  }

  if ("IntersectionObserver" in window && sections.length) {
    var visible = {};
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          visible[entry.target.id] = entry.isIntersecting;
        });
        for (var i = 0; i < sections.length; i++) {
          if (visible[sections[i].id]) {
            markCurrent(sections[i].id);
            return;
          }
        }
      },
      { rootMargin: "-30% 0px -60% 0px" }
    );
    sections.forEach(function (s) { io.observe(s); });
  }
})();
