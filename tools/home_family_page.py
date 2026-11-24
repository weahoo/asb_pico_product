"""VisualBuild product-family homepage for three distinct hardware products."""
from html import escape as esc

PRODUCTS=(
  ('stackhub','StackHub','stackShort','stackPitch','stackPoints','stackNote','AI / MCP'),
  ('flexhub','FlexHub','flexShort','flexPitch','flexPoints','flexNote','PHONE / HID'),
  ('transferhub','TransferHub','transferShort','transferPitch','transferPoints','transferNote','Wi-Fi / USB'),
)

SUMMARY_ICONS={'wifi': '<path d="M2 8.5a16 16 0 0 1 20 0M5 12a11 11 0 0 1 14 0M8.5 15.5a5.5 5.5 0 0 1 7 0"/><circle cx="12" cy="19" r=".8" fill="currentColor"/>', 'usb': '<path d="M12 22V3m-3 3 3-3 3 3M12 16l-6-5V7m6 12 6-5v-3"/><circle cx="6" cy="5" r="2"/><rect x="16" y="7" width="4" height="4" rx=".5"/>', 'phone': '<rect x="6" y="2" width="12" height="20" rx="3"/><path d="M11 18h2"/>', 'shield': '<path d="M12 22s8-4 8-11V5l-8-3-8 3v6c0 7 8 11 8 11Z"/><path d="m9 12 2 2 4-4"/>', 'link': '<path d="m10 13 4-4m-6 7-1 1a4 4 0 0 1-6-6l4-4a4 4 0 0 1 6 0m2 10a4 4 0 0 0 6 0l4-4a4 4 0 0 0-6-6l-1 1"/>', 'tool': '<path d="M14 7a5 5 0 0 0-6-5l3 3-3 3-3-3a5 5 0 0 0 5 6l-7 7a2 2 0 0 0 3 3l7-7a5 5 0 0 0 6-5l-3 3-3-3z"/>', 'monitor': '<rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8m-4-4v4"/>', 'keyboard': '<rect x="2" y="5" width="20" height="14" rx="2"/><path d="M6 9h.1m4 0h.1m4 0h.1m4 0h.1M6 13h.1m4 0h.1m4 0h.1m4 0h.1M8 16h8"/>', 'pen': '<path d="m16 3 5 5M3 21l4-1 14-14a2 2 0 0 0-3-3L4 17l-1 4Z"/>', 'browser': '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="M2 9h20m-16-3h.1m3 0h.1"/>'}
SUMMARY_ORDER={"stackhub":("wifi","link","shield","monitor"),"flexhub":("keyboard","usb","pen","browser"),"transferhub":("wifi","usb","phone","shield")}
SUMMARY_EN={'stackhub': 'AI tools for computers that stay offline', 'flexhub': 'Your phone, your universal desktop controller', 'transferhub': 'Your pocket-sized private file-sharing network'}

def summary_icon(name):
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+SUMMARY_ICONS[name]+'</svg>'

def link(href,label,primary=False):
    klass='btn family-btn'+(' primary family-btn-primary' if primary else '')
    return f'<a class="{klass}" href="{esc(href,quote=True)}" data-local>{esc(label)}</a>'

