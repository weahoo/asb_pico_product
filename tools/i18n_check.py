#!/usr/bin/env python3
"""Flexhub site i18n sweep.

Static checks (no browser):
  * guide.html: every data-l group has exactly the 7 languages in order, balanced inline tags
    matching EN, same numbers as EN, right script for the language, no MT placeholder debris,
    no manual "1." step prefixes, data-ph-* placeholders for every language.
  * site.js dict: same key set in every language, same checks per value, no value copied from
    another language.
Dynamic checks (Chrome via CDP, default http://127.0.0.1:9222; site served at --base):
  * index.html and guide.html in all 7 languages (guide in USB and wireless mode), all <details>
    opened, every tour tab / device picker visited; collects visible text plus aria-label, title,
    alt, placeholder, <title>, meta description/og/twitter and flags script mismatches, wrong-language
    spans that are visible, EN text leaking onto other languages, JS strings.
  * Step numbering: each stepper step / How card shows exactly one number; stepper list items are
    direct children (no HTML nesting damage); dot count == step count.
  * Console errors / page errors.

Usage:  python3 -m http.server 8765  (in repo root), then
        python3 tools/i18n_check.py [--base http://127.0.0.1:8765] [--cdp http://127.0.0.1:9222]
                                    [--static-only] [--json report.json]
Exit code 0 = clean, 1 = issues found.
"""
import argparse, html, json, os, re, subprocess, sys
from collections import Counter, defaultdict
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGS = ["en", "zh", "de", "fr", "ja", "ko", "ar"]
LANG_HTML = {"en": "en", "zh": "zh-Hans", "de": "de", "fr": "fr", "ja": "ja", "ko": "ko", "ar": "ar"}

RX = {
    "kana": re.compile(r"[\u3040-\u30ff\u31f0-\u31ff\uff66-\uff9f]"),
    "han": re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]"),
    "hangul": re.compile(r"[\u1100-\u11ff\u3130-\u318f\uac00-\ud7af]"),
    "arabic": re.compile(r"[\u0600-\u06ff\u0750-\u077f\ufb50-\ufdff\ufe70-\ufeff]"),
    "cjkpunct": re.compile(r"[\u3000-\u303f\uff01-\uff0f\uff1a-\uff20]"),
}
FORBID = {
    "en": ["kana", "han", "hangul", "arabic", "cjkpunct"],
    "de": ["kana", "han", "hangul", "arabic", "cjkpunct"],
    "fr": ["kana", "han", "hangul", "arabic", "cjkpunct"],
    "zh": ["kana", "hangul", "arabic"],
    "ja": ["hangul", "arabic"],
    "ko": ["kana", "han", "arabic"],
    "ar": ["kana", "han", "hangul", "cjkpunct"],
}
NATIVE = {"zh": ["han"], "ja": ["kana", "han"], "ko": ["hangul"], "ar": ["arabic"]}
# Latin words that may legitimately appear untranslated in any language.
ALLOW_TERMS = set("""
flexhub usb usb-c bluetooth wi-fi wifi bootsel pico raspberry rp2040 rp2350 macos windows linux ios ipados android
chromeos iphone ipad chrome edge safari firefox samsung pdf json hid led ok ctrl shift alt cmd option win esc tab enter
fn pc tv mac app gps ssid ip uf2 ble gpio http https www local build.me flexhub.local api url qr id ai f1 f2 f3 f4 f5
f6 f7 f8 f9 f10 f11 f12 pgup pgdn home end del ins capslock caps lock space backspace sd typec type-c otg mb kb ms s min
hz dpi ppt powerpoint keynote google slides zoom teams vlc youtube netflix creem paypal visa css html js nfc ota bios uefi
hdmi a-z xyz abc presenter github fire stick roku apple shield xbox playstation ps lg sony philips hisense tcl tizen webos
""".split())
# Literal strings of the Flexhub device web UI (firmware UI is English / Chinese only, out of scope)
# and key-cap names. They are quoted verbatim in every language, so they are not translation errors.
UI_LITERALS = ["Another page is controlling", "Connect target device", "Detecting connection", "USB detected late",
               "Disconnected", "Ready", "English", "\u4e2d\u6587", "Send", "Hello", "PrtSc", "Bksp", "Sym", "Caps", "Gui",
               "Ins", "Del", "PgUp", "PgDn", "Home", "End", "Bg\u2212", "Bg+", "FH", "Apple TV", "Google TV", "Xiaomi",
               "WPS", "DualSense", "Keynote", "Safari", "mini", "Page Up", "Page Down", "Move scale", "Mute"]
