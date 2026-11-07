"""VisualBuild product-family homepage, with a shared product-form illustration."""
from html import escape as esc

PRODUCTS=(
  ('stackhub','StackHub','stackShort','stackPitch','stackPoints','stackNote','AI / MCP'),
  ('flexhub','FlexHub','flexShort','flexPitch','flexPoints','flexNote','PHONE / HID'),
  ('transferhub','TransferHub','transferShort','transferPitch','transferPoints','transferNote','Wi-Fi / USB'),
)

def link(href,label,primary=False):
    klass='btn family-btn'+(' primary family-btn-primary' if primary else '')
    return f'<a class="{klass}" href="{esc(href,quote=True)}" data-local>{esc(label)}</a>'

def render(language,m,c):
    e=lambda value: esc(str(value),quote=True)
    figure=(
      '<div class="family-device">'
      '<div class="family-device-glow" aria-hidden="true"></div>'
      '<figure class="family-device-frame">'
      f'<img src="assets/product-illustration.svg" loading="eager" decoding="async" '
      f'width="240" height="217" alt="{e(m["coreDesc"])}">'
      '</figure>'
      f'<div class="family-device-title"><span>{e(m["coreEyebrow"])}</span>'
      f'<strong>{e(m["coreTitle"])}</strong></div>'
      f'<p class="family-device-note">{e(m["coreDesc"])}</p>'
      '</div>'
    )
    nodes=[]
    for index,(slug,name,desc,_,_,_,_) in enumerate(PRODUCTS,1):
        nodes.append(
          f'<a href="#family-{slug}-{language}" class="family-node family-node-{slug}" '
          f'aria-label="{e(name)}: {e(m[desc])}">'
          f'<span class="family-node-number">{index:02d}</span>'
          f'<h3>{name}</h3><p>{e(m[desc])}</p>'
          f'<span class="family-node-arrow" aria-hidden="true">↗</span></a>')
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
      '<div class="family-branch-stem" aria-hidden="true"></div>'
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
