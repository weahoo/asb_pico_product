/* SmartHub site — i18n + checkout config */
(function () {
  const dict = {
    en: {
      "skip": "Skip to content",
      "nav.benefits": "Why you'll love it",
      "nav.how": "How it works",
      "nav.buy": "Buy",
      "nav.faq": "FAQ",
      "nav.cta": "Get SmartHub",
      "lang.label": "Language",
      "hero.eyebrow": "Old phone · new adventures",
      "hero.title": "Give your old phone<br><span class=\"accent\">a happy second life.</span>",
      "hero.lead": "That phone in your drawer still holds your favorite photos and memories. With SmartHub, it becomes a wireless controller again — play without cables, and always have a spare remote close at hand.",
      "hero.ctaPrimary": "Get SmartHub",
      "hero.ctaSecondary": "See what it can do",
      "hero.m1": "♥ Keep your memories",
      "hero.m2": "✦ Play cable-free",
      "hero.m3": "☀ A spare remote, always ready",
      "hero.illustCaption": "SmartHub product illustration",
      "chip.reuse": "Old phone, new job",
      "chip.wireless": "Cable-free play",
      "chip.backup": "Spare remote",
      "ben.kicker": "Why you'll love it",
      "ben.title": "One little plug. Three happy surprises.",
      "ben.b1t": "Your old phone, back in your hands",
      "ben.b1p": "The phone or tablet you couldn't bear to throw away — full of photos, messages and moments — gets a fresh new job. Keep every memory right where it is, and turn it into a handy wireless controller you can carry anywhere.",
      "ben.b2t": "Play free from cables",
      "ben.b2p": "No more tangled cords or sitting close to the screen. Grab your controller, lean back on the sofa and play from across the room — wireless, comfortable and fun.",
      "ben.b3t": "A spare remote, always ready",
      "ben.b3p": "Remote slipped under the cushions? Batteries gone flat? SmartHub is your dependable backup — pick up your phone and keep going, no searching required.",
      "how.kicker": "How it works",
      "how.title": "Ready in under a minute.",
      "how.lead": "No apps to install, no complicated setup. If you can plug in a USB stick, you're all set.",
      "how.s1t": "Plug it in",
      "how.s1p": "Pop SmartHub into a USB port on your computer or entertainment setup.",
      "how.s2t": "Pick up your phone",
      "how.s2p": "Connect your old phone or tablet to SmartHub and open its page — that's it.",
      "how.s3t": "Play and relax",
      "how.s3p": "Use your phone or your favorite controller to play, browse and control — from wherever you're comfy.",
      "quote.text": "Memories stay. The fun comes back.",
      "quote.by": "Don't let a good phone gather dust — let it play again.",
      "buy.kicker": "Coming soon",
      "buy.title": "Bring your old phone back to the fun.",
      "buy.lead": "SmartHub will be available at visualbuild.shop very soon. Pricing and shipping details are on the way — check back shortly!",
      "buy.priceNote": "Price coming soon",
      "buy.cta": "Coming soon",
      "buy.fine": "Secure checkout on visualbuild.shop",
      "faq.kicker": "FAQ",
      "faq.title": "Good questions, quick answers",
      "faq.q1": "Which old phones and tablets work?",
      "faq.a1": "Almost any phone or tablet with a web browser — even ones that no longer get updates. No app download needed.",
      "faq.q2": "Will it change anything on my old phone?",
      "faq.a2": "No. Your photos, messages and memories stay exactly as they are. SmartHub simply gives the phone a new way to be useful.",
      "faq.q3": "Can I use a game controller too?",
      "faq.a3": "Yes! Pair your wireless controller and play from the sofa — no cable running across the room.",
      "faq.q4": "Do I need to install anything on my computer?",
      "faq.a4": "Nope. Just plug SmartHub in and it's ready to go.",
      "faq.q5": "Does it replace my other remotes?",
      "faq.a5": "Think of it as a trusty backup. Keep your usual remote — and when it goes missing or runs out of battery, SmartHub has you covered.",
      "foot.privacy": "Privacy",
      "foot.terms": "Terms",
      "foot.refund": "Refunds",
      "foot.copy": "© 2026 VisualBuild · visualbuild.shop"
    },
    zh: {
      "skip": "跳到正文",
      "nav.benefits": "为什么喜欢它",
      "nav.how": "怎么用",
      "nav.buy": "购买",
      "nav.faq": "常见问题",
      "nav.cta": "获取 SmartHub",
      "lang.label": "语言",
      "hero.eyebrow": "旧手机 · 新乐趣",
      "hero.title": "让旧手机<br><span class=\"accent\">开心地再活一次。</span>",
      "hero.lead": "抽屉里那台旧手机，还存着你最珍贵的照片和回忆。有了 SmartHub，它重新变成一台无线遥控手柄——摆脱线缆尽情畅玩，还随时多一个备用遥控器。",
      "hero.ctaPrimary": "获取 SmartHub",
      "hero.ctaSecondary": "看看它能做什么",
      "hero.m1": "♥ 回忆完好保留",
      "hero.m2": "✦ 无线自在畅玩",
      "hero.m3": "☀ 备用遥控随手可得",
      "hero.illustCaption": "SmartHub 产品示意图",
      "chip.reuse": "旧手机新用途",
      "chip.wireless": "无线畅玩",
      "chip.backup": "备用遥控",
      "ben.kicker": "为什么喜欢它",
      "ben.title": "一个小小插头，三份惊喜。",
      "ben.b1t": "旧手机，重新回到你手中",
      "ben.b1p": "那台舍不得扔的手机或平板，装满了照片、聊天和珍贵时刻。现在它有了新工作——回忆原封不动地留着，它变成一台随身携带的无线遥控器。",
      "ben.b2t": "摆脱线缆，自在畅玩",
      "ben.b2p": "告别缠成一团的线，也不用凑在屏幕前。拿起手柄，靠在沙发上，隔着整个客厅也能尽情玩——无线、舒服、好玩。",
      "ben.b3t": "备用遥控，随时待命",
      "ben.b3p": "遥控器掉进沙发缝？电池没电了？SmartHub 就是你可靠的备用方案——拿起手机就能继续，不用到处翻找。",
      "how.kicker": "怎么用",
      "how.title": "一分钟就能用上。",
      "how.lead": "不用装 App，没有复杂设置。会插 U 盘，就会用 SmartHub。",
      "how.s1t": "插上它",
      "how.s1p": "把 SmartHub 插进电脑或娱乐设备的 USB 口。",
      "how.s2t": "拿起手机",
      "how.s2p": "让旧手机或平板连上 SmartHub，打开它的页面——就这么简单。",
      "how.s3t": "放松开玩",
      "how.s3p": "用手机或你喜欢的手柄来玩、来浏览、来控制——怎么舒服怎么来。",
      "quote.text": "回忆留下，快乐回来。",
      "quote.by": "别让好手机落灰——让它再玩起来。",
      "buy.kicker": "即将上市",
      "buy.title": "让旧手机重新加入快乐时光。",
      "buy.lead": "SmartHub 即将在 visualbuild.shop 上架。价格与配送信息马上公布——敬请期待！",
      "buy.priceNote": "价格即将公布",
      "buy.cta": "即将开售",
      "buy.fine": "在 visualbuild.shop 安全结账",
      "faq.kicker": "常见问题",
      "faq.title": "好问题，简单答",
      "faq.q1": "哪些旧手机和平板可以用？",
      "faq.a1": "几乎所有带浏览器的手机或平板都可以——即使已经不再更新系统。无需下载 App。",
      "faq.q2": "会改动我旧手机里的东西吗？",
      "faq.a2": "不会。照片、聊天记录和回忆都原样保留。SmartHub 只是让这台手机重新派上用场。",
      "faq.q3": "也能用游戏手柄吗？",
      "faq.a3": "可以！连上你的无线手柄，窝在沙发上就能玩——客厅里不再拖着一根线。",
      "faq.q4": "电脑上需要安装什么吗？",
      "faq.a4": "不需要。插上 SmartHub 就能用。",
      "faq.q5": "它会取代我的其他遥控器吗？",
      "faq.a5": "把它当作可靠的备用吧。平时照常用原来的遥控器——找不到或没电时，SmartHub 帮你顶上。",
      "foot.privacy": "隐私",
      "foot.terms": "条款",
      "foot.refund": "退换",
      "foot.copy": "© 2026 VisualBuild · visualbuild.shop"
    }
  };

  function applyLang(lang) {
    const pack = dict[lang] || dict.en;
    document.documentElement.lang = lang === "zh" ? "zh-Hans" : "en";
    document.querySelectorAll("[data-i18n]").forEach((el) => {
      const key = el.getAttribute("data-i18n");
      if (pack[key] != null) el.textContent = pack[key];
    });
    document.querySelectorAll("[data-i18n-html]").forEach((el) => {
      const key = el.getAttribute("data-i18n-html");
      if (pack[key] != null) el.innerHTML = pack[key];
    });
    try { localStorage.setItem("smarthub_lang", lang); } catch (_) {}
    const sel = document.getElementById("lang");
    if (sel) sel.value = lang;
  }

  const saved = (function () {
    try { return localStorage.getItem("smarthub_lang"); } catch (_) { return null; }
  })();
  const preferZh = typeof navigator !== "undefined" && /^zh\b/i.test(navigator.language || "");
  applyLang(saved || (preferZh ? "zh" : "en"));

  const sel = document.getElementById("lang");
  if (sel) sel.addEventListener("change", () => applyLang(sel.value));

  const c = window.SHOP_CONFIG || {};
  const p = document.querySelector("#price");
  const n = document.querySelector("#priceNote");
  const b = document.querySelector("#buyButton");
  if (p && c.price) p.textContent = c.price;
  if (n && c.priceNote) n.textContent = c.priceNote;
  if (b && c.creemCheckoutUrl) {
    b.href = c.creemCheckoutUrl;
    b.textContent = document.documentElement.lang.startsWith("zh") ? "立即购买" : "Buy now";
    b.classList.remove("off");
  } else if (b) {
    b.addEventListener("click", (e) => e.preventDefault());
    b.style.opacity = ".55";
    b.style.pointerEvents = "none";
  }
})();