# Exact visible strings allowed as-is (e.g. the "EN" language toggle drawn in the device UI illustration).
UI_EXACT = {"EN"}
UI_LITERALS_RX = re.compile("|".join(re.escape(x) for x in sorted(UI_LITERALS, key=len, reverse=True)))
PLACEHOLDER_RX = re.compile(r"(x{3,}\d*x*|\bXX+\b|\bP\d+x\b|__+\w*__+|\[\[|\]\]|\{\{|\}\}|\bPH\d+\b|\bTERM\d+\b|\(x+\d*x*\))", re.I)
STEP_PREFIX_RX = re.compile(r"^\s*(?:\d+|[\u0660-\u0669]+|[\uff10-\uff19]+)\s*[.)\u3001\uff0e\uff09:\-\u2013]\s*\S")
DIGIT_MAP = {ord(c): ord("0") + i for i, c in enumerate("\u0660\u0661\u0662\u0663\u0664\u0665\u0666\u0667\u0668\u0669")}
DIGIT_MAP.update({ord(c): ord("0") + i for i, c in enumerate("\uff10\uff11\uff12\uff13\uff14\uff15\uff16\uff17\uff18\uff19")})
URL_RX = re.compile(r"(https?://\S+|[\w.-]*\.(?:local|me|com|shop|json|uf2|html)\b|\d+\.\d+\.\d+\.\d+|\b(?:ctrl|alt|shift|gui)\+[\w+]+)", re.I)


def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s))


def numbers(s):
    s = strip_tags(s).translate(DIGIT_MAP)
    s = URL_RX.sub(" ", s)
    return Counter(re.findall(r"\d+", s))


def numbers_mismatch(en_s, s):
    """Compare digits of a translation with EN. Missing EN numbers are errors, except 1-3,
    which languages often spell out (e.g. Arabic dual forms). Extra numbers are only errors
    when they are 0 or larger than 12 (small extras come from spelled-out English numbers,
    e.g. 'one minute' -> '1\ubd84', 'first generation' -> '1\uc138\ub300')."""
    a, b = numbers(en_s), numbers(s)
    missing = [n for n in (a - b).elements() if not (1 <= int(n) <= 3)]
    extra = [n for n in (b - a).elements() if int(n) == 0 or int(n) > 12]
    return missing, extra


def latin_words(text):
    t = URL_RX.sub(" ", text)
    return [w for w in re.findall(r"[A-Za-z\u00c0-\u024f][A-Za-z\u00c0-\u024f.\-\u2011]*", t)]


def unknown_latin(text):
    out = []
    for w in latin_words(text):
        lw = w.lower().strip(".-\u2011").replace("\u2011", "-")
        if not lw or lw in ALLOW_TERMS or len(lw) < 2:
            continue
        if re.fullmatch(r"[a-z]\d*|\d+[a-z]+", lw):
            continue
        out.append(w)
    return out


def script_issues(lang, text):
    """Return list of (kind, detail) problems for a visible string in `lang`."""
    issues = []
    if not text or not text.strip():
        return issues
    if text.strip() in UI_EXACT:
        return issues
    raw = text
    text = UI_LITERALS_RX.sub(" ", text)
    for k in FORBID[lang]:
        m = RX[k].findall(text)
        if m:
            issues.append(("script:" + k, "".join(m[:12])))
    if lang in NATIVE:
        native = sum(len(RX[k].findall(text)) for k in NATIVE[lang])
        unk = unknown_latin(text)
        if native == 0 and unk:
            issues.append(("latin-only", " ".join(unk[:8])))
        elif unk and lang != "ja" or (lang == "ja" and unk):
            long_unk = [w for w in unk if len(w) >= 4]
            if long_unk:
                issues.append(("latin-fragment", " ".join(long_unk[:8])))
        if lang == "ja" and not RX["kana"].search(text) and len(RX["han"].findall(text)) >= 8:
            issues.append(("ja-looks-chinese", text[:40]))
    if lang == "zh" and RX["kana"].search(text):
        pass  # already flagged by FORBID
    m = PLACEHOLDER_RX.search(raw) or (re.search("\ufffd", raw))
    if m:
        issues.append(("mt-placeholder", m.group(0)))
    return issues


