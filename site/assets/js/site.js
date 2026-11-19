/* Sanad site: what every page shares. The language switch, the main menu, toasts, the footer newsletter,
   copy buttons, section headlines and scroll reveals. A page adds its own strings with Sanad.strings()
   and its own behaviour with Sanad.onLang(); see assets/js/home.js. */
(function () {
  "use strict";
  var root = document.documentElement;
  var S = window.Sanad = { lang: "ar" };
  var hooks = [];

  // ---------- i18n: Arabic is in the markup, English lives in data-en* attributes ----------
  var TEXT = {
    ar: {
      langBtn: "English",
      copied: "تم النسخ",
      subscribed: "شكرًا لاشتراكك في نشرة سند!",
      badEmail: "اكتب بريدًا إلكترونيًا صحيحًا."
    },
    en: {
      langBtn: "العربية",
      copied: "Copied",
      subscribed: "Thanks for subscribing to Sanad's newsletter!",
      badEmail: "Please enter a valid email address."
    }
  };
  S.strings = function (t) {
    Object.keys(t).forEach(function (l) { Object.keys(t[l]).forEach(function (k) { TEXT[l][k] = t[l][k]; }); });
  };
  S.T = function () { return TEXT[S.lang]; };
  // a page's own work on every language change; it also runs once right away, for the language already shown
  S.onLang = function (fn) { hooks.push(fn); fn(S.lang); };

  S.still = matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!S.still) root.classList.add("anim");
  S.clamp = function (v) { return v < 0 ? 0 : v > 1 ? 1 : v; };
  S.head = document.querySelector(".site-head");

  function swap(attr, setter) {
    document.querySelectorAll("[" + attr + "]").forEach(function (el) {
      var key = "ar" + attr.replace(/^data-en/, "").replace(/-/g, "");
      if (!(key in el.dataset)) el.dataset[key] = setter.get(el);
      setter.set(el, S.lang === "en" ? el.getAttribute(attr) : el.dataset[key]);
    });
  }
  function applyLang(next) {
    S.lang = next;
    root.lang = S.lang;
    root.dir = S.lang === "ar" ? "rtl" : "ltr";
    // the <title> carries its English in data-en too, so this also renames the tab
    swap("data-en", { get: function (e) { return e.textContent; }, set: function (e, v) { e.textContent = v; } });
    swap("data-en-html", { get: function (e) { return e.innerHTML; }, set: function (e, v) { e.innerHTML = v; } });
    swap("data-en-ph", { get: function (e) { return e.placeholder; }, set: function (e, v) { e.placeholder = v; } });
    swap("data-en-aria", { get: function (e) { return e.getAttribute("aria-label"); }, set: function (e, v) { e.setAttribute("aria-label", v); } });
    swap("data-en-alt", { get: function (e) { return e.alt; }, set: function (e, v) { e.alt = v; } });
    swap("data-en-src", { get: function (e) { return e.getAttribute("src"); }, set: function (e, v) { e.src = v; } });
    swap("data-en-href", { get: function (e) { return e.getAttribute("href"); }, set: function (e, v) { e.setAttribute("href", v); } });
    // long texts that differ in shape between the languages (an article, a list) come as two blocks
    document.querySelectorAll("[data-ar-only]").forEach(function (e) { e.hidden = S.lang !== "ar"; });
    document.querySelectorAll("[data-en-only]").forEach(function (e) { e.hidden = S.lang !== "en"; });
    document.querySelectorAll("[data-lang-toggle]").forEach(function (b) {
      // the header's compact button shows a short code; the menu's button spells the language out
      if (b.hasAttribute("data-lang-short")) {
        b.querySelector("span").textContent = S.lang === "ar" ? "EN" : "ع";
        b.setAttribute("aria-label", S.lang === "ar" ? "Switch to English" : "التبديل إلى العربية");
      } else b.textContent = S.T().langBtn;
      b.lang = S.lang === "ar" ? "en" : "ar";
    });
    fitNav();
    splitSectionHeads();
    hooks.forEach(function (fn) { fn(S.lang); });
    try { localStorage.setItem("sanad-lang", S.lang); } catch (e) {}
  }
  document.querySelectorAll("[data-lang-toggle]").forEach(function (b) {
    b.addEventListener("click", function () { applyLang(S.lang === "ar" ? "en" : "ar"); });
  });

  // ---------- main menu (Sanad's own tabs, dropdowns included) ----------
  var siteHead = S.head;
  var headRow = siteHead.querySelector(".head-row");
  var navEl = document.getElementById("site-nav");
  var menuBtn = document.querySelector(".menu-btn");
  var subBtns = navEl.querySelectorAll("[aria-controls^='nav-sub']");
  var isCompact = function () { return siteHead.classList.contains("nav-compact"); };
  function setSub(btn, open) {
    var item = btn.closest(".nav-item");
    btn.setAttribute("aria-expanded", String(open));
    item.classList.toggle("open", open);
    if (open && !isCompact()) placeSub(item);
  }
  // centre the panel under its tab and keep it 16px inside the window
  function placeSub(item) {
    var sub = item.querySelector(".nav-sub"), tab = item.querySelector(".nav-top");
    sub.style.setProperty("--dx", "0px");
    var r = sub.getBoundingClientRect(), t = tab.getBoundingClientRect();
    var left = Math.min(Math.max(t.left + t.width / 2 - r.width / 2, 16), root.clientWidth - 16 - r.width);
    sub.style.setProperty("--dx", Math.round(left - r.left) + "px");
  }
  navEl.querySelectorAll(".sub-links").forEach(function (ul) {
    Array.prototype.forEach.call(ul.children, function (li, i) { li.style.setProperty("--i", i); });
  });
  function closeSubs(except) { subBtns.forEach(function (b) { if (b !== except) setSub(b, false); }); }
  function setMenu(open) {
    menuBtn.setAttribute("aria-expanded", String(open));
    siteHead.classList.toggle("nav-open", open);
    if (!open) closeSubs();
  }
  S.closeMenu = function () { setMenu(false); };
  // fold the tabs into the menu button whenever they can't share the row with the actions
  function fitNav() {
    siteHead.classList.remove("nav-compact");
    var list = navEl.firstElementChild;
    var fold = innerWidth <= 1100 || headRow.scrollWidth > headRow.clientWidth + 1 || list.scrollWidth > navEl.clientWidth + 1;
    siteHead.classList.toggle("nav-compact", fold);
    if (!fold) setMenu(false);
    closeSubs();
  }
  subBtns.forEach(function (b) {
    var item = b.closest(".nav-item"), t;
    b.addEventListener("click", function () {
      // a mouse that just opened the panel by hovering shouldn't close it again by clicking
      if (item.dataset.hover) { delete item.dataset.hover; return; }
      navEl.classList.remove("instant");
      var open = b.getAttribute("aria-expanded") !== "true";
      closeSubs(b);
      setSub(b, open);
    });
    item.addEventListener("pointerenter", function (e) {
      if (e.pointerType !== "mouse" || isCompact()) return;
      clearTimeout(t);
      // moving from one open panel to the next swaps them in place instead of replaying the entrance
      var other = navEl.querySelector(".nav-item.open");
      navEl.classList.toggle("instant", !!other && other !== item);
      if (b.getAttribute("aria-expanded") !== "true") { closeSubs(b); setSub(b, true); item.dataset.hover = "1"; }
    });
    item.addEventListener("pointerleave", function (e) {
      if (e.pointerType !== "mouse" || isCompact()) return;
      t = setTimeout(function () { delete item.dataset.hover; setSub(b, false); }, 220);
    });
    item.addEventListener("focusout", function (e) {
      if (!isCompact() && !item.contains(e.relatedTarget)) setSub(b, false);
    });
  });
  menuBtn.addEventListener("click", function () { setMenu(menuBtn.getAttribute("aria-expanded") !== "true"); });
  navEl.addEventListener("click", function (e) { if (e.target.closest("a")) setMenu(false); });
  document.addEventListener("click", function (e) {
    if (siteHead.contains(e.target)) return;
    closeSubs();
    if (isCompact()) setMenu(false);
  });
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    var open = navEl.querySelector("[aria-controls^='nav-sub'][aria-expanded='true']");
    if (open) { setSub(open, false); open.focus(); }
    else if (menuBtn.getAttribute("aria-expanded") === "true") { setMenu(false); menuBtn.focus(); }
  });
  addEventListener("resize", fitNav);
  if (document.fonts) document.fonts.ready.then(fitNav);
  fitNav();

  // ---------- toasts and copy buttons ----------
  var toastTimer;
  S.toast = function (msg) {
    var t = document.querySelector(".toast");
    if (!t) { t = document.createElement("div"); t.className = "toast"; t.setAttribute("role", "status"); document.body.appendChild(t); }
    t.textContent = msg; t.hidden = false;
    clearTimeout(toastTimer); toastTimer = setTimeout(function () { t.hidden = true; }, 1800);
  };
  function copyText(text, fallbackEl) {
    var done = function () { S.toast(S.T().copied); };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, function () { selectEl(fallbackEl); });
    } else selectEl(fallbackEl);
  }
  function selectEl(el) {
    if (!el) return;
    var r = document.createRange(); r.selectNodeContents(el);
    var s = getSelection(); s.removeAllRanges(); s.addRange(r);
  }
  document.addEventListener("click", function (e) {
    var b = e.target.closest("[data-copy]");
    if (b) copyText(b.getAttribute("data-copy"), b.parentElement.querySelector("code"));
    if (e.target.closest("[data-copy-link]")) copyText(location.href.split("#")[0], null);
  });

  // ---------- newsletter ----------
  var nl = document.getElementById("newsletter");
  if (nl) nl.addEventListener("submit", function (e) {
    e.preventDefault();
    var email = document.getElementById("nl-email");
    S.toast(/^\S+@\S+\.\S+$/.test(email.value) ? S.T().subscribed : S.T().badEmail);
  });

  // ---------- headlines ----------
  // Words rise one by one (whole words, so Arabic letters stay joined).
  // Section headlines rise out of a mask, so each word gets an inner span.
  S.splitWords = function (h, cls, masked) {
    var i = 0;
    (function walk(node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (n) {
        if (n.nodeType === 3) {
          var frag = document.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(function (part) {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(part)); return; }
            var w = document.createElement("span");
            w.className = cls; w.style.setProperty("--i", i++);
            if (masked) { var inner = document.createElement("span"); inner.textContent = part; w.appendChild(inner); }
            else w.textContent = part;
            frag.appendChild(w);
          });
          node.replaceChild(frag, n);
        } else if (n.nodeType === 1 && !n.classList.contains(cls)) walk(n);
      });
    })(h);
  };
  function splitSectionHeads() {
    if (S.still) return;
    document.querySelectorAll(".sec-head h2").forEach(function (h) { if (!h.closest(".hero")) S.splitWords(h, "sw", true); });
  }

  // ---------- page-wide reveals and counters ----------
  var revealSel = ".sec-head, .trust li, .marquee, .p-count, .ch-media, .ch-stats li, .ch-note, .pillar, .p-card, .multiply, .impact-grid li, .st-picker button, .bank, .way, .inv, .news a, .head-split > a, [data-rv]";
  document.querySelectorAll(revealSel).forEach(function (el) {
    if (el.closest(".hero")) return;
    el.setAttribute("data-reveal", "");
    var sibs = Array.prototype.filter.call(el.parentElement.children, function (x) { return x.matches(revealSel); });
    el.style.setProperty("--d", (Math.max(0, sibs.indexOf(el)) * .09).toFixed(2) + "s");
  });
  // counts up to the number as written, keeping its decimals and any suffix such as "+"
  S.countUp = function (el) {
    var m = el.textContent.trim().match(/^([\d,]+(?:\.\d+)?)(.*)$/);
    if (!m) return;
    var end = parseFloat(m[1].replace(/,/g, "")), dec = (m[1].split(".")[1] || "").length, t0 = performance.now();
    var opt = { minimumFractionDigits: dec, maximumFractionDigits: dec };
    (function step(now) {
      var k = S.clamp((now - t0) / 1600), e = 1 - Math.pow(1 - k, 3);
      el.textContent = (end * e).toLocaleString("en-US", opt) + m[2];
      if (k < 1) requestAnimationFrame(step);
    })(t0);
  };
  if (!S.still && "IntersectionObserver" in window) {
    var watch = new Map();
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        watch.get(e.target).forEach(function (el) {
          el.classList.add("in");
          el.querySelectorAll("[data-count]").forEach(function (c) { if (!c.dataset.done) { c.dataset.done = "1"; S.countUp(c); } });
          setTimeout(function () { el.classList.add("done"); }, 2000 + (parseFloat(el.style.getPropertyValue("--d")) || 0) * 1000);
        });
        io.unobserve(e.target);
      });
    }, { threshold: .14, rootMargin: "0px 0px -6% 0px" });
    document.querySelectorAll("[data-reveal]").forEach(function (el) {
      // a card that starts fully clipped never registers as visible, so its row is watched instead
      var target = el.matches(".inv") ? el.parentElement : el;
      if (!watch.has(target)) { watch.set(target, []); io.observe(target); }
      watch.get(target).push(el);
    });
  } else {
    document.querySelectorAll("[data-reveal]").forEach(function (el) { el.classList.add("in", "done"); });
  }

  // ?lang=en opens the English version directly; otherwise use the last choice
  var saved = new URLSearchParams(location.search).get("lang");
  if (!saved) { try { saved = localStorage.getItem("sanad-lang"); } catch (e) {} }
  applyLang(saved === "en" ? "en" : "ar");
})();
