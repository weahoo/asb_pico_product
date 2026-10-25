const CACHE='flexhub-transfer-v5-duplex';
const assets=['./','./index.html','./FlexHub-Receiver.html','./offline-guide.html','./FlexHub-Offline.zip'].map(p=>new URL(p,self.registration.scope).href);
self.addEventListener('install',event=>event.waitUntil(caches.open(CACHE).then(c=>c.addAll(assets))));
self.addEventListener('activate',event=>event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k.startsWith('flexhub-transfer-')&&k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',event=>{
 const key=new URL(event.request.url);key.search='';
 if(event.request.method!=='GET'||!assets.includes(key.href))return;
 event.respondWith(fetch(event.request).catch(()=>caches.match(key.href)));
});