# ---------------------------------------------------------------- static: guide.html spans
class Node:
    __slots__ = ("tag", "attrs", "start", "end", "inner_start", "children", "parent")

    def __init__(self, tag, attrs, start, inner_start, parent):
        self.tag, self.attrs, self.start, self.inner_start, self.parent = tag, dict(attrs), start, inner_start, parent
        self.end = None
        self.children = []


VOID = set("area base br col embed hr img input link meta param source track wbr path rect circle line polyline polygon ellipse use stop".split())


class Tree(HTMLParser):
    """Source-level tree (no HTML5 error recovery) so we can see what the author wrote."""

    def __init__(self, src):
        super().__init__(convert_charrefs=False)
        self.src = src
        self.lines = [0]
        for i, c in enumerate(src):
            if c == "\n":
                self.lines.append(i + 1)
        self.root = Node("#root", [], 0, 0, None)
        self.cur = self.root
        self.errors = []
        self.feed(src)

    def pos(self):
        ln, col = self.getpos()
        return self.lines[ln - 1] + col

    def handle_starttag(self, tag, attrs):
        p = self.pos()
        raw = self.get_starttag_text() or ""
        n = Node(tag, attrs, p, p + len(raw), self.cur)
        self.cur.children.append(n)
        if tag in VOID or raw.endswith("/>"):
            n.end = n.inner_start
            return
        self.cur = n

    def handle_startendtag(self, tag, attrs):
        p = self.pos()
        raw = self.get_starttag_text() or ""
        n = Node(tag, attrs, p, p + len(raw), self.cur)
        n.end = n.inner_start
        self.cur.children.append(n)

    def handle_endtag(self, tag):
        p = self.pos()
        if tag in VOID:
            return
        node = self.cur
        while node is not self.root and node.tag != tag:
            node = node.parent
        if node is self.root:
            self.errors.append(("stray </%s>" % tag, p))
            return
        n = self.cur
        while n is not node:
            self.errors.append(("unclosed <%s> (closed by </%s>)" % (n.tag, tag), n.start))
            n.end = p
            n = n.parent
        node.end = p
        self.cur = node.parent


def line_of(src, pos):
    return src.count("\n", 0, pos) + 1


def tag_seq(inner):
    return Counter(t.lower() for t in re.findall(r"<\s*/?\s*([a-zA-Z][\w-]*)", inner))


def tags_balanced(inner):
    st = []
    for m in re.finditer(r"<\s*(/?)\s*([a-zA-Z][\w-]*)[^>]*?(/?)>", inner):
        close, t, selfc = m.group(1), m.group(2).lower(), m.group(3)
        if t in VOID or selfc:
            continue
        if not close:
            st.append(t)
        else:
            if not st or st[-1] != t:
                return False
            st.pop()
    return not st


def add(issues, kind, where, lang, detail, sev="error"):
    issues.append({"kind": kind, "where": where, "lang": lang, "detail": detail, "sev": sev})


