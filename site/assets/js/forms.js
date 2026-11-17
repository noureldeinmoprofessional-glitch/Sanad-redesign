/* Forms on their own page (form[data-validate]): checks each field as written in the markup (required,
   email, phone, link, file type and size), shows the message under the field and moves focus to the first
   problem. On success the form gives way to its [data-done] message. Nothing is sent yet. */
(function () {
  "use strict";
  var S = window.Sanad, T = S.T;
  S.strings({
    ar: {
      fRequired: "هذا الحقل مطلوب.",
      fPhone: "اكتب رقم هاتف صحيح.",
      fUrl: "اكتب رابطًا صحيحًا يبدأ بـ https://",
      fFileType: "ارفع ملف PDF أو Word.",
      fFileSize: function (mb) { return "حجم الملف أكبر من " + mb + " ميجابايت."; }
    },
    en: {
      fRequired: "This field is required.",
      fPhone: "Please enter a valid phone number.",
      fUrl: "Please enter a valid link starting with https://",
      fFileType: "Please upload a PDF or Word file.",
      fFileSize: function (mb) { return "The file is larger than " + mb + " MB."; }
    }
  });

  function problem(el) {
    var v = (el.value || "").trim();
    if (el.type === "file") {
      var f = el.files && el.files[0];
      if (!f) return el.required ? T().fRequired : "";
      var ok = (el.accept || "").split(",").some(function (ext) { return f.name.toLowerCase().slice(-ext.trim().length) === ext.trim(); });
      if (!ok) return T().fFileType;
      var mb = parseFloat(el.dataset.maxMb || "0");
      if (mb && f.size > mb * 1024 * 1024) return T().fFileSize(mb);
      return "";
    }
    if (!v) return el.required ? T().fRequired : "";
    if (el.type === "email" && !/^\S+@\S+\.\S+$/.test(v)) return T().badEmail;
    if (el.type === "tel" && !/^\d{8,15}$/.test(v.replace(/[\s()+-]/g, ""))) return T().fPhone;
    if (el.type === "url" && !/^https?:\/\/\S+\.\S+/.test(v)) return T().fUrl;
    return "";
  }
  function show(el, msg) {
    var err = document.getElementById(el.id + "-err");
    var box = el.type === "file" ? el.closest(".drop") : el;
    box.setAttribute("aria-invalid", msg ? "true" : "false");
    if (box !== el) el.setAttribute("aria-invalid", msg ? "true" : "false");
    if (err) { err.textContent = msg; err.hidden = !msg; }
  }

  document.querySelectorAll("form[data-validate]").forEach(function (form) {
    var fields = form.querySelectorAll("input:not([type=hidden]), select, textarea");
    // a chosen file shows its name in the drop area
    form.querySelectorAll("input[type=file]").forEach(function (inp) {
      inp.addEventListener("change", function () {
        var name = inp.closest(".drop").querySelector("[data-file-name]");
        if (name) name.textContent = inp.files && inp.files[0] ? inp.files[0].name : "";
        show(inp, problem(inp));
      });
    });
    // once a field has been flagged, it clears as soon as it is fixed
    fields.forEach(function (el) {
      el.addEventListener("input", function () { if (el.getAttribute("aria-invalid") === "true") show(el, problem(el)); });
    });
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var first = null;
      fields.forEach(function (el) { var msg = problem(el); show(el, msg); if (msg && !first) first = el; });
      if (first) { first.focus(); first.scrollIntoView({ block: "center", behavior: S.still ? "auto" : "smooth" }); return; }
      var done = form.parentElement.querySelector("[data-done]");
      form.hidden = true;
      done.hidden = false;
      done.querySelector("h2").focus();
    });
  });
})();
