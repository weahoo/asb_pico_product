from pathlib import Path
import argparse
import zipfile
import os, shutil, importlib.util, hashlib, json

def generate(project, site=None):
    shared=Path(os.environ.get('FLEXHUB_TRANSFER_SOURCE',str(project.parents[1]/'asb_pico_product/transfer-src')))
    if shared.is_dir():
        for name in ('index.html','portal.html','offline-i18n.json','offline-README.txt'):
            shutil.copy2(shared/name,project/'web'/name)
        shutil.copy2(shared/'offline_assets.py',project/'tools/offline_assets.py')
    spec=importlib.util.spec_from_file_location('transfer_offline_assets',project/'tools/offline_assets.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    build_offline_assets=module.build_offline_assets
    (project/'generated').mkdir(exist_ok=True)
    html=(project/'web/index.html').read_text(encoding='utf-8')
    html=build_offline_assets(project,html)
    pages={role:html.replace('__ROLE__',role) for role in ('sender','receiver')}
    pages['portal']=(project/'web/portal.html').read_text(encoding='utf-8')
    arrays=[]
    for role, page in pages.items():
        data=page.encode('utf-8')+b'\0'
        arrays.append('static const unsigned char '+role+'_html[]={'+','.join(str(x) for x in data)+'};')
    (project/'generated/web_assets.h').write_text('\n'.join(arrays),encoding='utf-8')
    (project/'web/send.html').write_text(pages['sender'],encoding='utf-8')
    (project/'web/FlexHub-Receiver.html').write_bytes(pages['receiver'].encode('utf-8'))
    (project/'generated/ui-manifest.json').write_text(json.dumps({'source':str(shared) if shared.is_dir() else 'bundled snapshot','receiver_sha256':hashlib.sha256(pages['receiver'].encode('utf-8')).hexdigest()},indent=2),encoding='utf-8')
    if site:
        target=Path(site)/'transfer';target.mkdir(parents=True,exist_ok=True)
        for name in ('index.html','FlexHub-Receiver.html'):
            (target/name).write_bytes(pages['receiver'].encode('utf-8'))
        guide=(project/'web/offline-guide.html').read_bytes()
        (target/'offline-guide.html').write_bytes(guide)
        with zipfile.ZipFile(target/'FlexHub-Offline.zip','w',compression=zipfile.ZIP_DEFLATED) as archive:
            archive.writestr('FlexHub-Offline/FlexHub-Receiver.html',pages['receiver'].encode('utf-8'))
            archive.writestr('FlexHub-Offline/offline-guide.html',guide)
            archive.writestr('FlexHub-Offline/README.txt',(project/'web/offline-README.txt').read_bytes())
        print('Receiver exported to',target)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--site-dir',type=Path)
    args=parser.parse_args();generate(Path(__file__).resolve().parents[1],args.site_dir)
