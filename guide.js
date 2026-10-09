/* Flexhub user guide — language, mode switch, steppers, device picker, remote tour, timeline, troubleshooting filter. ES5 for old browsers. */
(function () {
  "use strict";
  var doc = document, root = doc.documentElement, body = doc.body;
  root.className += " js";
  function all(sel, ctx) { return Array.prototype.slice.call((ctx || doc).querySelectorAll(sel)); }
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) {} return null; }
  var reduce = !!(window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches);
  function scrollTo(el) { if (el && el.scrollIntoView) { try { el.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" }); } catch (e) { el.scrollIntoView(true); } } }

  /* Language (same key as the landing page) */
  var titles = {
    en: "Flexhub user guide — USB mode & wireless mode setup, pairing, macros, troubleshooting",
    zh: "Flexhub 使用说明 — USB 模式与无线模式：连接、配对、宏、常见问题"
  };
  var lang = "en";
  function setLang(l) {
    lang = l === "zh" ? "zh" : "en";
    root.lang = lang === "zh" ? "zh-Hans" : "en";
    doc.title = titles[lang];
    store("flexhub_lang", lang);
    var sel = doc.getElementById("lang");
    if (sel) sel.value = lang;
    all("[data-ph-en]").forEach(function (el) { el.setAttribute("placeholder", el.getAttribute("data-ph-" + lang)); });
    all(".stepper").forEach(function (s) { if (s._render) s._render(); });
  }
  var savedLang = store("flexhub_lang");
  setLang(savedLang || (/^zh\b/i.test(navigator.language || "") ? "zh" : "en"));
  var langSel = doc.getElementById("lang");
  if (langSel) langSel.addEventListener("change", function () { setLang(langSel.value); });

  /* Mode: usb | ble  (#usb, #wireless, #ble, #bluetooth) */
  function setMode(mode, updateHash) {
    mode = mode === "ble" ? "ble" : "usb";
    body.setAttribute("data-mode", mode);
    all("[data-set-mode]").forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-set-mode") === mode ? "true" : "false"); });
    store("flexhub_guide_mode", mode);
    if (updateHash && window.history && history.replaceState) history.replaceState(null, "", mode === "ble" ? "#wireless" : "#usb");
  }
  function modeFromHash() {
    var h = (location.hash || "").toLowerCase();
    if (h === "#usb") return "usb";
    if (h === "#wireless" || h === "#ble" || h === "#bluetooth") return "ble";
    return null;
  }
  var hashMode = modeFromHash();
  setMode(hashMode || store("flexhub_guide_mode") || "usb", false);
  all("[data-set-mode]").forEach(function (b) {
    b.addEventListener("click", function () {
      setMode(b.getAttribute("data-set-mode"), true);
      var go = b.getAttribute("data-go");
      if (go) scrollTo(doc.getElementById(go));
    });
  });
  window.addEventListener("hashchange", function () { var x = modeFromHash(); if (x) setMode(x, false); });

  /* Steppers */
  all(".stepper").forEach(function (box) {
    var items = all(".steps > li", box), i = 0, n = items.length;
    var bar = box.querySelector(".progress span"), count = box.querySelector(".st-count"), dots = box.querySelector(".st-dots");
    var prev = box.querySelector("[data-prev]"), next = box.querySelector("[data-next]");
    var btns = [];
    items.forEach(function (li, k) {
      var b = doc.createElement("button");
      b.type = "button"; b.textContent = String(k + 1);
      b.setAttribute("aria-label", "Step " + (k + 1));
      b.addEventListener("click", function () { go(k); });
      dots.appendChild(b); btns.push(b);
    });
    function go(k) { i = Math.max(0, Math.min(n - 1, k)); render(); }
    function render() {
      items.forEach(function (li, k) { li.className = k === i ? "on" : ""; });
      btns.forEach(function (b, k) {
        b.className = k < i ? "done" : "";
        if (k === i) b.setAttribute("aria-current", "step"); else b.removeAttribute("aria-current");
      });
      if (bar) bar.style.width = ((i + 1) / n * 100) + "%";
      if (count) count.textContent = lang === "zh" ? ("第 " + (i + 1) + " 步，共 " + n + " 步") : ("Step " + (i + 1) + " of " + n);
      if (prev) prev.disabled = i === 0;
      if (next) next.disabled = i === n - 1;
    }
    box._render = render;
    if (prev) prev.addEventListener("click", function () { go(i - 1); });
    if (next) next.addEventListener("click", function () { go(i + 1); });
    box.addEventListener("keydown", function (e) {
      if (e.target && /INPUT|TEXTAREA|SELECT/.test(e.target.tagName)) return;
      if (e.keyCode === 37) { go(i - 1); } else if (e.keyCode === 39) { go(i + 1); }
    });
    render();
  });

  /* Device picker */
  all("[data-picker]").forEach(function (box) {
    var picks = all("[data-pick]", box), panels = all("[data-panel]", box);
    function show(id) {
      picks.forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-pick") === id ? "true" : "false"); });
      panels.forEach(function (p) { p.className = "pick-panel" + (p.getAttribute("data-panel") === id ? " on" : ""); });
    }
    picks.forEach(function (b) { b.addEventListener("click", function () { show(b.getAttribute("data-pick")); }); });
    if (picks.length) show(picks[0].getAttribute("data-pick"));
  });

  /* Remote page tour */
  all("[data-tour]").forEach(function (box) {
    var tabs = all("[data-tab]", box), panes = all("[data-pane]", box), descs = all("[data-desc]", box);
    function show(id, focus) {
      tabs.forEach(function (t) {
        var on = t.getAttribute("data-tab") === id;
        t.setAttribute("aria-selected", on ? "true" : "false");
        t.setAttribute("tabindex", on ? "0" : "-1");
        if (on && focus) t.focus();
      });
      panes.forEach(function (p) { p.className = "ph-pane" + (p.getAttribute("data-pane") === id ? " on" : ""); });
      descs.forEach(function (d) { d.className = "tour-desc" + (d.getAttribute("data-desc") === id ? " on" : ""); });
    }
    tabs.forEach(function (t, k) {
      t.addEventListener("click", function () { show(t.getAttribute("data-tab")); });
      t.addEventListener("keydown", function (e) {
        var d = e.keyCode === 39 ? 1 : e.keyCode === 37 ? -1 : 0;
        if (!d) return;
        e.preventDefault();
        show(tabs[(k + d + tabs.length) % tabs.length].getAttribute("data-tab"), true);
      });
    });
    if (tabs.length) show(tabs[0].getAttribute("data-tab"));
  });

  /* Timeline fill + TOC highlight */
  var tls = all(".tl"), tocLinks = all(".toc a");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.className += " in"; io.unobserve(e.target); } });
    }, { threshold: 0.3 });
    tls.forEach(function (t) { io.observe(t); });
    var secIo = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        var id = "#" + e.target.id;
        tocLinks.forEach(function (a) { a.className = a.getAttribute("href") === id ? "on" : ""; });
      });
    }, { rootMargin: "-40% 0px -55% 0px" });
    tocLinks.forEach(function (a) { var s = doc.getElementById(a.getAttribute("href").slice(1)); if (s) secIo.observe(s); });
  } else {
    tls.forEach(function (t) { t.className += " in"; });
  }

  /* Troubleshooting filter */
  var filter = doc.getElementById("tsFilter"), list = doc.getElementById("tsList"), empty = doc.getElementById("tsEmpty"), expand = doc.getElementById("tsExpand");
  if (list) {
    var items = all("details", list);
    var run = function () {
      var q = (filter && filter.value || "").toLowerCase().replace(/^\s+|\s+$/g, ""), shown = 0;
      items.forEach(function (d) {
        var hit = !q || (d.textContent || "").toLowerCase().indexOf(q) !== -1;
        if (hit) { d.removeAttribute("hidden"); shown++; } else { d.setAttribute("hidden", ""); }
        if (q && hit) d.open = true;
      });
      if (empty) empty.className = "ts-empty" + (shown ? "" : " on");
    };
    if (filter) { filter.addEventListener("input", run); filter.addEventListener("keyup", run); }
    if (expand) expand.addEventListener("click", function () {
      var open = items.some(function (d) { return !d.open && !d.hasAttribute("hidden"); });
      items.forEach(function (d) { if (!d.hasAttribute("hidden")) d.open = open; });
    });
    var h = (location.hash || "").slice(1);
    if (/^ts-/.test(h)) { var t = doc.getElementById(h); if (t) t.open = true; }
  }
})();
