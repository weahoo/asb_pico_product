#!/usr/bin/env python3
"""Build the Flexhub legal pages (privacy, terms, refund, shipping, contact) in 7 languages.

Source of truth: legal_src/<page>/en.md (English prevails). Translations: legal_src/<page>/<lang>.md
with exactly the same block structure (same headings / paragraphs / list items in the same order,
same [placeholders] and same link targets). Shared UI strings: legal_src/common.json.

Source format:  front matter (title / description / h1 / nav) then a line "---", then one block
per line: "## " h2, "### " h3, "- " list item, anything else = paragraph. Blank lines are ignored.
Inline: **bold**, [text](href), [Placeholder] (rendered highlighted, kept identical in every
language so it can be filled in once), bare https:// URLs.

Usage: python3 tools/build_legal.py [--check]   (--check: validate only, write nothing)
Output: privacy.html terms.html refund.html shipping.html contact.html in the repo root.
"""
import html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "legal_src")
LANGS = ["en", "zh", "de", "fr", "ja", "ko", "ar"]
LANG_HTML = {"en": "en", "zh": "zh-Hans", "de": "de", "fr": "fr", "ja": "ja", "ko": "ko", "ar": "ar"}
PAGES = ["privacy", "terms", "refund", "shipping", "contact"]
FOOTER = [("guide.html", "f.guide"), ("privacy.html", "f.privacy"), ("terms.html", "f.terms"),
          ("refund.html", "f.refund"), ("shipping.html", "f.shipping"), ("contact.html", "f.contact")]
UPDATED = "2026-10-10"
SITE = "https://visualbuild.shop/"
INLINE_RX = re.compile(r"\[([^\]\n]+)\]\(([^)\s]+)\)|\[([^\]\n]+)\]|(https?://[^\s<>()]*[^\s<>().,;:!?\u3002\uff0c])|\*\*(.+?)\*\*")
PH_RX = re.compile(r"\[([^\]\n]+)\](?!\()")
LINK_RX = re.compile(r"\[[^\]\n]+\]\(([^)\s]+)\)")


def parse(path):
    text = open(path, encoding="utf-8").read()
    head, body = text.split("\n---\n", 1)
    meta = {}
    for line in head.strip().split("\n"):
        k, v = line.split(":", 1)
        meta[k.strip()] = v.strip()
    blocks = []
    for line in body.split("\n"):
        line = line.rstrip()
        if not line.strip():
            continue
        if line.startswith("### "):
            blocks.append(("h3", line[4:].strip()))
        elif line.startswith("## "):
            blocks.append(("h2", line[3:].strip()))
        elif line.startswith("- "):
            blocks.append(("li", line[2:].strip()))
        else:
            blocks.append(("p", line.strip()))
    return meta, blocks


def inline(s):
    out, pos = [], 0
    for m in INLINE_RX.finditer(s):
        out.append(html.escape(s[pos:m.start()], quote=False))
        if m.group(1) is not None:
            out.append('<a href="%s">%s</a>' % (html.escape(m.group(2)), html.escape(m.group(1), quote=False)))
        elif m.group(3) is not None:
            out.append('<span class="ph" translate="no">[%s]</span>' % html.escape(m.group(3), quote=False))
        elif m.group(4) is not None:
            u = html.escape(m.group(4))
            out.append('<a href="%s" rel="noopener">%s</a>' % (u, u))
        else:
            out.append("<b>%s</b>" % html.escape(m.group(5), quote=False))
        pos = m.end()
    out.append(html.escape(s[pos:], quote=False))
    return "".join(out)


