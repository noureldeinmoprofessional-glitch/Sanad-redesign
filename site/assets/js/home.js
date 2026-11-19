/* Sanad homepage: the donation form, the stories, the film and the pinned hero.
   Shared behaviour (language, menu, reveals, counters, toasts) lives in assets/js/site.js. */
(function () {
  "use strict";
  var root = document.documentElement;
  var S = window.Sanad, T = S.T, still = S.still, clamp = S.clamp, head = S.head;

  S.strings({
    ar: {
      cur: "ج.م",
      monthly: function (a) { return "أكون سندًا بـ " + a + " ج.م شهريًا"; },
      once: function (a) { return "تبرّع بـ " + a + " ج.م"; },
      perMonth: "شهريًا", oneTime: "مرة واحدة",
      funds: { children: "تنمية الأطفال", youth: "تمكين الشباب", caregivers: "تدريب مقدّمي الرعاية", kafala: "تدريب الأسر الكافلة", general: "تبرع عام" },
      thanks: function (n) { return "شكرًا لك يا " + n; },
      errAmt: "أقل مبلغ للتبرع 10 ج.م.",
      errName: "اكتب اسمك من فضلك.",
      errPhone: "اكتب رقم موبايل صحيح، مثل 01012345678.",
      filmTitle: "يعني إيه سند؟",
    },
    en: {
      cur: "EGP",
      monthly: function (a) { return "Give EGP " + a + " monthly"; },
      once: function (a) { return "Give EGP " + a; },
      perMonth: "monthly", oneTime: "one-time",
      funds: { children: "Children's development", youth: "Youth empowerment", caregivers: "Caregiver training", kafala: "Kafala family training", general: "General donation" },
      thanks: function (n) { return "Thank you, " + n; },
      errAmt: "The minimum gift is EGP 10.",
      errName: "Please enter your name.",
      errPhone: "Please enter a valid mobile number, like 01012345678.",
      filmTitle: "What does Sanad mean?",
    }
  });

  // ---------- donation form ----------
  var step1 = document.getElementById("step1");
  var step2 = document.getElementById("step2");
  var step3 = document.getElementById("step3");
  var giveBtn = document.getElementById("give-btn");
  var custom = document.getElementById("custom-amt");
  var amtErr = document.getElementById("amt-err");
  var card = document.getElementById("give");

  var fmt = function (n) { return Number(n).toLocaleString("en-US"); };
  var digits = function (s) {
    return String(s || "").replace(/[٠-٩]/g, function (d) { return "٠١٢٣٤٥٦٧٨٩".indexOf(d); }).replace(/[^\d]/g, "");
  };
  function val(name) { var el = step1.querySelector("input[name=" + name + "]:checked"); return el ? el.value : null; }
  function amount() {
    var c = parseInt(digits(custom.value), 10);
    if (c) return c;
    return parseInt(val("amount") || "0", 10);
  }
  function label() {
    var a = fmt(amount() || 0), t = T();
    return val("freq") === "monthly" ? t.monthly(a) : t.once(a);
  }
  function render() {
    giveBtn.textContent = label();
    var t = T();
    document.getElementById("summary").textContent =
      fmt(amount() || 0) + " " + t.cur + " " + (val("freq") === "monthly" ? t.perMonth : t.oneTime) +
      " · " + t.funds[val("fund")];
  }
  step1.addEventListener("change", function (e) {
    if (e.target.name === "amount") { custom.value = ""; amtErr.hidden = true; }
    render();
  });
  custom.addEventListener("input", function () {
    var d = digits(custom.value);
    custom.value = d ? fmt(d) : "";
    if (d) step1.querySelectorAll("input[name=amount]").forEach(function (r) { r.checked = false; });
    else if (!val("amount")) step1.querySelector("input[name=amount][value='500']").checked = true;
    amtErr.hidden = true;
    render();
  });
  step2.addEventListener("change", render);

  function show(step, focusEl) {
    [step1, step2, step3].forEach(function (s) { s.hidden = s !== step; });
    // details and thank-you are taller than the pinned stage, so the hero lets go
    if (step !== step1 && pinned) unpin();
    if (focusEl) focusEl.focus({ preventScroll: true });
    if (card.getBoundingClientRect().top < head.offsetHeight) card.scrollIntoView({ block: "start" });
  }
  function fieldError(input, errEl, msg) {
    input.setAttribute("aria-invalid", msg ? "true" : "false");
    errEl.textContent = msg || "";
    errEl.hidden = !msg;
  }
  step1.addEventListener("submit", function (e) {
    e.preventDefault();
    if (amount() < 10) { amtErr.textContent = T().errAmt; amtErr.hidden = false; custom.focus(); return; }
    render();
    show(step2, document.getElementById("d-name"));
  });
  step2.addEventListener("submit", function (e) {
    e.preventDefault();
    var name = document.getElementById("d-name"), phone = document.getElementById("d-phone");
    var okName = name.value.trim().length > 1, len = digits(phone.value).length, okPhone = len === 0 || (len >= 8 && len <= 15);
    fieldError(name, document.getElementById("name-err"), okName ? "" : T().errName);
    fieldError(phone, document.getElementById("phone-err"), okPhone ? "" : T().errPhone);
    if (!okName) { name.focus(); return; }
    if (!okPhone) { phone.focus(); return; }
    var title = document.getElementById("thanks-title");
    title.textContent = T().thanks(name.value.trim().split(/\s+/)[0]);
    document.getElementById("upsell").hidden = val("freq") !== "once";
    document.getElementById("upsell-done").hidden = true;
    show(step3, title);
  });
  card.addEventListener("click", function (e) {
    if (e.target.closest("[data-back]")) show(step1, giveBtn);
    if (e.target.closest("[data-restart]")) { step2.reset(); render(); show(step1, giveBtn); }
  });
  document.getElementById("make-monthly").addEventListener("click", function () {
    step1.querySelector("input[name=freq][value=monthly]").checked = true;
    document.getElementById("upsell").hidden = true;
    document.getElementById("upsell-done").hidden = false;
    render();
  });

  // Any "give" call-to-action preselects the form and brings it into view
  document.addEventListener("click", function (e) {
    var a = e.target.closest('[data-give-fund], a[href="#give"]');
    if (!a) return;
    e.preventDefault();
    var f = a.getAttribute("data-give-fund");
    if (f) step1.querySelector("input[name=fund][value=" + f + "]").checked = true;
    render();
    show(step1);
    revealForm();
  });

  // ---------- stories: picker, arrows and arrow keys ----------
  var tabs = Array.prototype.slice.call(document.querySelectorAll(".st-picker [role=tab]"));
  var stNow = document.getElementById("st-now");
  function selectTab(tab) {
    tabs.forEach(function (t, i) {
      var on = t === tab, panel = document.getElementById(t.getAttribute("aria-controls"));
      t.setAttribute("aria-selected", String(on));
      t.tabIndex = on ? 0 : -1;
      panel.hidden = !on;
      panel.classList.toggle("enter", on);
      if (on) stNow.textContent = i + 1;
    });
  }
  function step(d) {
    var i = tabs.findIndex(function (t) { return t.getAttribute("aria-selected") === "true"; });
    return tabs[(i + d + tabs.length) % tabs.length];
  }
  tabs.forEach(function (t) {
    t.addEventListener("click", function () { selectTab(t); });
    t.addEventListener("keydown", function (e) {
      if (e.key !== "ArrowLeft" && e.key !== "ArrowRight") return;
      var forward = (e.key === "ArrowLeft") === (root.dir === "rtl");
      var next = step(forward ? 1 : -1);
      next.focus(); selectTab(next);
    });
  });
  document.querySelectorAll("[data-st]").forEach(function (b) {
    b.addEventListener("click", function () { selectTab(step(+b.getAttribute("data-st"))); });
  });
  // the first story makes its entrance the first time the section comes into view
  var storiesEl = document.getElementById("stories");
  if (!still && "IntersectionObserver" in window) {
    var storyIO = new IntersectionObserver(function (en) {
      if (!en[0].isIntersecting) return;
      storiesEl.classList.add("seen");
      var first = storiesEl.querySelector(".story:not([hidden])");
      if (first) first.classList.add("enter");
      storyIO.disconnect();
    }, { threshold: .2 });
    storyIO.observe(storiesEl);
  } else storiesEl.classList.add("seen");

  // ---------- the film: nothing loads from YouTube until the visitor presses play ----------
  var filmDlg = document.getElementById("film-modal"), filmBox = filmDlg.querySelector(".film-player"), filmOpener = null;
  function openFilm(btn) {
    filmOpener = btn;
    var f = document.createElement("iframe");
    f.src = "https://www.youtube-nocookie.com/embed/lNpo7sIex6s?autoplay=1&rel=0&playsinline=1&hl=" + S.lang;
    f.title = T().filmTitle;
    f.allow = "autoplay; encrypted-media; picture-in-picture; fullscreen";
    f.allowFullscreen = true;
    filmBox.appendChild(f);
    if (filmDlg.showModal) filmDlg.showModal(); else filmDlg.setAttribute("open", "");
  }
  function closeFilm() { if (filmDlg.close) filmDlg.close(); else { filmDlg.removeAttribute("open"); filmDlg.dispatchEvent(new Event("close")); } }
  filmDlg.addEventListener("close", function () {
    filmBox.innerHTML = "";
    if (filmOpener) filmOpener.focus({ preventScroll: true });
  });
  filmDlg.addEventListener("click", function (e) {
    if (e.target === filmDlg || e.target.closest("[data-film-close]")) {
      if (e.target.closest("[data-give-fund]")) filmOpener = null;
      closeFilm();
    }
  });
  document.addEventListener("click", function (e) {
    var b = e.target.closest("[data-film]");
    if (b) { e.preventDefault(); openFilm(b); }
  });

  // ---------- what we do: read more ----------
  document.querySelectorAll(".pl-toggle").forEach(function (b) {
    b.addEventListener("click", function () {
      var open = b.getAttribute("aria-expanded") !== "true";
      b.setAttribute("aria-expanded", String(open));
      document.getElementById(b.getAttribute("aria-controls")).classList.toggle("open", open);
    });
  });

  // the hero numbers count up as their stats land
  if (!still) setTimeout(function () {
    document.querySelectorAll(".hero-stats [data-count]").forEach(function (c) { if (!c.dataset.done) { c.dataset.done = "1"; S.countUp(c); } });
  }, 1950);

  // the challenge photo drifts a little against the scroll
  var chSec = document.getElementById("challenge"), chImg = chSec.querySelector(".ch-media img");
  function parallax() {
    var r = chSec.getBoundingClientRect(), vh = innerHeight;
    if (r.bottom < 0 || r.top > vh) return;
    var k = clamp(((r.top + r.height / 2) - vh / 2) / vh * .5 + .5) * 2 - 1;
    chImg.style.setProperty("--py", (k * -chImg.offsetHeight * .035).toFixed(1));
  }

  // ---------- hero: the people Sanad strengthens spiral into view, then swirl away and open onto the form ----------
  var heroEl = document.getElementById("hero"), stage = heroEl.querySelector(".hero-stage"), copyEl = heroEl.querySelector(".hero-copy");
  var art = heroEl.querySelector(".hv-art"), mainPh = art.querySelector(".hv-main"), sats = art.querySelectorAll(".hv-sat");
  var linkPath = art.querySelector(".hv-path path"), vortex = art.querySelector(".hv-vortex"), vPath = vortex.querySelector("path");
  var blobs = art.querySelectorAll(".hv-blob"), slot = heroEl.querySelector(".form-slot");
  // resting places, as fractions of the art box (RTL); on phones the art is full width, so the photos keep clear of the screen edge
  var SAT_WIDE = [[.80, .19], [.90, .49], [.80, .79]], SAT_NARROW = [[.74, .2], [.83, .5], [.74, .8]], SAT = SAT_WIDE;
  var INTRO_MS = 4200;
  var geo = null, pinned = false, unpinned = false, introT0 = null, heroP = 0, shownP = 0, linkLen = 0, fs = 1, painting = false, focusWhenOpen = false;
  var easeInOut = function (k) { return k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2; };
  function seg(t, a, b) { return easeInOut(clamp((t - a) / (b - a))); }
  function stageH() { return innerHeight - head.offsetHeight; }
  heroEl.classList.add("js");

  function catmull(p) {
    var d = "M" + p[0][0].toFixed(1) + " " + p[0][1].toFixed(1);
    for (var i = 0; i < p.length - 1; i++) {
      var a = p[i - 1] || p[i], b = p[i], c = p[i + 1], e = p[i + 2] || c;
      d += " C" + [b[0] + (c[0] - a[0]) / 6, b[1] + (c[1] - a[1]) / 6, c[0] - (e[0] - b[0]) / 6, c[1] - (e[1] - b[1]) / 6, c[0], c[1]]
        .map(function (n) { return n.toFixed(1); }).join(" ");
    }
    return d;
  }
  function layoutArt() {
    var W = art.clientWidth, H = art.clientHeight;
    if (!W || !H) { geo = null; return; }
    SAT = innerWidth > 960 ? SAT_WIDE : SAT_NARROW;
    var rtl = root.dir === "rtl", fx = function (f) { return rtl ? f * W : (1 - f) * W; }, pts = [];
    geo = { cx: fx(.52), cy: H * .5, sat: [] };
    sats.forEach(function (sat, i) {
      var x = fx(SAT[i][0]), y = SAT[i][1] * H;
      geo.sat.push({ R: Math.hypot(x - geo.cx, y - geo.cy), a: Math.atan2(y - geo.cy, x - geo.cx), sz: sat.offsetWidth });
      pts.push([x, y]);
    });
    // the hand-drawn line enters above the first photo and leaves below the last
    var side = rtl ? 1 : -1;
    pts.unshift([pts[0][0] + side * W * .07, -H * .04]);
    pts.push([pts[pts.length - 1][0] + side * W * .09, H * 1.04]);
    linkPath.parentNode.setAttribute("viewBox", "0 0 " + W + " " + H);
    linkPath.setAttribute("d", catmull(pts));
    linkLen = linkPath.getTotalLength();
    linkPath.style.strokeDasharray = linkLen;
    var vs = W; // the spiral is as wide as the art box (100cqw)
    vortex.style.left = (geo.cx - vs / 2).toFixed(1) + "px";
    vortex.style.top = (geo.cy - vs / 2).toFixed(1) + "px";
    mainPh.style.setProperty("--cx", ((rtl ? .52 / .76 : .24 / .76) * 100).toFixed(1) + "%");
  }
  function decideMode() {
    heroEl.style.setProperty("--stage-h", stageH() + "px");
    var want = !still && !unpinned && innerWidth > 960;
    heroEl.classList.toggle("is-pin", want);
    if (want) {
      fs = Math.min(1, (stageH() - 32) / card.offsetHeight);
      if (fs < .74 || copyEl.scrollHeight > copyEl.clientHeight + 2) want = false;
    }
    heroEl.classList.toggle("is-pin", want);
    pinned = want;
    if (!pinned) { slot.inert = false; slot.style.clipPath = slot.style.opacity = card.style.transform = ""; heroP = shownP = 0; }
    layoutArt();
    heroScroll();
    paint();
  }
  function unpin() { unpinned = true; heroEl.classList.add("released"); decideMode(); }
  function heroScroll() {
    if (!pinned) return;
    heroP = clamp((scrollY + head.offsetHeight - heroEl.offsetTop) / (heroEl.offsetHeight - stageH()));
  }
  // the scroll position at which the form has fully opened
  function revealForm() {
    var how = still ? "auto" : "smooth";
    if (pinned) {
      scrollTo({ top: heroEl.offsetTop - head.offsetHeight + (heroEl.offsetHeight - stageH()) * .78, behavior: how });
      focusWhenOpen = true; // focus lands once the form has opened
      requestPaint();
    } else {
      card.scrollIntoView({ behavior: how, block: "start" });
      card.focus({ preventScroll: true });
    }
  }
  function paint() {
    var it = introT0 === null ? 0 : still ? 1 : clamp((performance.now() - introT0) / INTRO_MS);
    var p = pinned ? shownP : 0, rtl = root.dir === "rtl", spin = rtl ? -1 : 1;
    stage.style.setProperty("--p", p.toFixed(3));
    if (pinned) {
      var f = seg(p, .4, .7);
      slot.style.clipPath = f >= 1 ? "none" : "circle(" + (75 * f).toFixed(2) + "% at " + (rtl ? 52 : 48) + "% 50%)";
      slot.style.opacity = Math.min(1, f * 1.8).toFixed(3);
      card.style.transform = "translate(-50%, calc(-50% + " + (36 * (1 - f)).toFixed(1) + "px)) scale(" + (fs * (.9 + .1 * f)).toFixed(3) + ")";
      slot.inert = f < .5;
      if (focusWhenOpen && !slot.inert) { focusWhenOpen = false; card.focus({ preventScroll: true }); }
    }
    if (!geo) return;
    // the main photo opens out of the spiral's centre, and later collapses back into it
    var mIn = seg(it, .02, .5), mOut = seg(p, .14, .52);
    mainPh.style.clipPath = "circle(" + (75 * mIn * (1 - mOut)).toFixed(2) + "% at var(--cx) 50%)";
    mainPh.style.transform = "rotate(" + (spin * 16 * mOut).toFixed(2) + "deg) scale(" + (1.1 - .1 * mIn - .14 * mOut).toFixed(3) + ")";
    mainPh.style.opacity = (1 - .35 * mOut).toFixed(3);
    // three photos spiral out of the centre into place, then swirl outward and away
    sats.forEach(function (sat, i) {
      var g = geo.sat[i], e1 = seg(it, .18 + .1 * i, .7 + .1 * i), e2 = seg(p, .02 + .06 * i, .4 + .06 * i);
      var a = g.a + spin * (-1.6 * Math.PI * (1 - e1) + 1.3 * Math.PI * e2), R = g.R * e1 * (1 + 1.15 * e2);
      var x = geo.cx + Math.cos(a) * R - g.sz / 2, y = geo.cy + Math.sin(a) * R - g.sz / 2;
      sat.style.transform = "translate(" + x.toFixed(1) + "px," + y.toFixed(1) + "px) rotate(" + (spin * (-120 * (1 - e1) + 150 * e2)).toFixed(1) +
        "deg) scale(" + ((.35 + .65 * e1) * (1 - .55 * e2)).toFixed(3) + ")";
      sat.style.opacity = (Math.min(1, e1 * 1.4) * (1 - e2)).toFixed(3);
    });
    // the line that joins them draws in last and is the first thing to go
    var lIn = seg(it, .62, 1), lOut = seg(p, 0, .16);
    linkPath.style.strokeDashoffset = (linkLen * (1 - lIn + lOut)).toFixed(1);
    // the spiral itself shows only while things are moving through it
    var vIn = seg(it, 0, .42), vEx = seg(p, .16, .46);
    vortex.style.opacity = Math.max(.5 * vIn * (1 - seg(it, .45, .85)), .45 * vEx * (1 - seg(p, .5, .64))).toFixed(3);
    vPath.style.strokeDashoffset = (1 - Math.max(it < 1 ? vIn : 0, vEx)).toFixed(3);
    vortex.style.transform = "rotate(" + (spin * (200 * it + 300 * p)).toFixed(1) + "deg)";
    blobs.forEach(function (b, i) {
      var e1 = seg(it, .4 + .08 * i, .85 + .08 * i), e2 = seg(p, .05, .4);
      b.style.transform = "translate(" + (spin * 90 * e2).toFixed(1) + "px," + (120 * e2).toFixed(1) + "px) rotate(" +
        (spin * (-30 * (1 - e1) + 25 * e2)).toFixed(1) + "deg) scale(" + (.4 + .6 * e1).toFixed(3) + ")";
      b.style.opacity = (Math.min(1, e1 * 1.5) * (1 - e2)).toFixed(3);
    });
  }
  function requestPaint() {
    if (painting) return;
    painting = true;
    requestAnimationFrame(function () {
      painting = false;
      var gap = heroP - shownP;
      shownP = Math.abs(gap) < .0005 ? heroP : shownP + gap * .09;
      paint();
      if (shownP !== heroP) requestPaint();
    });
  }
  function introLoop() { paint(); if (performance.now() - introT0 < INTRO_MS + 100) requestAnimationFrame(introLoop); }
  function startIntro() { if (introT0 !== null) return; introT0 = performance.now(); if (still) paint(); else introLoop(); }
  if (!still && "IntersectionObserver" in window) {
    var heroIO = new IntersectionObserver(function (en) { if (en[0].isIntersecting) { startIntro(); heroIO.disconnect(); } }, { threshold: .3 });
    heroIO.observe(art);
  } else startIntro();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { decideMode(); });

  // ---------- scroll: the hero and the sticky mobile donate bar ----------
  var sticky = document.getElementById("sticky");
  function onScroll() {
    var vh = innerHeight, headH = head.offsetHeight;
    root.style.setProperty("--head-h", headH + "px");
    heroScroll();
    requestPaint();
    if (!still) parallax();
    // shown whenever the form is out of view, once the visitor has started scrolling
    var cr = card.getBoundingClientRect();
    var off = scrollY > 120 && (cr.bottom < headH || cr.top > vh);
    sticky.classList.toggle("show", off);
    sticky.setAttribute("aria-hidden", String(!off));
    sticky.querySelectorAll("a").forEach(function (a) { a.tabIndex = off ? 0 : -1; });
  }
  addEventListener("scroll", onScroll, { passive: true });
  addEventListener("resize", function () { decideMode(); onScroll(); });
  onScroll();

  // on every language change (and once now): relabel the form, re-split the hero headline, re-lay the hero
  var heroTitle = document.getElementById("hero-title");
  S.onLang(function () {
    render();
    if (!still) S.splitWords(heroTitle, "hw", false);
    decideMode();
    onScroll();
  });
})();
