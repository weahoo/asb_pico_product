/* Flexhub legal pages: language picker (same storage key and ?lang= as landing/guide). */
(function () {
  var LANGS = ["en","zh","de","fr","ja","ko","ar"];
  var LANG_HTML = {en:"en", zh:"zh-Hans", de:"de", fr:"fr", ja:"ja", ko:"ko", ar:"ar"};
  var meta = JSON.parse(document.getElementById("legal-meta").textContent);
  var root = document.documentElement;
  function store(v) { try { localStorage.setItem("flexhub_lang", v); } catch (e) {} }
  function setMeta(sel, val) { var m = document.querySelector(sel); if (m && val) m.setAttribute("content", val); }
  function current() {
    for (var k in LANG_HTML) { if (LANG_HTML[k] === root.lang) return k; }
    return "en";
  }
  function setLang(l, save) {
    if (LANGS.indexOf(l) < 0) l = "en";
    root.lang = LANG_HTML[l];
    root.dir = l === "ar" ? "rtl" : "ltr";
    var m = meta[l] || meta.en;
    document.title = m.title;
    setMeta('meta[name="description"]', m.description);
    setMeta('meta[property="og:title"]', m.title);
    setMeta('meta[property="og:description"]', m.description);
    var sel = document.getElementById("lang");
    if (sel) { sel.value = l; sel.setAttribute("aria-label", m.langLabel); }
    if (save) store(l);
  }
  setLang(current(), true);
  var sel = document.getElementById("lang");
  if (sel) sel.addEventListener("change", function () { setLang(sel.value, true); });
})();
