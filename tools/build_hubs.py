from pathlib import Path
import json,html
p=Path(__file__).resolve().parents[1]
packs=json.loads((p/'hub-content.json').read_text(encoding='utf-8'))
def esc(s):return html.escape(s)
def link(url,text,primary=False):
 return '<a data-local class="btn '+('primary' if primary else '')+'" href="'+url+'">'+esc(text)+'</a>'
def shell(name,blocks):
 title={'index':'VisualBuild — FlexHub, TransferHub, StackHub','transferhub':'TransferHub — bidirectional file transfer','stackhub':'StackHub — USB browser MCP bridge','transferhub-guide':'TransferHub user guide','stackhub-guide':'StackHub user guide'}[name]
 desc={'index':'Three hubs for device control, bidirectional file transfer and MCP bridging.','transferhub':'Transfer files between a Wi-Fi phone and USB computer, online or offline.','stackhub':'Connect Chan MCP to a backend via a computer browser and USB.','transferhub-guide':'Set up phone-to-computer and computer-to-phone file transfers.','stackhub-guide':'Configure Wi-Fi, Chan WSS, backend MCP and the USB browser bridge.'}[name]
 url='https://visualbuild.shop/'+('' if name=='index' else name+'.html')
 alts=''.join('<link rel="alternate" hreflang="'+('zh-Hans' if l=='zh' else l)+'" href="'+url+'?lang='+l+'">' for l in packs)
 return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+esc(title)+'</title><meta name="description" content="'+esc(desc)+'"><link rel="canonical" href="'+url+'">'+alts+'<meta property="og:title" content="'+esc(title)+'"><meta property="og:description" content="'+esc(desc)+'"><meta property="og:url" content="'+url+'"><link rel="icon" href="assets/mark.svg"><link rel="stylesheet" href="hubs.css"></head><body><a class="skip" href="#main">Skip to content</a><header><a class="brand" data-local href="index.html">VisualBuild<span style="color:#ef8700">.</span></a><nav aria-label="Products"><a data-local href="flexhub.html">FlexHub</a><a data-local href="transferhub.html">TransferHub</a><a data-local href="stackhub.html">StackHub</a></nav><select id="hub-lang" aria-label="Language">'+''.join('<option value="'+l+'">'+v+'</option>' for l,v in [('en','EN'),('zh','中文'),('de','DE'),('fr','FR'),('ja','日本語'),('ko','한국어'),('ar','العربية')])+'</select></header><main id="main">'+''.join('<article class="lang-block '+('active' if l=='en' else '')+'" data-lang="'+l+'">'+b+'</article>' for l,b in blocks.items())+'</main><footer><p>© 2026 VisualBuild · FlexHub / TransferHub / StackHub</p><a href="contact.html">Contact</a><a href="shipping.html">Shipping</a><a href="refund.html">Refunds</a><a href="privacy.html">Privacy</a><a href="terms.html">Terms</a></footer><script src="hubs.js"></script></body></html>'
pages={n:{} for n in ['index','transferhub','stackhub','transferhub-guide','stackhub-guide']}
for l,c in packs.items():
 cards=''
 for num,key,title in [('01','flex','FlexHub'),('02','transfer','TransferHub'),('03','stack','StackHub')]:
  url={'flex':'flexhub','transfer':'transferhub','stack':'stackhub'}[key]
  guide='guide.html' if key=='flex' else url+'-guide.html'
  cards+='<section class="card"><span class="number">'+num+'</span><h2>'+title+'</h2><p>'+esc(c[key])+'</p><div class="actions">'+link(url+'.html',c['details'],True)+link(guide,c['guide'])+'</div></section>'
 pages['index'][l]='<section class="hero"><span class="eyebrow">VISUALBUILD / HUB COLLECTION</span><h1>'+esc(c['home'])+'</h1><p class="lead">'+esc(c['intro'])+'</p></section><div class="cards">'+cards+'</div><p class="note">'+esc(c['note'])+'</p>'
 for key,title,stem in [('transfer','TransferHub','t'),('stack','StackHub','s')]:
  name=key+'hub';guide=name+'-guide.html'
  flow=['Wi-Fi browser','TransferHub','USB browser'] if key=='transfer' else ['Chan / WSS','StackHub','USB browser','MCP backend']
  diagram='<div class="flow">'+ '<b aria-hidden="true">↔</b>'.join('<span>'+esc(v)+'</span>' for v in flow)+'</div>'
  actions=link(guide,c['guide'],True)+link('contact.html?product='+name,c['buy'])
  if key=='transfer':actions+=link('transfer/index.html',c['open'])+ '<a class="btn" href="transfer/FlexHub-Offline.zip" download>'+esc(c['zip'])+'</a>'
  pages[name][l]='<section class="hero"><span class="eyebrow">'+title.upper()+'</span><h1>'+esc(c[key])+'</h1><div class="actions">'+actions+'</div></section><section class="section"><h2>'+esc(c['flow'])+'</h2>'+diagram+'</section><section class="section"><h2>'+esc(c['setup'])+'</h2><p>'+esc(c[stem+'setup'])+'</p></section><section class="section"><h2>'+esc(c['limits'])+'</h2><p>'+esc(c[stem+'limits'])+'</p></section><p class="note">'+esc(c['pending'])+'</p>'
  guidebody='<section class="hero"><span class="eyebrow">'+title.upper()+'</span><h1>'+title+' · '+esc(c['guide'])+'</h1><div class="actions">'+link(name+'.html',c['details'])+link('index.html',c['back'])+'</div></section><section class="section"><h2>'+esc(c['setup'])+'</h2><p>'+esc(c[stem+'setup'])+'</p></section><section class="section"><h2>'+esc(c['steps'])+'</h2><ol>'+''.join('<li>'+esc(x)+'</li>' for x in c[stem+'steps'])+'</ol></section>'
  if key=='transfer':guidebody+='<div class="actions">'+link('transfer/index.html',c['open'],True)+'<a class="btn" href="transfer/FlexHub-Offline.zip" download>'+esc(c['zip'])+'</a></div>'
  else:
   example={'mcpServers':{'local':{'url':'http://127.0.0.1:8800/mcp-http','headers':{'Authorization':'YOUR_SERVICE_AUTH_VALUE'}}}}
   guidebody+='<section class="section"><p>'+esc(c['example'])+'</p><pre><code>'+esc(json.dumps(example,indent=2))+'</code></pre><pre><code>python tools/install_host.py --asb-root &quot;PATH_TO_ASB&quot;</code></pre><p><code>https://YOUR_MCP_HOST/mcp-http?asb_service_api_key=YOUR_URL_ENCODED_KEY</code></p></section>'
  guidebody+='<section class="section"><h2>'+esc(c['limits'])+'</h2><p>'+esc(c[stem+'limits'])+'</p></section>'
  pages[name+'-guide'][l]=guidebody
for name,blocks in pages.items():(p/(name+'.html')).write_text(shell(name,blocks),encoding='utf-8')
print('Generated five pages in seven languages')