def validate(page, docs):
    errs = []
    en_meta, en_blocks = docs["en"]
    en_kinds = [k for k, _ in en_blocks]
    for l in LANGS:
        if l not in docs:
            errs.append("%s: missing %s.md" % (page, l))
            continue
        meta, blocks = docs[l]
        for key in ("title", "description", "h1", "nav"):
            if not meta.get(key):
                errs.append("%s/%s: front matter %r missing" % (page, l, key))
        kinds = [k for k, _ in blocks]
        if kinds != en_kinds:
            for i, (a, b) in enumerate(zip(en_kinds + ["-"] * 999, kinds + ["-"] * 999)):
                if a != b:
                    errs.append("%s/%s: block %d is %s, EN has %s (%d vs %d blocks) near: %s" % (
                        page, l, i + 1, b, a, len(kinds), len(en_kinds), (blocks[i][1] if i < len(blocks) else "")[:50]))
                    break
            continue
        for i, ((_, t), (_, et)) in enumerate(zip(blocks, en_blocks)):
            if sorted(PH_RX.findall(t)) != sorted(PH_RX.findall(et)):
                errs.append("%s/%s block %d: placeholders %s vs EN %s" % (page, l, i + 1, PH_RX.findall(t), PH_RX.findall(et)))
            if LINK_RX.findall(t) != LINK_RX.findall(et):
                errs.append("%s/%s block %d: links %s vs EN %s" % (page, l, i + 1, LINK_RX.findall(t), LINK_RX.findall(et)))
    return errs


def render_doc(page, l, meta, blocks, common):
    d = ' dir="rtl"' if l == "ar" else ' dir="ltr"'
    h = ['<article class="legal-doc" data-l="%s" lang="%s"%s>' % (l, LANG_HTML[l], d)]
    h.append("<h1>%s</h1>" % inline(meta["h1"]))
    h.append('<p class="updated">%s <time datetime="%s">%s</time></p>' % (html.escape(common["updated"][l]), UPDATED, UPDATED))
    if l != "en":
        h.append('<p class="prevails">%s <a href="%s.html?lang=en" hreflang="en">%s</a></p>' % (
            html.escape(common["prevails"][l]), page, html.escape(common["enLink"][l])))
    h2s = [t for k, t in blocks if k == "h2"]
    if len(h2s) >= 4:
        h.append('<nav class="legal-toc" aria-label="%s"><b>%s</b><ol>' % (html.escape(common["toc"][l]), html.escape(common["toc"][l])))
        for i, t in enumerate(h2s):
            h.append('<li><a href="#%s-s%d">%s</a></li>' % (l, i + 1, inline(re.sub(r"^\d+\.\s*", "", t))))
        h.append("</ol></nav>")
    n2, in_ul = 0, False
    for k, t in blocks:
        if k != "li" and in_ul:
            h.append("</ul>")
            in_ul = False
        if k == "h2":
            n2 += 1
            h.append('<h2 id="%s-s%d">%s</h2>' % (l, n2, inline(t)))
        elif k == "h3":
            h.append("<h3>%s</h3>" % inline(t))
        elif k == "li":
            if not in_ul:
                h.append("<ul>")
                in_ul = True
            h.append("<li>%s</li>" % inline(t))
        else:
            h.append("<p>%s</p>" % inline(t))
    if in_ul:
        h.append("</ul>")
    h.append("</article>")
    return "\n".join(h)


def spans(common, key):
    return "".join('<span data-l="%s">%s</span>' % (l, html.escape(common[key][l])) for l in LANGS)


