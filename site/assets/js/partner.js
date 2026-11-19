/* The partnership form, on every page: "Corporate & Donor Partnerships" in the menu and the homepage card open it,
   and so does a link to /#partner. It checks each answer and shows a thank-you; nothing is sent yet. */
(function () {
  "use strict";
  var root = document.documentElement;
  var S = window.Sanad, T = S.T, still = S.still;
  if (!document.getElementById("partner-form")) return;

  S.strings({
    ar: {
      pfRequired: "هذا الحقل مطلوب.",
      pfPhone: "اكتب رقم هاتف صحيح.",
      pfPick: "اختر خيارًا واحدًا على الأقل.",
      pfOther: "اكتب الخيار الآخر.",
      pfThanks: function (org) { return "شكرًا لكم، " + org + "!"; },
      pfDone: function (email) { return "يسعدنا اهتمامكم بالشراكة مع سند. وصلتنا استمارتكم، وسيتواصل معكم فريق الشراكات قريبًا على " + email + " لنستكشف معًا فرص التعاون."; }
    },
    en: {
      pfRequired: "This field is required.",
      pfPhone: "Please enter a valid phone number.",
      pfPick: "Choose at least one option.",
      pfOther: "Please describe the other option.",
      pfThanks: function (org) { return "Thank you, " + org + "!"; },
      pfDone: function (email) { return "We're delighted you'd like to partner with Sanad. Your form has reached us, and our partnerships team will be in touch soon at " + email + " to explore how we can work together."; }
    }
  });

  // ---------- partnership form ----------
  var pf = document.getElementById("partner-form");
  var pfForm = document.getElementById("pf-form");
  var pfDone = document.getElementById("pf-done");
  var pfOpener = null;
  function pfReset() {
    pfForm.reset();
    pfForm.hidden = false;
    pfDone.hidden = true;
    pf.setAttribute("aria-labelledby", "pf-title");
    pf.classList.remove("is-done");
    pfForm.querySelectorAll(".err").forEach(function (e) { e.hidden = true; e.textContent = ""; });
    pfForm.querySelectorAll("[aria-invalid]").forEach(function (e) { e.removeAttribute("aria-invalid"); });
  }
  function pfOpen(opener) {
      pfOpener = opener;
      if (S.closeMenu) S.closeMenu();
      pfReset();
      pf.showModal();
      root.classList.add("pf-lock");
      pfForm.querySelector(".pf-body").scrollTop = 0;
      document.getElementById("pf-org").focus();
  }
  document.querySelectorAll("[data-open-partner]").forEach(function (b) {
    b.addEventListener("click", function (e) { e.preventDefault(); pfOpen(b); });
  });
  // a link to /#partner (the menu without JavaScript, or a shared link) opens the form on arrival
  function fromHash() { if (location.hash === "#partner" && !pf.open) pfOpen(null); }
  fromHash();
  addEventListener("hashchange", fromHash);
  pf.addEventListener("close", function () {
    root.classList.remove("pf-lock");
    if (!pfOpener) return;
    // opened from the menu: the link is folded away again, so focus returns to its tab (or the menu button on phones)
    var back = pfOpener;
    if (!back.offsetParent) {
      var tab = back.closest(".nav-item") && back.closest(".nav-item").querySelector(".nav-top");
      var menuBtn = document.querySelector(".menu-btn");
      back = tab && tab.offsetParent ? tab : (menuBtn && menuBtn.offsetParent ? menuBtn : null);
    }
    if (back) back.focus();
  });
  pf.querySelectorAll("[data-pf-close]").forEach(function (b) { b.addEventListener("click", function () { pf.close(); }); });
  // a click on the dimmed backdrop closes the form too
  pf.addEventListener("click", function (e) { if (e.target === pf) pf.close(); });
  // typing an "other" answer ticks its box; "No" in the conference question clears the yeses, and the reverse
  pfForm.addEventListener("input", function (e) {
    if (e.target.type === "text" && e.target.name.slice(-6) === "-other") {
      e.target.closest(".pf-opt").querySelector("[data-other]").checked = e.target.value.trim() !== "";
    }
    if (e.target.type === "checkbox" && e.target.checked) {
      var group = pfForm.querySelectorAll('input[name="' + e.target.name + '"]');
      group.forEach(function (c) {
        if (c !== e.target && (c.hasAttribute("data-exclusive") || e.target.hasAttribute("data-exclusive"))) c.checked = false;
      });
    }
  });
  function pfCheck() {
    var first = null;
    function mark(el, errEl, msg) {
      el.setAttribute("aria-invalid", msg ? "true" : "false");
      errEl.textContent = msg || "";
      errEl.hidden = !msg;
      if (msg && !first) first = el;
    }
    ["pf-org", "pf-contact", "pf-job", "pf-email", "pf-phone"].forEach(function (id) {
      var el = document.getElementById(id), v = el.value.trim(), msg = v ? "" : T().pfRequired;
      if (v && id === "pf-email" && !/^\S+@\S+\.\S+$/.test(v)) msg = T().badEmail;
      if (v && id === "pf-phone") { var d = v.replace(/[\s()+-]/g, ""); if (!/^\d{8,15}$/.test(d)) msg = T().pfPhone; }
      mark(el, document.getElementById(id + "-err"), msg);
    });
    ["pf-prog", "pf-type", "pf-conf"].forEach(function (id) {
      var set = document.getElementById(id), boxes = set.querySelectorAll('input[type="checkbox"]:checked');
      var other = set.querySelector("[data-other]"), msg = boxes.length ? "" : T().pfPick;
      if (!msg && other && other.checked && !set.querySelector('input[type="text"]').value.trim()) msg = T().pfOther;
      mark(set, document.getElementById(id + "-err"), msg);
    });
    return first;
  }
  pfForm.addEventListener("submit", function (e) {
    e.preventDefault();
    var bad = pfCheck();
    if (bad) {
      var target = bad.matches("fieldset") ? (bad.querySelector('input[type="checkbox"]:not(:checked)') || bad.querySelector("input")) : bad;
      if (bad.matches("fieldset") && bad.querySelector("[data-other]:checked")) target = bad.querySelector('input[type="text"]');
      target.focus();
      bad.scrollIntoView({ block: "center", behavior: still ? "auto" : "smooth" });
      return;
    }
    // prototype: nothing is sent yet; this is where the answers go to Sanad's form or CRM
    document.getElementById("pf-done-title").textContent = T().pfThanks("⁨" + document.getElementById("pf-org").value.trim() + "⁩");
    document.getElementById("pf-done-text").textContent = T().pfDone("⁨" + document.getElementById("pf-email").value.trim() + "⁩");
    pfForm.hidden = true;
    pfDone.hidden = false;
    pf.classList.add("is-done");
    pf.setAttribute("aria-labelledby", "pf-done-title");
    document.getElementById("pf-done-title").focus();
  });

})();
