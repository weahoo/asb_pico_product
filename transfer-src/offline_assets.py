
import json,html
def build_offline_assets(project, source):
    data=json.loads((project/'web/offline-i18n.json').read_text(encoding='utf-8'))
    labels={'en':'English','zh':'中文','de':'Deutsch','fr':'Français','ja':'日本語','ko':'한국어','ar':'العربية'}
    options=''.join('<option value="'+k+'">'+v+'</option>' for k,v in labels.items())
    sections=[]
    for lang,d in data.items():
        e=html.escape
        content='<h1>'+e(d['title'])+'</h1><p>'+e(d['intro'])+'</p><aside>'+e(d['needs'])+'</aside>'
        for title,items in zip(d['headings'],[d['steps'][:2],d['steps'][2:4],d['steps'][4:],d['notes']]):
            content+='<h2>'+e(title)+'</h2><ol>'+''.join('<li>'+e(x)+'</li>' for x in items)+'</ol>'
        content+='<p><a href="./FlexHub-Receiver.html">'+e(d['open'])+'</a></p>'
        sections.append('<section data-language="'+lang+'" lang="'+lang+'"'+(' hidden' if lang!='en' else '')+'>'+content+'</section>')
    choose="""function preferred(){const q=new URLSearchParams(location.search).get('lang');let s;try{s=localStorage.getItem('flexhub_lang')}catch{}return [q,s,(navigator.language||'en').split('-')[0],'en'].find(x=>languages.includes(x));}"""
    guide='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>FlexHub · Offline guide</title><style>body{font:16px/1.75 system-ui,sans-serif;color:#242428;background:#f5f5f7;margin:0;padding:24px}main{max-width:780px;margin:auto;background:white;padding:32px;border:1px solid #e4e4e8;border-radius:20px}h1{font-size:28px}h2{font-size:20px;margin-top:30px}a{color:#9b5200}li{margin:10px 0;overflow-wrap:anywhere}aside{background:#fff8ed;border-inline-start:3px solid #ff9500;padding:14px}select{font:inherit;max-width:100%;padding:8px;border:1px solid #ddd;border-radius:9px;background:white}[hidden]{display:none!important}</style></head><body><main><header><strong>FlexHub</strong> · <label for="guideLang">Language / 语言</label> <select id="guideLang">'''+options+'</select></header>'+''.join(sections)+'''<script>const languages=['en','zh','de','fr','ja','ko','ar'];'''+choose+'''
function change(lang){document.documentElement.lang=lang==='zh'?'zh-CN':lang;document.documentElement.dir=lang==='ar'?'rtl':'ltr';document.querySelectorAll('[data-language]').forEach(e=>e.hidden=e.dataset.language!==lang);document.title='FlexHub · '+document.querySelector('[data-language="'+lang+'"] h1').textContent;document.getElementById('guideLang').value=lang;try{localStorage.setItem('flexhub_lang',lang)}catch{}}
document.getElementById('guideLang').onchange=e=>change(e.target.value);change(preferred());</script></main></body></html>'''
    (project/'web/offline-guide.html').write_text(guide,encoding='utf-8')
    small={lang:{key:d[key] for key in ('download','html','hint','title')} for lang,d in data.items()}
    ui='<label for="downloadLang">Guide language / 指南语言</label><select id="downloadLang" style="font:inherit;padding:8px;border:1px solid #ddd;border-radius:8px;background:white">'+options+'''</select><div class="row" style="margin-top:14px"><a id="offlineDownload" class="button secondary" href="./FlexHub-Offline.zip" download="FlexHub-Offline.zip">Download offline ZIP</a><a id="offlineGuide" href="./offline-guide.html" target="_blank" rel="noopener">Guide</a></div><p id="offlineHint" class="small"></p><a id="offlineHtml" href="./FlexHub-Receiver.html" download="FlexHub-Receiver.html">Download HTML only</a>'''
    start=source.index('<div class="row"><a id="offlineDownload"')
    end=source.index('<p id="offlineState"',start)
    source=source[:start]+ui+source[end:]
    script='<script>(()=>{const messages='+json.dumps(small,ensure_ascii=False)+';const languages=Object.keys(messages);'+choose+'''
function setLanguage(lang){const d=messages[lang];const box=document.getElementById('receiverResources');box.dir=lang==='ar'?'rtl':'ltr';box.lang=lang;document.getElementById('downloadLang').value=lang;document.getElementById('offlineDownload').textContent=d.download;document.getElementById('offlineGuide').textContent=d.title;document.getElementById('offlineGuide').href='./offline-guide.html?lang='+lang;document.getElementById('offlineHint').textContent=d.hint;document.getElementById('offlineHtml').textContent=d.html;try{localStorage.setItem('flexhub_lang',lang)}catch{}}
document.getElementById('downloadLang').onchange=e=>setLanguage(e.target.value);setLanguage(preferred());})();</script>'''
    return source.replace('</body>',script+'</body>')