def render_page(page, docs, common, lang_select, early_js):
    en = docs["en"][0]
    url = SITE + page + ".html"
    alts = "\n".join('  <link rel="alternate" hreflang="%s" href="%s?lang=%s">' % (LANG_HTML[l], url, l) for l in LANGS)
    meta_json = {l: {"title": docs[l][0]["title"], "description": docs[l][0]["description"], "langLabel": common["langLabel"][l]} for l in LANGS}
    foot = " ·\n        ".join('<a href="%s">%s</a>' % (href, spans(common, key)) for href, key in FOOTER)
    body = "\n".join(render_doc(page, l, docs[l][0], docs[l][1], common) for l in LANGS)
    return """<!doctype html>
<!-- Generated by tools/build_legal.py from legal_src/%(page)s/*.md — edit the sources, not this file. -->
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>%(title)s</title>
  <meta name="description" content="%(desc)s">
  <meta name="robots" content="index,follow">
  <meta name="theme-color" content="#ffffff">
  <link rel="canonical" href="%(url)s">
%(alts)s
  <link rel="alternate" hreflang="x-default" href="%(url)s">
  <meta property="og:site_name" content="Flexhub">
  <meta property="og:type" content="website">
  <meta property="og:url" content="%(url)s">
  <meta property="og:title" content="%(title)s">
  <meta property="og:description" content="%(desc)s">
  <link rel="icon" href="assets/mark.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Sans+SC:wght@400;500;700&family=Noto+Sans+JP:wght@400;500;700&family=Noto+Sans+KR:wght@400;500;700&family=Noto+Sans+Arabic:wght@400;500;700&display=swap" rel="stylesheet">
  %(early)s
  <link rel="stylesheet" href="styles.css">
  <link rel="stylesheet" href="legal.css">
  <script type="application/json" id="legal-meta">%(meta)s</script>
</head>
<body class="legal">
  <a class="skip" href="#main">%(skip)s</a>
  <header class="top">
    <div class="wrap top-inner">
      <a class="brand" href="/">
        <div class="brand-mark" aria-hidden="true"><span>FH</span></div>
        <div class="brand-text"><b>Flexhub</b><small>%(tag)s</small></div>
      </a>
      <div class="nav-actions">
        <label class="sr-only" for="lang">%(langlabel)s</label>
        %(select)s
      </div>
    </div>
  </header>
  <main id="main" class="wrap">
%(body)s
    <p class="legal-back"><a class="btn btn-ghost btn-sm" href="/">%(back)s</a></p>
  </main>
  <footer>
    <div class="wrap foot">
      <div class="foot-brand">Flexhub</div>
      <div>
        %(foot)s
      </div>
      <p style="margin:0;width:100%%">© 2026 Flexhub · visualbuild.shop</p>
    </div>
  </footer>
  <script src="legal.js"></script>
</body>
</html>
""" % {"page": page, "title": html.escape(en["title"]), "desc": html.escape(en["description"]), "url": url, "alts": alts,
       "early": early_js, "meta": json.dumps(meta_json, ensure_ascii=False).replace("</", "<\\/"),
       "skip": spans(common, "skip"), "tag": spans(common, "brandTag"), "langlabel": spans(common, "langLabel"),
       "select": lang_select, "body": body, "back": spans(common, "back"), "foot": foot}


def main():
    check_only = "--check" in sys.argv
    common = json.load(open(os.path.join(SRC, "common.json"), encoding="utf-8"))
    guide = open(os.path.join(ROOT, "guide.html"), encoding="utf-8").read()
    lang_select = re.search(r'<select id="lang".*?</select>', guide, re.S).group(0)
    lang_select = re.sub(r'\s*data-a11y="[^"]*"', "", lang_select)
    early_js = re.search(r'<script>\(function\(\)\{try\{var L=.*?</script>', guide, re.S).group(0)
    all_errs = []
    for page in PAGES:
        docs = {}
        for l in LANGS:
            p = os.path.join(SRC, page, l + ".md")
            if os.path.exists(p):
                docs[l] = parse(p)
        errs = validate(page, docs)
        all_errs += errs
        if errs or check_only:
            continue
        out = render_page(page, docs, common, lang_select, early_js)
        open(os.path.join(ROOT, page + ".html"), "w", encoding="utf-8").write(out)
        print("wrote %s.html (%d blocks x %d languages)" % (page, len(docs["en"][1]), len(LANGS)))
    for e in all_errs:
        print("ERROR", e)
    sys.exit(1 if all_errs else 0)


if __name__ == "__main__":
    main()
