# StackHub landing page. Never collects recovery codes or payment details.
from html import escape as e

BILLING='https://stackhub-billing.onrender.com/#payment'
HARDWARE='contact.html?product=stackhub'
PRICES={'basic':[(1,6,36),(3,17,102),(12,60,360)],
        'premium':[(1,20,120),(3,53,318),(12,200,1200)]}
LIMITS={'free':(1000,'32 KiB'),'basic':(10000,'1 MiB'),'premium':(50000,'5 MiB')}

def link(url,label,primary=False):
    cls='btn sh-btn'+(' primary sh-main-btn' if primary else '')
    return f'<a href="{e(url,quote=True)}" class="{cls}">{e(label)}</a>'

def render(lang,m,c):
    t=lambda x:e(x,quote=True)
    chips=''.join(f'<span class="sh-chip">{t(x)}</span>' for x in m['features'])
    cases=''.join(f'<article class="sh-use"><span class="sh-use-n">{i:02d}</span>'
                  f'<div><h3>{t(a)}</h3><p>{t(b)}</p></div></article>'
                  for i,(a,b) in enumerate(m['scenarios'],1))
    steps=''.join(f'<li><span class="sh-step-n">{i:02d}</span><span>{t(x)}</span></li>'
                  for i,x in enumerate(m['steps'],1))
    cards=''
    for tier,title in [('free',m['free']),('basic',m['basic']),('premium',m['pro'])]:
        calls,capacity=LIMITS[tier]
        if tier=='free':
            prices='<li class="sh-free-price">&#36;0</li>'
        else:
            prices=''.join(
                f'<li class="sh-price-row" data-plan="{tier}" data-months="{months}">'
                f'<span>{t(m["periods"][i])}</span><span>'
                f'<strong class="sh-usd">&#36;{usd}</strong>'
                f'<small class="sh-cny">≈ ¥{cny}</small></span></li>'
                for i,(months,usd,cny) in enumerate(PRICES[tier]))
        cards+=(
            f'<article class="sh-plan {"sh-featured" if tier=="premium" else ""}" data-tier="{tier}">'
            f'<h3>{t(title)}</h3><p class="sh-plan-usage">'
            f'<strong data-calls="{tier}">{calls:,}</strong> {t(m["calls"])} · '
            f'<span data-size="{tier}">{t(capacity)}</span></p>'
            f'<ul class="sh-price-list">{prices}</ul>'
            +(link(BILLING,m['buyPlan'],tier=='premium') if tier!='free'
              else link('stackhub-guide.html',m['guideBtn']))
            +'</article>')
    nav=(link(BILLING,m['buyPlan'],True)+link(HARDWARE,m['hardwareBtn'])
         +link('stackhub-guide.html',m['guideBtn']))
    warning=t(m['hardwareWarning']).replace('**','')
    return f"""
<div class="sh-landing" data-stack-lang="{lang}">
 <section class="sh-hero">
  <span class="eyebrow">STACKHUB / CONTROLLED AI BRIDGE</span>
  <h1>{t(m['headline'])}</h1><p class="sh-subhead">{t(m['subhead'])}</p>
  <p class="lead">{t(m['intro'])}</p>
  <div class="sh-chips">{chips}</div>
  <div class="actions sh-hero-actions">{nav}</div>
 </section>
 <section class="sh-axes">
  <article class="sh-axis"><span class="sh-axis-label">01 / VERTICAL</span><h2>{t(m['vertical'])}</h2>
   <p>{t(m['verticalDesc'])}</p></article>
  <article class="sh-axis"><span class="sh-axis-label">02 / HORIZONTAL</span><h2>{t(m['horizontal'])}</h2>
   <p>{t(m['horizontalDesc'])}</p><p class="sh-platforms">Claude · MCP AI · StackChan · Windows · macOS · Linux</p></article>
 </section>
 <section class="sh-illustration" aria-label="{t(m['sceneTitle'])}">
  <div class="sh-illustration-copy">
   <span class="eyebrow">STACKHUB / SCENARIO</span>
   <h2>{t(m['sceneTitle'])}</h2>
   <p>{t(m['sceneCaption'])}</p>
  </div>
  <figure class="sh-illustration-art">
   <img src="assets/stackhub-scenario-sketch-transparent.png" width="1012" height="920"
     loading="lazy" decoding="async" alt="{t(m['sceneAlt'])}">
  </figure>
 </section>
 <section class="sh-section"><span class="eyebrow">USE CASES</span>
  <h2>{t(m['scenariosTitle'])}</h2><div class="sh-use-grid">{cases}</div>
 </section>
 <section class="sh-section sh-workflow"><span class="eyebrow">SETUP</span>
  <h2>{t(m['stepsTitle'])}</h2>
  <div class="sh-path" aria-label="External AI, independent StackHub Wi-Fi, USB Bridge, offline computer">
   <span>External AI / MCP</span><b aria-hidden="true">→</b><span>StackHub · Wi-Fi</span>
   <b aria-hidden="true">→</b><span>USB Bridge</span><b aria-hidden="true">→</b><span>Offline PC / MCP</span>
  </div>
  <ol class="sh-steps">{steps}</ol>
  <p class="sh-coming"><strong>{t(m['siri'])}</strong> — {t(m['siriDesc'])}</p>
 </section>
 <section class="sh-section sh-pricing" id="plans-{lang}"><span class="eyebrow">SOFTWARE PLANS</span>
  <h2>{t(m['priceTitle'])}</h2><p>{t(m['priceIntro'])}</p>
  <p class="sh-hardware-note">{warning}</p>
  <div class="sh-plan-grid">{cards}</div>
  <p class="sh-price-note">{t(m['priceNote'])}</p>
  <p class="sh-live-status" data-price-status role="status" aria-live="polite"></p>
  <div class="actions">{link(BILLING,m['buyPlan'],True)}{link(HARDWARE,m['hardwareBtn'])}</div>
 </section>
 <section class="sh-section sh-owner stackhub-subscription" id="subscription-{lang}" data-subscription-lang="{lang}">
  <span class="eyebrow">ALREADY OWN A DEVICE?</span><h2>{t(m['already'])}</h2>
  <p>{t(m['alreadyDesc'])}</p>
  <label class="stackhub-id-label" for="stackhub-device-id-{lang}">{t(c['subLabel'])}</label>
  <input class="stackhub-device-id" type="text" id="stackhub-device-id-{lang}"
   maxlength="25" placeholder="stackhub-0123456789abcdef" autocomplete="off" spellcheck="false">
  <div class="actions">
   <button class="btn primary sh-btn stackhub-subscribe-buy" type="button">{t(c['subGo'])}</button>
   <button class="btn sh-btn stackhub-subscribe-copy" type="button">{t(c['subCopy'])}</button>
  </div>
  <p class="stackhub-subscribe-status" role="status" aria-live="polite"></p>
  <span class="stackhub-l10n" hidden data-invalid="{t(c['subInvalid'])}"
   data-copied="{t(c['subCopied'])}" data-copy-failed="{t(c['subCopyFailed'])}"></span>
 </section>
</div>"""