def check_guide_static(issues):
    path = os.path.join(ROOT, "guide.html")
    src = open(path, encoding="utf-8").read()
    tree = Tree(src)
    for msg, p in tree.errors:
        add(issues, "html-structure", "guide.html:%d" % line_of(src, p), "*", msg)
    groups = 0

    def walk(node):
        nonlocal groups
        kids = node.children
        i = 0
        while i < len(kids):
            if "data-l" in kids[i].attrs:
                j = i
                while j < len(kids) and "data-l" in kids[j].attrs:
                    j += 1
                check_group(kids[i:j])
                groups += 1
                for k in kids[i:j]:
                    walk(k)
                i = j
            else:
                walk(kids[i])
                i += 1

    def check_group(g):
        where = "guide.html:%d" % line_of(src, g[0].start)
        ls = [k.attrs.get("data-l") for k in g]
        if ls != LANGS:
            add(issues, "span-group", where, "*", "languages %s (expected %s)" % (ls, LANGS))
        tags = set(k.tag for k in g)
        if len(tags) > 1:
            add(issues, "span-group", where, "*", "mixed element types %s" % tags)
        inner = {}
        for k in g:
            l = k.attrs.get("data-l")
            if k.end is None:
                add(issues, "html-structure", where, l, "span never closed")
                continue
            inner[l] = src[k.inner_start:k.end]
        en = inner.get("en")
        if en is None:
            return
        en_tags, en_nums = tag_seq(en), numbers(en)
        en_txt = strip_tags(en).strip()
        for l, s in inner.items():
            txt = strip_tags(s).strip()
            if not txt and en_txt:
                add(issues, "empty", where, l, "empty translation of %r" % en_txt[:60])
                continue
            if "data-l=" in s:
                add(issues, "nested-lang", where, l, "span contains other data-l spans")
            if not tags_balanced(s):
                add(issues, "tags-unbalanced", where, l, s[:120])
            elif tag_seq(s) != en_tags:
                add(issues, "tags-differ", where, l, "%s vs en %s" % (dict(tag_seq(s)), dict(en_tags)), "warn")
            if l != "en" and any(numbers_mismatch(en, s)):
                add(issues, "numbers-differ", where, l, "missing %s extra %s | %s" % (numbers_mismatch(en, s) + (txt[:70],)))
            for kind, d in script_issues(l, txt):
                add(issues, kind, where, l, "%s | %s" % (d, txt[:80]), "warn" if kind == "latin-fragment" else "error")
            if STEP_PREFIX_RX.match(txt) and not STEP_PREFIX_RX.match(en_txt):
                add(issues, "step-prefix", where, l, txt[:60])
            if l != "en" and len(en_txt) > 12 and txt == en_txt and not unknown_latin(en_txt) == []:
                add(issues, "untranslated", where, l, txt[:70], "warn")
        seen = defaultdict(list)
        for l, s in inner.items():
            seen[strip_tags(s).strip()].append(l)
        for t, ls2 in seen.items():
            if len(ls2) > 1 and len(t) > 15 and unknown_latin(t) and not set(ls2) <= {"en", "de", "fr"}:
                add(issues, "copied-across-langs", where, ",".join(ls2), t[:70])

    walk(tree.root)
    # placeholder attributes
    for m in re.finditer(r"<[^>]*data-ph-en=[^>]*>", src):
        tag = m.group(0)
        for l in LANGS:
            v = re.search(r'data-ph-%s="([^"]*)"' % l, tag)
            if not v:
                add(issues, "placeholder-missing", "guide.html:%d" % line_of(src, m.start()), l, tag[:80])
            else:
                for kind, d in script_issues(l, html.unescape(v.group(1))):
                    add(issues, kind, "guide.html:%d placeholder" % line_of(src, m.start()), l, d)
    return groups