def render(language,m,c):
    e=lambda value: esc(str(value),quote=True)
    figure=(
      '<div class="family-device family-products-overview">'
      '<div class="family-product-badges" aria-hidden="true">'
      '<span class="family-product-badge family-product-badge-stack">StackHub</span>'
      '<span class="family-product-badge family-product-badge-flex">FlexHub</span>'
      '<span class="family-product-badge family-product-badge-transfer">TransferHub</span>'
      '</div>'
      f'<div class="family-device-title"><span>{e(m["coreEyebrow"])}</span>'
      f'<strong>{e(m["coreTitle"])}</strong></div>'
      f'<p class="family-device-note">{e(m["coreDesc"])}</p>'
      '</div>'
    )
    nodes=[]
    for index,(slug,name,desc,_,_,_,_) in enumerate(PRODUCTS,1):
        summary=m['summaryCards'][slug]
        bullets=''.join(f'<li>{summary_icon(icon)}<span>{e(point)}</span></li>' for icon,point in zip(SUMMARY_ORDER[slug],summary['points']))
        subtitle=f'<p class="family-summary-en" lang="en" dir="ltr">{e(SUMMARY_EN[slug])}</p>' if language=='zh' else ''
        nodes.append(
          f'<a href="#family-{slug}-{language}" class="family-node family-node-{slug} family-summary" '
          f'aria-label="{e(name)}: {e(summary["title"])}">'
          f'<h3>{name}</h3><p class="family-summary-title">{e(summary["title"])}</p>{subtitle}'
          f'<figure class="hub-paper-art family-paper-art" aria-hidden="true"><img src="assets/{slug}-paper-cut.svg" width="400" height="480" alt="" decoding="async"></figure>'
          f'<ul class="family-summary-points">{bullets}</ul>'
          f'<span class="family-summary-more">{e(m["explore"])} <span aria-hidden="true">↗</span></span></a>')
    nodes.append(
      '<div class="family-node family-node-future">'
      '<span class="family-node-number">04</span>'
      f'<h3>{e(m["futureName"])}</h3><p>{e(m["futureShort"])}</p>'
      f'<span class="family-future-pill">{e(m["coming"])}</span>'
      '</div>')
    stories=[]
    for index,(slug,name,short,pitch,points,note,flow) in enumerate(PRODUCTS,1):
        points_html=''.join(f'<li>{e(value)}</li>' for value in m[points])
        guide='guide.html' if slug=='flexhub' else slug+'-guide.html'
        stories.append(
          f'<section class="family-story family-story-{slug}" id="family-{slug}-{language}">'
          '<div class="family-story-identity">'
          f'<span class="family-product-index">{index:02d} / 03</span>'
          f'<div class="family-mark" aria-hidden="true">{e(flow)}</div>'
          f'<h3>{name}</h3>'
          f'<p class="family-story-short">{e(m[short])}</p>'
          '</div>'
          '<div class="family-story-body">'
          f'<p class="family-story-pitch">{e(m[pitch])}</p>'
          f'<ul class="family-highlights">{points_html}</ul>'
          f'<p class="family-story-note">{e(m[note])}</p>'
          '<div class="actions family-story-actions">'
          +link(slug+'.html',m['explore'],True)
          +link(guide,m['guide'])
          +'</div></div></section>')
    return (
      '<div class="family-home" data-family-lang="'+language+'">'
      '<section class="family-hero">'
      f'<span class="eyebrow">{e(m["eyebrow"])}</span>'
      f'<h1>{e(m["headline"])}</h1>'
      f'<p class="lead">{e(m["lead"])}</p>'
      f'<p class="family-kicker">{e(m["familyTag"])}</p>'
      '</section>'
      '<section class="family-map" aria-label="'+e(m['mapLabel'])+'">'
      +figure+
      '<div class="family-node-grid">'+''.join(nodes)+'</div>'
      '</section>'
      '<section class="family-detail-intro" id="family-details-'+language+'">'
      f'<span class="eyebrow">{e(m["detailEyebrow"])}</span>'
      f'<h2>{e(m["detailHeadline"])}</h2>'
      f'<p>{e(m["detailLead"])}</p>'
      '</section>'
      '<div class="family-stories">'+''.join(stories)+'</div>'
      '<section class="family-next">'
      '<span class="family-next-spark" aria-hidden="true">＋</span>'
      '<div>'
      f'<span class="eyebrow">{e(m["coming"])}</span>'
      f'<h2>{e(m["moreHeadline"])}</h2><p>{e(m["moreDesc"])}</p>'
      '</div></section>'
      '</div>'
    )
