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
    en: "Flexhub user guide \u2014 USB mode & wireless mode setup, pairing, macros, troubleshooting",
    zh: "Flexhub \u4f7f\u7528\u8bf4\u660e \u2014 USB \u6a21\u5f0f\u4e0e\u65e0\u7ebf\u6a21\u5f0f\uff1a\u8fde\u63a5\u3001\u914d\u5bf9\u3001\u5b8f\u3001\u5e38\u89c1\u95ee\u9898",
    de: "Flexhub Bedienungsanleitung \u2014 USB- & Funkmodus: Einrichtung, Pairing, Makros, Fehlerbehebung",
    fr: "Guide Flexhub \u2014 modes USB et sans fil : configuration, appairage, macros, d\u00e9pannage",
    ja: "Flexhub \u30e6\u30fc\u30b6\u30fc\u30ac\u30a4\u30c9 \u2014 USB / \u30ef\u30a4\u30e4\u30ec\u30b9\u30e2\u30fc\u30c9\u306e\u8a2d\u5b9a\u3001\u30da\u30a2\u30ea\u30f3\u30b0\u3001\u30de\u30af\u30ed\u3001\u30c8\u30e9\u30d6\u30eb\u30b7\u30e5\u30fc\u30c6\u30a3\u30f3\u30b0",
    ko: "Flexhub \uc0ac\uc6a9 \uc124\uba85\uc11c \u2014 USB\u00b7\ubb34\uc120 \ubaa8\ub4dc \uc124\uc815, \ud398\uc5b4\ub9c1, \ub9e4\ud06c\ub85c, \ubb38\uc81c \ud574\uacb0",
    ar: "\u062f\u0644\u064a\u0644 \u0645\u0633\u062a\u062e\u062f\u0645 Flexhub \u2014 \u0648\u0636\u0639\u0627 USB \u0648\u0627\u0644\u0644\u0627\u0633\u0644\u0643\u064a: \u0627\u0644\u0625\u0639\u062f\u0627\u062f \u0648\u0627\u0644\u0627\u0642\u062a\u0631\u0627\u0646 \u0648\u0627\u0644\u0645\u0627\u0643\u0631\u0648 \u0648\u0627\u0633\u062a\u0643\u0634\u0627\u0641 \u0627\u0644\u0623\u062e\u0637\u0627\u0621"
  };
  var descs = {"en": "Complete Flexhub user guide: USB mode (driver-free keyboard and mouse) and wireless mode (power only, Bluetooth pairing as flexhub), the flexhub Wi‑Fi page, macros, Presenter, TV remotes, firmware updates and troubleshooting.", "zh": "Flexhub 完整使用说明：USB 模式（免驱键盘鼠标）与无线模式（只供电，蓝牙配对 flexhub）、flexhub Wi‑Fi 页面、宏、演示器、电视遥控、固件升级与常见问题。", "de": "Vollständige Flexhub-Anleitung: USB-Modus (Tastatur und Maus ohne Treiber) und Funkmodus (nur Strom, Bluetooth-Pairing als flexhub), die flexhub-Wi‑Fi-Seite, Makros, Presenter, TV-Fernbedienungen, Firmware-Updates und Fehlerbehebung.", "fr": "Guide complet de Flexhub : mode USB (clavier et souris sans pilote) et mode sans fil (alimentation seule, appairage Bluetooth « flexhub »), la page Wi‑Fi flexhub, macros, présentateur, télécommandes TV, mises à jour du firmware et dépannage.", "ja": "Flexhub 完全ガイド：USB モード（ドライバ不要のキーボードとマウス）とワイヤレスモード（電源のみ、Bluetooth で flexhub とペアリング）、flexhub Wi‑Fi ページ、マクロ、プレゼンター、TV リモコン、ファームウェア更新、トラブルシューティング。", "ko": "Flexhub 전체 사용 설명서: USB 모드(드라이버 없는 키보드·마우스)와 무선 모드(전원만, Bluetooth로 flexhub 페어링), flexhub Wi‑Fi 페이지, 매크로, 프레젠터, TV 리모컨, 펌웨어 업데이트, 문제 해결.", "ar": "دليل Flexhub الكامل: وضع USB (لوحة مفاتيح وفأرة بدون تعريف) والوضع اللاسلكي (طاقة فقط، اقتران Bluetooth باسم flexhub)، وصفحة Wi‑Fi، والماكرو، وجهاز العرض، وأجهزة تحكم التلفاز، وتحديثات البرنامج الثابت واستكشاف الأخطاء."};
  function setMeta(sel, val) { var m = doc.querySelector(sel); if (m && val) m.setAttribute("content", val); }
  var LANGS = ["en","zh","de","fr","ja","ko","ar"];
  var LANG_HTML = {en:"en", zh:"zh-Hans", de:"de", fr:"fr", ja:"ja", ko:"ko", ar:"ar"};
  var lang = "en";
  function detectLang() {
    try {
      var q = new URLSearchParams(location.search).get("lang");
      if (q && LANGS.indexOf(q) >= 0) return q;
    } catch (e) {}
    var s = store("flexhub_lang");
    if (s && LANGS.indexOf(s) >= 0) return s;
    var nav = (navigator.language || "").toLowerCase();
    if (/^zh/.test(nav)) return "zh";
    if (/^de/.test(nav)) return "de";
    if (/^fr/.test(nav)) return "fr";
    if (/^ja/.test(nav)) return "ja";
    if (/^ko/.test(nav)) return "ko";
    if (/^ar/.test(nav)) return "ar";
    return "en";
  }
  var A11Y = {"nav": {"en": "Primary", "zh": "主导航", "de": "Hauptnavigation", "fr": "Navigation principale", "ja": "メインナビゲーション", "ko": "주 메뉴", "ar": "التنقل الرئيسي"}, "lang": {"en": "Language", "zh": "语言", "de": "Sprache", "fr": "Langue", "ja": "言語", "ko": "언어", "ar": "اللغة"}, "choose": {"en": "Choose a mode", "zh": "选择模式", "de": "Modus wählen", "fr": "Choisir un mode", "ja": "モードを選択", "ko": "모드 선택", "ar": "اختر الوضع"}, "mode": {"en": "Mode", "zh": "模式", "de": "Modus", "fr": "Mode", "ja": "モード", "ko": "모드", "ar": "الوضع"}, "toc": {"en": "On this page", "zh": "本页内容", "de": "Auf dieser Seite", "fr": "Sur cette page", "ja": "このページの内容", "ko": "이 페이지의 내용", "ar": "في هذه الصفحة"}, "sceneUsb": {"en": "Computer connected to Flexhub by USB cable; phone connected to Flexhub over Wi‑Fi", "zh": "电脑通过 USB 线连接 Flexhub；手机通过 Wi‑Fi 连接 Flexhub", "de": "Computer per USB-Kabel mit Flexhub verbunden; Handy per Wi‑Fi mit Flexhub verbunden", "fr": "Ordinateur relié à Flexhub par câble USB ; téléphone connecté à Flexhub en Wi‑Fi", "ja": "パソコンは USB ケーブルで Flexhub に接続、スマホは Wi‑Fi で Flexhub に接続", "ko": "컴퓨터는 USB 케이블로 Flexhub에 연결되고, 휴대폰은 Wi‑Fi로 Flexhub에 연결됨", "ar": "الحاسوب موصول بـ Flexhub بكابل USB، والهاتف متصل بـ Flexhub عبر Wi‑Fi"}, "sceneBle": {"en": "Power bank powering Flexhub; Flexhub paired to a TV over Bluetooth and to a phone over Wi‑Fi", "zh": "充电宝为 Flexhub 供电；Flexhub 通过蓝牙配对电视，通过 Wi‑Fi 连接手机", "de": "Powerbank versorgt Flexhub mit Strom; Flexhub per Bluetooth mit einem Fernseher gekoppelt und per Wi‑Fi mit einem Handy verbunden", "fr": "Batterie externe alimentant Flexhub ; Flexhub appairé à un téléviseur en Bluetooth et connecté à un téléphone en Wi‑Fi", "ja": "モバイルバッテリーで Flexhub に給電し、Flexhub は Bluetooth でテレビとペアリング、Wi‑Fi でスマホと接続", "ko": "보조배터리로 Flexhub에 전원 공급, Flexhub는 Bluetooth로 TV와 페어링되고 Wi‑Fi로 휴대폰과 연결됨", "ar": "بطارية متنقلة تزوّد Flexhub بالطاقة، وFlexhub مقترن بالتلفاز عبر Bluetooth ومتصل بالهاتف عبر Wi‑Fi"}, "compare": {"en": "USB mode versus wireless mode", "zh": "USB 模式与无线模式对比", "de": "USB-Modus und Funkmodus im Vergleich", "fr": "Mode USB et mode sans fil comparés", "ja": "USB モードとワイヤレスモードの比較", "ko": "USB 모드와 무선 모드 비교", "ar": "مقارنة بين وضع USB والوضع اللاسلكي"}, "device": {"en": "Device", "zh": "设备", "de": "Gerät", "fr": "Appareil", "ja": "デバイス", "ko": "기기", "ar": "الجهاز"}, "preview": {"en": "Flexhub remote page preview", "zh": "Flexhub 遥控页面预览", "de": "Vorschau der Flexhub-Fernbedienungsseite", "fr": "Aperçu de la page de télécommande Flexhub", "ja": "Flexhub リモコンページのプレビュー", "ko": "Flexhub 리모컨 페이지 미리보기", "ar": "معاينة صفحة التحكم في Flexhub"}, "tabs": {"en": "Remote tabs", "zh": "遥控标签页", "de": "Tabs der Fernbedienung", "fr": "Onglets de la télécommande", "ja": "リモコンのタブ", "ko": "리모컨 탭", "ar": "تبويبات صفحة التحكم"}, "search": {"en": "Search troubleshooting", "zh": "搜索常见问题", "de": "Fehlerbehebung durchsuchen", "fr": "Rechercher dans le dépannage", "ja": "トラブルシューティングを検索", "ko": "문제 해결 검색", "ar": "البحث في استكشاف الأخطاء"}, "step": {"en": "Step {n}", "zh": "第 {n} 步", "de": "Schritt {n}", "fr": "Étape {n}", "ja": "ステップ {n}", "ko": "{n}단계", "ar": "الخطوة {n}"}};
  function t11(key) { var e = A11Y[key]; return e ? (e[lang] || e.en) : ""; }
  function setLang(l) {
    lang = LANGS.indexOf(l) >= 0 ? l : "en";
    root.lang = LANG_HTML[lang] || "en";
    root.dir = lang === "ar" ? "rtl" : "ltr";
    doc.title = titles[lang] || titles.en;
    var dsc = descs[lang] || descs.en;
    setMeta('meta[name="description"]', dsc);
    setMeta('meta[property="og:title"]', doc.title);
    setMeta('meta[property="og:description"]', dsc);
    store("flexhub_lang", lang);
    var sel = doc.getElementById("lang");
    if (sel) sel.value = lang;
    all("[data-ph-en]").forEach(function (el) {
      var ph = el.getAttribute("data-ph-" + lang) || el.getAttribute("data-ph-en");
      if (ph) el.setAttribute("placeholder", ph);
    });
    all("[data-a11y]").forEach(function (el) {
      el.getAttribute("data-a11y").split(";").forEach(function (pair) {
        var i = pair.indexOf(":"); if (i < 0) return;
        var v = t11(pair.slice(i + 1).trim());
        if (v) el.setAttribute(pair.slice(0, i).trim(), v);
      });
    });
    all(".stepper").forEach(function (s) { if (s._render) s._render(); });
  }
  setLang(detectLang());
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
      b.type = "button";
      b.setAttribute("aria-label", t11("step").replace("{n}", String(k + 1)));
      b.addEventListener("click", function () { go(k); });
      dots.appendChild(b); btns.push(b);
    });
    function go(k) { i = Math.max(0, Math.min(n - 1, k)); render(); }
    function render() {
      items.forEach(function (li, k) { li.className = k === i ? "on" : ""; });
      btns.forEach(function (b, k) {
        b.className = k < i ? "done" : "";
        if (k === i) b.setAttribute("aria-current", "step"); else b.removeAttribute("aria-current");
        b.setAttribute("aria-label", t11("step").replace("{n}", String(k + 1)));
      });
      if (bar) bar.style.width = ((i + 1) / n * 100) + "%";
      if (count) {
        var cur = i + 1;
        if (lang === "zh") count.textContent = "第 " + cur + " 步，共 " + n + " 步";
        else if (lang === "de") count.textContent = "Schritt " + cur + " von " + n;
        else if (lang === "fr") count.textContent = "Étape " + cur + " sur " + n;
        else if (lang === "ja") count.textContent = cur + " / " + n + " ステップ";
        else if (lang === "ko") count.textContent = cur + " / " + n + " 단계";
        else if (lang === "ar") count.textContent = "الخطوة " + cur + " من " + n;
        else count.textContent = "Step " + cur + " of " + n;
      }
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