# ---------------------------------------------------------------- static: site.js dict
def load_js_object(path, name):
    code = r"""
    const fs=require('fs'); const s=fs.readFileSync(process.argv[1],'utf8'); const name=process.argv[2];
    const i=s.indexOf('const '+name+' = '); if(i<0){console.log('null');process.exit(0);}
    let j=s.indexOf('{',i), d=0, q=null, k=j;
    for(;k<s.length;k++){const c=s[k]; if(q){ if(c==='\\'){k++;continue;} if(c===q)q=null; continue;}
      if(c==='"'||c==="'"||c==='`'){q=c;continue;} if(c==='{')d++; else if(c==='}'){d--; if(!d)break;}}
    console.log(JSON.stringify((0,eval)('('+s.slice(j,k+1)+')')));
    """
    out = subprocess.run(["node", "-e", code, path, name], capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def check_site_static(issues):
    path = os.path.join(ROOT, "site.js")
    d = load_js_object(path, "dict")
    en = d["en"]
    for l in LANGS:
        if l not in d:
            add(issues, "dict-lang-missing", "site.js", l, "no dict[%s]" % l)
            continue
        miss = set(en) - set(d[l])
        extra = set(d[l]) - set(en)
        for k in sorted(miss):
            add(issues, "dict-key-missing", "site.js:" + k, l, "falls back / missing")
        for k in sorted(extra):
            add(issues, "dict-key-extra", "site.js:" + k, l, "not in en", "warn")
        for k, v in d[l].items():
            if k not in en or not isinstance(v, str):
                continue
            where = "site.js:" + k
            txt = strip_tags(v).strip()
            if not tags_balanced(v):
                add(issues, "tags-unbalanced", where, l, v[:100])
            elif tag_seq(v) != tag_seq(en[k]):
                add(issues, "tags-differ", where, l, "%s vs en %s" % (dict(tag_seq(v)), dict(tag_seq(en[k]))), "warn")
            if l != "en" and any(numbers_mismatch(en[k], v)):
                add(issues, "numbers-differ", where, l, "missing %s extra %s | %s" % (numbers_mismatch(en[k], v) + (txt[:70],)))
            for kind, det in script_issues(l, txt):
                add(issues, kind, where, l, "%s | %s" % (det, txt[:80]), "warn" if kind == "latin-fragment" else "error")
            if STEP_PREFIX_RX.match(txt) and not STEP_PREFIX_RX.match(strip_tags(en[k]).strip()):
                add(issues, "step-prefix", where, l, txt[:60])
            if l != "en" and v == en[k] and unknown_latin(strip_tags(v)):
                add(issues, "untranslated", where, l, txt[:70], "warn" if l in ("de", "fr") else "error")
            for l2 in LANGS:
                if l2 != l and l2 != "en" and l2 in d and d[l2].get(k) == v and len(txt) > 6 and l != "en" and unknown_latin(txt):
                    if LANGS.index(l2) < LANGS.index(l):
                        add(issues, "copied-across-langs", where, l + "," + l2, txt[:70])


# ---------------------------------------------------------------- dynamic (CDP)
COLLECT_JS = r"""
(lang) => {
  const out = [];
  const skip = new Set(['SCRIPT','STYLE','NOSCRIPT','TEMPLATE']);
  const vis = (el) => { if (!el) return false; if (el.closest('[hidden]') && !el.closest('details')) return false;
    if (el.checkVisibility) return el.checkVisibility({checkOpacity:false, checkVisibilityCSS:true}); return !!el.getClientRects().length; };
  const path = (el) => { const p=[]; while (el && el.nodeType===1 && p.length<4) { let s=el.tagName.toLowerCase(); if (el.id) s+='#'+el.id; else if (el.classList && el.classList.length) s+='.'+[...el.classList].slice(0,2).join('.'); p.unshift(s); el=el.parentElement; } return p.join('>'); };
  const tw = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let n;
  while ((n = tw.nextNode())) {
    const el = n.parentElement; if (!el || skip.has(el.tagName)) continue;
    if (el.closest('[translate="no"],code,kbd')) continue;
    const t = n.nodeValue.replace(/\s+/g,' ').trim(); if (!t) continue;
    if (!vis(el)) continue;
    out.push({t, where: path(el)});
  }
  document.querySelectorAll('[aria-label],[title],[alt],[placeholder]').forEach(el => {
    if (el.closest('[data-l]') && el.closest('[data-l]').getAttribute('data-l') !== lang) return;
    for (const a of ['aria-label','title','alt','placeholder']) { const v = el.getAttribute(a); if (v && v.trim()) out.push({t: v.trim(), where: path(el)+'@'+a}); }
  });
  out.push({t: document.title, where: 'title'});
  document.querySelectorAll('meta[name=description],meta[property^="og:"],meta[name^="twitter:"]').forEach(m => {
    const k = m.getAttribute('name') || m.getAttribute('property'); if (/title|description/.test(k)) out.push({t: m.content, where: 'meta:'+k}); });
  const wrong = [...document.querySelectorAll('[data-l]')].filter(e => e.getAttribute('data-l') !== lang && e.parentElement && vis(e.parentElement) && getComputedStyle(e).display !== 'none').map(e => path(e)+'[data-l='+e.getAttribute('data-l')+']');
  return {texts: out, wrongVisible: wrong.slice(0, 20), wrongCount: wrong.length,
          htmlLang: document.documentElement.lang, dir: document.documentElement.dir};
}
"""

STEPS_JS = r"""
() => {
  const res = [];
  const vis = (el) => el && (el.checkVisibility ? el.checkVisibility() : !!el.getClientRects().length);
  const marker = (li) => { const cs = getComputedStyle(li); return cs.display === 'list-item' && cs.listStyleType !== 'none' && li.parentElement && li.parentElement.tagName === 'OL'; };
  const startsNum = (s) => /^\s*[\d\u0660-\u0669\uff10-\uff19]+\s*[.)\u3001\uff0e:\-\u2013]?\s/.test(s);
  document.querySelectorAll('.stepper').forEach((box, bi) => {
    if (!vis(box)) return;
    const ol = box.querySelector('ol.steps');
    const direct = ol.querySelectorAll(':scope > li').length, allLi = ol.querySelectorAll('li').length;
    const dots = box.querySelectorAll('.st-dots button').length;
    if (direct !== allLi) res.push({kind: 'stepper-nesting', box: box.className, detail: direct + ' direct <li> of ' + allLi});
    if (dots && dots !== direct) res.push({kind: 'stepper-dots', box: box.className, detail: dots + ' dots for ' + direct + ' steps'});
    const lis = ol.querySelectorAll(':scope > li');
    lis.forEach((li, k) => {
      const shown = [];
      const b = li.querySelector('h3 .n'); if (b && vis(b)) shown.push('badge:' + b.textContent.trim());
      if (marker(li) && vis(li)) shown.push('marker');
      const dot = box.querySelectorAll('.st-dots button')[k]; if (dot && vis(dot)) { const bc = getComputedStyle(dot, '::before').content; const dt = (dot.textContent + ' ' + (bc && bc !== 'none' && bc !== 'normal' ? bc.replace(/"/g, '') : '')).trim(); if (/\d/.test(dt)) shown.push('dot:' + dt); }
      const h = li.querySelector('h3'); if (h) { const tx = [...h.childNodes].filter(c => !(c.classList && c.classList.contains('n'))).map(c => c.textContent).join(' ').trim();
        const vt = [...h.querySelectorAll('[data-l]')].filter(vis).map(e => e.textContent).join(' ').trim() || tx;
        if (startsNum(vt)) shown.push('text:' + vt.slice(0, 12)); }
      // Only the active step is displayed; inactive steps are checked when their dot is clicked (dyn states).
      if (vis(li) && shown.length !== 1) res.push({kind: 'step-number-count', box: box.className, step: k + 1, detail: shown.join(' + ') || 'none'});
      if (!b || !/^\d+$/.test(b.textContent.trim())) res.push({kind: 'step-number-count', box: box.className, step: k + 1, detail: 'missing badge'});
      const exp = String(k + 1); (b ? ['badge:' + b.textContent.trim()] : []).concat(shown.filter(s => /^dot:/.test(s))).forEach(s => { if (s.split(':')[1] !== exp) res.push({kind: 'step-number-wrong', box: box.className, step: k+1, detail: s}); });
    });
  });
  document.querySelectorAll('ol').forEach(ol => { if (ol.closest('.stepper') || !vis(ol)) return;
    ol.querySelectorAll(':scope > li').forEach((li, k) => { if (!marker(li)) return; const t = li.innerText.trim(); if (startsNum(t)) res.push({kind: 'step-number-count', box: 'ol', step: k+1, detail: 'marker + text ' + t.slice(0, 20)}); }); });
  document.querySelectorAll('.num').forEach((num, k) => { if (!vis(num)) return; const card = num.parentElement; const h = card.querySelector('h3');
    const vt = h ? [...h.querySelectorAll('[data-l],[data-i18n]')].filter(vis).map(e => e.textContent).join(' ').trim() || h.innerText.trim() : '';
    if (startsNum(vt)) res.push({kind: 'step-number-count', box: '.num card', step: k+1, detail: num.textContent.trim() + ' + ' + vt.slice(0, 20)}); });
  document.querySelectorAll('[data-i18n],[data-i18n-html]').forEach(el => { if (!vis(el)) return; const p = el.previousElementSibling; const t = el.textContent.trim();
    if (p && /^\d+$/.test(p.textContent.trim()) && vis(p) && startsNum(t)) res.push({kind: 'step-number-count', box: 'landing', detail: p.textContent.trim() + ' + ' + t.slice(0, 20)}); });
  return res;
}
"""

EXPAND_JS = r"""
() => { document.querySelectorAll('details').forEach(d => { d.removeAttribute('hidden'); d.open = true; }); return document.querySelectorAll('details').length; }
"""


def dyn_states(page, url_path):
    """Yield labels while cycling through tabs / pickers / stepper steps so hidden panes get rendered."""
    yield "base"
    for sel, lab in (("[data-tour] [data-tab]", "tab"), ("[data-picker] [data-pick]", "pick"), (".stepper .st-dots button", "step")):
        n = page.evaluate("(s) => document.querySelectorAll(s).length", sel)
        for i in range(n):
            ok = page.evaluate("([s,i]) => { const b = document.querySelectorAll(s)[i]; if (!b || !(b.checkVisibility ? b.checkVisibility() : b.offsetParent)) return false; b.click(); return true; }", [sel, i])
            if ok:
                yield "%s%d" % (lab, i)


def check_dynamic(issues, base, cdp):
    from playwright.sync_api import sync_playwright
    stats = Counter()
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(cdp)
        ctx = browser.contexts[0] if browser.contexts else browser.new_context()
        page = ctx.new_page()
        page.set_viewport_size({"width": 1280, "height": 900})
        console = []
        page.on("console", lambda m: console.append((m.type, m.text)) if m.type == "error" else None)
        page.on("pageerror", lambda e: console.append(("pageerror", str(e))))
        en_texts = {}
        targets = [("index.html", None)] + [("guide.html", m) for m in ("usb", "wireless")]
        for lang in LANGS:
            for path, mode in targets:
                console.clear()
                url = "%s/%s?lang=%s%s" % (base.rstrip("/"), path, lang, ("#" + mode) if mode else "")
                page.goto("about:blank")
                page.goto(url, wait_until="load")
                page.wait_for_timeout(250)
                label = "%s%s" % (path, ("#" + mode) if mode else "")
                page.evaluate(EXPAND_JS)
                texts = {}
                wrong = 0
                for st in dyn_states(page, path):
                    r = page.evaluate(COLLECT_JS, lang)
                    if r["htmlLang"] != LANG_HTML[lang] or r["dir"] != ("rtl" if lang == "ar" else "ltr"):
                        add(issues, "html-lang", label, lang, "lang=%s dir=%s" % (r["htmlLang"], r["dir"]))
                    if r["wrongCount"] and not wrong:
                        wrong = r["wrongCount"]
                        add(issues, "wrong-lang-visible", label + " " + st, lang, "%d visible: %s" % (wrong, r["wrongVisible"][:5]))
                    for t in r["texts"]:
                        texts.setdefault(t["t"], t["where"] + " [" + st + "]")
                    if st.startswith("step") or st == "base":
                        for s in page.evaluate(STEPS_JS):
                            add(issues, s["kind"], label + " " + st + " " + s.get("box", ""), lang, "step %s: %s" % (s.get("step", "-"), s["detail"]))
                stats[lang] += len(texts)
                if lang == "en":
                    en_texts[label] = set(texts)
                for t, where in texts.items():
                    for kind, d in script_issues(lang, t):
                        add(issues, kind, label + " " + where, lang, "%s | %s" % (d, t[:80]), "warn" if kind == "latin-fragment" else "error")
                    if lang != "en" and t in en_texts.get(label, ()) and len(t) > 12 and len(unknown_latin(UI_LITERALS_RX.sub(" ", t))) >= 2:
                        add(issues, "english-leak", label + " " + where, lang, t[:80], "error" if lang in NATIVE else "warn")
                for typ, txt in console:
                    add(issues, "console-error", label, lang, txt[:200])
        page.close()
    return stats


def dedupe(issues):
    seen, out = set(), []
    for i in issues:
        k = (i["kind"], i["lang"], i["detail"], i["where"].split(" ")[0] if i["kind"].startswith("script") or i["kind"] in ("latin-only", "latin-fragment", "english-leak", "mt-placeholder") else i["where"])
        if k in seen:
            continue
        seen.add(k)
        out.append(i)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="http://127.0.0.1:8765")
    ap.add_argument("--cdp", default="http://127.0.0.1:9222")
    ap.add_argument("--static-only", action="store_true")
    ap.add_argument("--json")
    ap.add_argument("--show-warn", action="store_true")
    ap.add_argument("--max", type=int, default=400)
    a = ap.parse_args()
    issues = []
    g = check_guide_static(issues)
    check_site_static(issues)
    print("static: %d guide.html span groups checked" % g)
    if not a.static_only:
        st = check_dynamic(issues, a.base, a.cdp)
        print("dynamic: visible strings per language:", dict(st))
    issues = dedupe(issues)
    errs = [i for i in issues if i["sev"] == "error"]
    warns = [i for i in issues if i["sev"] != "error"]
    by = Counter((i["lang"], i["kind"]) for i in errs)
    show = errs + (warns if a.show_warn else [])
    for i in show[: a.max]:
        print("%-5s %-20s %-6s %s :: %s" % (i["sev"][:4].upper(), i["kind"], i["lang"], i["where"], i["detail"]))
    print("\nerrors by language/kind:")
    for (l, k), n in sorted(by.items()):
        print("  %-6s %-22s %d" % (l, k, n))
    print("TOTAL errors=%d warnings=%d" % (len(errs), len(warns)))
    if a.json:
        json.dump(issues, open(a.json, "w"), ensure_ascii=False, indent=1)
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
