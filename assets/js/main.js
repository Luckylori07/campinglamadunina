/* Camping La Madunina — demo Tramontis. JavaScript nativo, nessuna dipendenza.
   Tutto è un miglioramento progressivo: senza JS il sito resta navigabile. */
(function () {
  "use strict";
  var doc = document.documentElement;
  var lang = doc.lang || "it";
  var I = (window.LM_I18N || {});
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* --- lingua preferita (mantenuta tra le visite) ------------------------- */
  try {
    var pref = localStorage.getItem("lm-lang");
    var sameSite = document.referrer && document.referrer.indexOf(location.origin) === 0;
    var alt = document.querySelector('link[rel="alternate"][hreflang="' + pref + '"]');
    if (pref && pref !== lang && alt && !sameSite && !location.search.match(/nolang/)) {
      location.replace(alt.getAttribute("href"));
      return;
    }
  } catch (e) {}
  document.addEventListener("click", function (ev) {
    var a = ev.target.closest && ev.target.closest("a[hreflang][data-setlang]");
    if (a) { try { localStorage.setItem("lm-lang", a.getAttribute("hreflang")); } catch (e) {} }
  });

  /* --- altezza banner + header (per menu mobile e ancore) ---------------- */
  var top = document.querySelector(".top");
  function measure() { if (top) doc.style.setProperty("--top-h", top.offsetHeight + "px"); }
  measure();
  window.addEventListener("resize", measure, { passive: true });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(measure);
  window.addEventListener("scroll", function () { if (top) top.classList.toggle("is-scrolled", window.scrollY > 8); }, { passive: true });

  /* --- menu mobile ------------------------------------------------------- */
  var burger = document.querySelector(".burger");
  var nav = document.getElementById("nav");
  function setMenu(open) {
    if (!burger || !nav) return;
    burger.setAttribute("aria-expanded", String(open));
    burger.setAttribute("aria-label", open ? I.menuClose : I.menuOpen);
    nav.classList.toggle("is-open", open);
    measure();
  }
  if (burger && nav) {
    burger.addEventListener("click", function () { setMenu(burger.getAttribute("aria-expanded") !== "true"); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("is-open")) { setMenu(false); burger.focus(); }
    });
    nav.addEventListener("click", function (e) { if (e.target.closest("a")) setMenu(false); });
    window.matchMedia("(min-width: 1180px)").addEventListener("change", function () { setMenu(false); });
  }

  /* --- selettore lingua: chiusura al click esterno / Esc ------------------ */
  var lng = document.querySelector("details.lang");
  if (lng) {
    document.addEventListener("click", function (e) { if (!lng.contains(e.target)) lng.removeAttribute("open"); });
    lng.addEventListener("keydown", function (e) { if (e.key === "Escape") { lng.removeAttribute("open"); lng.querySelector("summary").focus(); } });
  }

  /* --- entrata progressiva ----------------------------------------------- */
  var rv = [].slice.call(document.querySelectorAll(".rv"));
  if (rv.length) {
    if (!("IntersectionObserver" in window) || reduce) {
      rv.forEach(function (el) { el.classList.add("in"); });
    } else {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
      }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
      rv.forEach(function (el) { io.observe(el); });
      // rete di sicurezza: nulla resta nascosto
      setTimeout(function () { rv.forEach(function (el) { el.classList.add("in"); }); }, 4000);
    }
  }

  /* --- filtri galleria --------------------------------------------------- */
  var filters = document.querySelector(".filters");
  if (filters) {
    var items = [].slice.call(document.querySelectorAll(".gallery .gitem"));
    var live = document.getElementById("gcount");
    filters.addEventListener("click", function (e) {
      var b = e.target.closest("button[data-filter]");
      if (!b) return;
      filters.querySelectorAll("button").forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); });
      var f = b.getAttribute("data-filter"), n = 0;
      items.forEach(function (it) {
        var show = f === "all" || it.getAttribute("data-cat") === f;
        it.hidden = !show; if (show) n++;
      });
      if (live) live.textContent = (I.shown || "") + " " + n;
    });
  }

  /* --- lightbox accessibile (dialog nativo) ------------------------------- */
  var links = [].slice.call(document.querySelectorAll("a[data-lightbox]"));
  if (links.length && typeof HTMLDialogElement === "function") {
    var dlg = document.createElement("dialog");
    dlg.className = "lb";
    dlg.setAttribute("aria-label", I.lbLabel || "Gallery");
    dlg.innerHTML =
      '<div class="lb__bar"><span class="lb__count" aria-live="polite"></span>' +
      '<button type="button" class="lb__btn lb__close" aria-label="' + (I.lbClose || "Close") + '"><svg class="icon" aria-hidden="true"><use href="#i-x"/></svg></button></div>' +
      '<div class="lb__stage"><button type="button" class="lb__btn lb__prev" aria-label="' + (I.lbPrev || "Previous") + '"><svg class="icon" aria-hidden="true"><use href="#i-chev-l"/></svg></button>' +
      '<img class="lb__img" alt=""><button type="button" class="lb__btn lb__next" aria-label="' + (I.lbNext || "Next") + '"><svg class="icon" aria-hidden="true"><use href="#i-chev-r"/></svg></button></div>' +
      '<p class="lb__cap"></p>';
    document.body.appendChild(dlg);
    var img = dlg.querySelector(".lb__img"), cap = dlg.querySelector(".lb__cap"), cnt = dlg.querySelector(".lb__count");
    var cur = 0, opener = null, list = links;

    function visible() { return links.filter(function (a) { var f = a.closest(".gitem"); return !(f && f.hidden); }); }
    function show(i) {
      cur = (i + list.length) % list.length;
      var a = list[cur], im = a.querySelector("img");
      img.style.animation = "none"; void img.offsetWidth; img.style.animation = "";
      img.src = a.getAttribute("href");
      img.alt = im ? im.alt : "";
      cap.innerHTML = a.getAttribute("data-caption") || "";
      cnt.textContent = (cur + 1) + " / " + list.length;
      // precarica la successiva
      var n = new Image(); n.src = list[(cur + 1) % list.length].getAttribute("href");
    }
    links.forEach(function (a) {
      a.addEventListener("click", function (e) {
        if (e.metaKey || e.ctrlKey || e.shiftKey || e.button === 1) return;
        e.preventDefault();
        opener = a; list = visible();
        if (list.indexOf(a) < 0) list = links;
        dlg.showModal(); show(list.indexOf(a));
        dlg.querySelector(".lb__close").focus();
      });
    });
    dlg.querySelector(".lb__prev").addEventListener("click", function () { show(cur - 1); });
    dlg.querySelector(".lb__next").addEventListener("click", function () { show(cur + 1); });
    dlg.querySelector(".lb__close").addEventListener("click", function () { dlg.close(); });
    dlg.addEventListener("close", function () { if (opener) opener.focus(); });
    dlg.addEventListener("click", function (e) { if (e.target === dlg || e.target.classList.contains("lb__stage")) dlg.close(); });
    dlg.addEventListener("keydown", function (e) {
      if (e.key === "ArrowLeft") { e.preventDefault(); show(cur - 1); }
      if (e.key === "ArrowRight") { e.preventDefault(); show(cur + 1); }
    });
    var sx = null;
    dlg.addEventListener("touchstart", function (e) { sx = e.touches[0].clientX; }, { passive: true });
    dlg.addEventListener("touchend", function (e) {
      if (sx === null) return;
      var dx = e.changedTouches[0].clientX - sx; sx = null;
      if (Math.abs(dx) > 50) show(cur + (dx < 0 ? 1 : -1));
    }, { passive: true });
  }

  /* --- modulo contatti: nessun invio fittizio, apre il client di posta ---- */
  var form = document.getElementById("contact-form");
  if (form) {
    var status = document.getElementById("form-status");
    var fields = ["name", "email", "period", "message", "privacy"];
    form.setAttribute("novalidate", "");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var ok = true, first = null;
      fields.forEach(function (id) {
        var el = form.elements[id], err = document.getElementById("err-" + id);
        if (!el || !err) return;
        var bad = false, msg = "";
        if (el.type === "checkbox") { bad = !el.checked; msg = I.errPrivacy; }
        else if (id === "email") { bad = !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(el.value.trim()); msg = el.value.trim() ? I.errEmail : I.errRequired; }
        else if (id === "name" || id === "message") { bad = !el.value.trim(); msg = I.errRequired; }
        el.setAttribute("aria-invalid", String(bad));
        err.textContent = bad ? msg : "";
        if (bad) { ok = false; first = first || el; }
      });
      if (!ok) { status.textContent = I.errSummary; first.focus(); return; }
      var v = function (id) { return form.elements[id].value.trim(); };
      var body = I.mailName + ": " + v("name") + "\n" + I.mailEmail + ": " + v("email") + "\n" +
        (v("period") ? I.mailPeriod + ": " + v("period") + "\n" : "") + "\n" + v("message") + "\n\n— " + I.mailFooter;
      location.href = "mailto:info@campinglamadunina.com?subject=" + encodeURIComponent(I.mailSubject) + "&body=" + encodeURIComponent(body);
      status.textContent = I.sent;
    });
    form.addEventListener("input", function (e) {
      var el = e.target, err = document.getElementById("err-" + el.name);
      if (err && el.getAttribute("aria-invalid") === "true") { el.setAttribute("aria-invalid", "false"); err.textContent = ""; }
    });
  }
})();
