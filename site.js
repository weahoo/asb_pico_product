/* SmartHub site — i18n + checkout config */
(function () {
  const dict = {
    en: {
      skip: "Skip to content",
      "nav.how": "How it works",
      "nav.features": "Features",
      "nav.specs": "Specs",
      "nav.buy": "Buy",
      "nav.faq": "FAQ",
      "nav.cta": "Get SmartHub",
      "lang.label": "Language",
      "hero.eyebrow": "SoftAP · DualSense · for real people",
      "hero.title": "When a phone alone is not enough.<br><span class=\"accent\">A careful remote for the machine.</span>",
      "hero.lead": "SmartHub by visualbuild.local is a Pico SoftAP remote and DualSense hub — complementary to your phone, not competing with it. Made for accessibility, demos, and coarse remote control over USB HID when the target cannot (or must not) install another agent.",
      "hero.ctaPrimary": "Get SmartHub",
      "hero.ctaSecondary": "See how it helps",
      "hero.m1l": "SoftAP",
      "hero.m2l": "USB HID",
      "hero.m3l": "Together with phone",
      "hero.illustCaption": "SmartHub SoftAP remote and DualSense hub illustration",
      "chip.access": "Accessibility",
      "chip.demo": "Demos",
      "chip.remote": "Coarse remote",
      "flow.phone": "Phone / Pad",
      "flow.phoneSub": "Web remote",
      "flow.hubSub": "Pico SoftAP",
      "flow.target": "Target",
      "flow.targetSub": "USB HID",
      "how.kicker": "How it works",
      "how.title": "One small bridge. Three honest steps.",
      "how.lead": "SmartHub sits quietly between your phone or controller and the USB target — a thin physical layer you can trust, not another cloud agent asking for more.",
      "how.s1t": "Plug in",
      "how.s1p": "Connect SmartHub to the target over USB. It enumerates as keyboard, mouse and joystick HID (manufacturer visualbuild.me).",
      "how.s2t": "Join SoftAP",
      "how.s2p": "Connect to the visualbuild.local hotspot (initial password build.me) and open the hosted web UI on your phone or tablet.",
      "how.s3t": "Control",
      "how.s3p": "Drive touch, mouse, keyboard, DualSense, remotes and recordings — gently, without installing software on the target.",
      "feat.kicker": "Product highlights",
      "feat.title": "Stable SoftAP first. Everything else after.",
      "feat.lead": "We care first that the hotspot stays usable under real phone and controller load — then layer remotes, DualSense, and recording for accessibility, demos, and everyday coarse control.",
      "feat.f1t": "SoftAP web remote",
      "feat.f1p": "Pico-hosted HTTP / WebSocket UI. Join the hotspot, authenticate once, and keep control local — no cloud round-trip for input.",
      "feat.f2t": "DualSense — as an input, not a game console",
      "feat.f2p": "Pair DualSense and supported pads when a stick or button is kinder than a tiny touchscreen. Bridge them to USB HID — for accessibility and demos, not gaming-first.",
      "feat.f3t": "USB HID bridge",
      "feat.f3p": "Keyboard, mouse and joystick for machines that cannot (or must not) install a control agent — legacy PCs, kiosks, locked images, shared demo floors.",
      "feat.f4t": "Recording & BOOTSEL",
      "feat.f4p": "Capture actions in the browser, export/import libraries, store a script on the Pico, and trigger playback from configurable BOOTSEL actions.",
      "feat.f5t": "Remotes & Pencil",
      "feat.f5p": "Apple TV / Google-style remotes, touch gestures, and iPad + Apple Pencil input paths designed for real tablet use.",
      "feat.f6t": "Access password",
      "feat.f6p": "One device access password for SoftAP and home-network HTTP / WebSocket. Change it in Settings; factory reset restores the initial password.",
      "why.kicker": "Why SmartHub",
      "why.title": "When software cannot cross the boundary, a human action still can.",
      "why.lead": "Use it beside ASB when you need a physical layer — or on its own, as a warm SoftAP companion for devices you already care about.",
      "why.s1t": "Machines that still matter",
      "why.s1p": "Keep useful hardware in service instead of throwing it away. Basic HID control needs no install on the target.",
      "why.s2t": "Phone stays primary — SmartHub fills the gaps",
      "why.s2p": "Your phone remains the familiar surface. SmartHub adds the coarse remote path — keyboard, mouse, DualSense, remotes — over a local SoftAP UI.",
      "why.s3t": "Thin by design",
      "why.s3p": "SmartHub is an execution bridge. AI planning and skill packaging stay upstream in ASB / visualbuild.me when you need them.",
      "why.s4t": "Local-first radio",
      "why.s4p": "SoftAP stability comes first. BLE command reception stays opt-in and off by default.",
      "specs.kicker": "At a glance",
      "specs.title": "Hardware identity & defaults",
      "specs.lead": "Aligned with the asb_pico_ds5 SoftAP / DualSense firmware baseline. Final retail packaging may differ.",
      "specs.a1l": "Local name",
      "specs.a2l": "Initial access",
      "specs.a3l": "USB HID",
      "specs.a4l": "Board class",
      "specs.a5l": "Outputs",
      "specs.a5v": "Keyboard · Mouse · Joystick",
      "specs.a6l": "Control",
      "specs.a6v": "HTTP + WebSocket UI",
      "specs.a7l": "Controllers",
      "specs.a7v": "DualSense & supported pads",
      "specs.a8l": "Companion",
      "specs.a8v": "Android + ASB Burn",
      "buy.kicker": "visualbuild.shop",
      "buy.title": "SmartHub — ready when you are ready.",
      "buy.lead": "Checkout, shipping, and warranty will be confirmed before orders open. This page is honest about that — no live payment yet, just the product we are building with care.",
      "buy.priceNote": "Price to be announced",
      "buy.cta": "Coming soon",
      "buy.fine": "Secure checkout will open on visualbuild.shop",
      "faq.kicker": "FAQ",
      "faq.title": "Things worth knowing first",
      "faq.q1": "Does the target need ASB or SmartHub software installed?",
      "faq.a1": "No for basic USB HID bridge use. The target only needs to accept a standard keyboard / mouse / joystick. ASB on visualbuild.me is the optional upstream automation plane.",
      "faq.q2": "Is SmartHub the same as Automation Skill Builder?",
      "faq.a2": "No. SmartHub is the Pico SoftAP / DualSense hardware bridge (visualbuild.local) — complementary to your phone for accessibility, demos, and coarse remote. Automation Skill Builder is the desktop/local AI automation product on visualbuild.me. They can work together; they are not the same product.",
      "faq.q3": "How do I connect the first time?",
      "faq.a3": "Plug SmartHub into USB, join the visualbuild.local SoftAP (initial password build.me), open the hosted page, and sign in with the same access password. You can change the password later in Settings.",
      "faq.q4": "Can firmware be updated from Android?",
      "faq.a4": "Yes — ASB Burn is the standalone Android / desktop companion for firmware install and recovery.",
      "faq.q5": "Does BLE stay on all the time?",
      "faq.a5": "BLE command reception is opt-in and default-off. SoftAP stability takes priority over always-on radio features.",
      "foot.privacy": "Privacy",
      "foot.terms": "Terms",
      "foot.refund": "Refunds",
      "foot.copy": "© 2026 VisualBuild. Domain target: visualbuild.shop"
    },
    zh: {
      skip: "跳到正文",
      "nav.how": "原理",
      "nav.features": "功能",
      "nav.specs": "规格",
      "nav.buy": "购买",
      "nav.faq": "问答",
      "nav.cta": "获取 SmartHub",
      "lang.label": "语言",
      "hero.eyebrow": "SoftAP · DualSense · 认真对真人",
      "hero.title": "当手机一个人不够时。<br><span class=\"accent\">给目标机一份认真的遥控。</span>",
      "hero.lead": "SmartHub 是 visualbuild.local 的 Pico SoftAP 遥控与 DualSense 中枢——它不抢手机的主控位，而是补上手机够不到的粗粒度远程：无障碍辅助、演示讲解、受限环境里的键盘鼠标手柄。连上热点，打开网页，动作就从 USB HID 走到目标机。",
      "hero.ctaPrimary": "获取 SmartHub",
      "hero.ctaSecondary": "看看它如何帮到你",
      "hero.m1l": "SoftAP",
      "hero.m2l": "USB HID",
      "hero.m3l": "与手机互补",
      "hero.illustCaption": "SmartHub SoftAP 遥控与 DualSense 中枢示意图",
      "chip.access": "无障碍",
      "chip.demo": "演示",
      "chip.remote": "粗粒度远程",
      "flow.phone": "手机 / 平板",
      "flow.phoneSub": "网页遥控",
      "flow.hubSub": "Pico SoftAP",
      "flow.target": "目标机",
      "flow.targetSub": "USB HID",
      "how.kicker": "工作方式",
      "how.title": "一座小桥，三步说清楚。",
      "how.lead": "SmartHub 安静地待在手机/手柄与 USB 目标之间——薄薄一层你可以信任的物理执行，而不是又一个索要权限的云端代理。",
      "how.s1t": "插入",
      "how.s1p": "用 USB 把 SmartHub 接到目标机。它会枚举为键盘、鼠标与摇杆 HID（厂商 visualbuild.me）。",
      "how.s2t": "加入 SoftAP",
      "how.s2p": "连接 visualbuild.local 热点（初始密码 build.me），在手机或平板打开设备托管的网页界面。",
      "how.s3t": "控制",
      "how.s3p": "触控、鼠标、键盘、DualSense、遥控与录制——温和地完成，目标机无需安装任何软件。",
      "feat.kicker": "产品亮点",
      "feat.title": "先把 SoftAP 做稳，其余再慢慢加上。",
      "feat.lead": "我们先关心真实手机与手柄负载下热点是否仍可用，再为无障碍、演示与日常粗粒度控制叠上遥控、DualSense 与录制。",
      "feat.f1t": "SoftAP 网页遥控",
      "feat.f1p": "Pico 托管的 HTTP / WebSocket 界面。加入热点、一次鉴权，输入保持本地，不经云端往返。",
      "feat.f2t": "DualSense——当作输入，而不是游戏主机",
      "feat.f2p": "当摇杆或实体键比小屏幕触控更体贴时，配对 DualSense 与受支持手柄，桥接到 USB HID——面向无障碍与演示，而不是以游戏为先。",
      "feat.f3t": "USB HID 桥",
      "feat.f3p": "为无法或不允许安装控制代理的机器提供键盘、鼠标与摇杆——老旧 PC、展厅机、锁定镜像、共享演示环境。",
      "feat.f4t": "录制与 BOOTSEL",
      "feat.f4p": "在浏览器中录制动作、导入导出库、在 Pico 上保存脚本，并通过可配置的 BOOTSEL 动作触发回放。",
      "feat.f5t": "遥控与 Pencil",
      "feat.f5p": "Apple TV / Google 风格遥控、触控手势，以及面向真实平板使用的 iPad + Apple Pencil 路径。",
      "feat.f6t": "访问密码",
      "feat.f6p": "SoftAP 与家庭网络 HTTP / WebSocket 共用同一设备访问密码。可在设置中修改；恢复出厂重置回初始密码。",
      "why.kicker": "为什么是 SmartHub",
      "why.title": "当软件跨不过边界，人的动作仍然可以。",
      "why.lead": "需要时与 ASB 搭配作为物理层；也可以独自作为 SoftAP 伴侣，温柔地服务你已经在意的设备。",
      "why.s1t": "仍然值得留下的机器",
      "why.s1p": "让仍有用的硬件继续服务，而不是整机丢掉。基础 HID 控制无需在目标侧安装软件。",
      "why.s2t": "手机仍是主角——SmartHub 补缺口",
      "why.s2p": "手机仍是你熟悉的输入面。SmartHub 补上粗粒度远程：键盘、鼠标、DualSense、遥控——都走本地 SoftAP 界面。",
      "why.s3t": "刻意做薄",
      "why.s3p": "SmartHub 是执行桥。需要 AI 规划与技能打包时，留在上游 ASB / visualbuild.me。",
      "why.s4t": "本地优先射频",
      "why.s4p": "SoftAP 稳定优先。BLE 指令接收保持可选，默认关闭。",
      "specs.kicker": "一览",
      "specs.title": "硬件标识与默认值",
      "specs.lead": "对齐 asb_pico_ds5 SoftAP / DualSense 固件基线。最终零售包装可能不同。",
      "specs.a1l": "本地名",
      "specs.a2l": "初始访问",
      "specs.a3l": "USB HID",
      "specs.a4l": "板型",
      "specs.a5l": "输出",
      "specs.a5v": "键盘 · 鼠标 · 摇杆",
      "specs.a6l": "控制",
      "specs.a6v": "HTTP + WebSocket 界面",
      "specs.a7l": "手柄",
      "specs.a7v": "DualSense 与受支持手柄",
      "specs.a8l": "配套",
      "specs.a8v": "Android + ASB Burn",
      "buy.kicker": "visualbuild.shop",
      "buy.title": "SmartHub — 等你准备好，我们再开售。",
      "buy.lead": "结账、发货与保修会在正式接单前确认。本页把这件事说清楚——暂无真实支付，只有我们认真在做的产品。",
      "buy.priceNote": "价格待公布",
      "buy.cta": "即将开售",
      "buy.fine": "安全结账将在 visualbuild.shop 开放",
      "faq.kicker": "常见问题",
      "faq.title": "先知道这些就好",
      "faq.q1": "目标机需要安装 ASB 或 SmartHub 软件吗？",
      "faq.a1": "基础 USB HID 桥接不需要。目标机只需接受标准键盘/鼠标/摇杆。visualbuild.me 上的 ASB 是可选的上游自动化层。",
      "faq.q2": "SmartHub 和 Automation Skill Builder 是同一个产品吗？",
      "faq.a2": "不是。SmartHub 是 Pico SoftAP / DualSense 硬件桥（visualbuild.local）——与手机互补，用于无障碍、演示与粗粒度远程。Automation Skill Builder 是 visualbuild.me 上的桌面/本地 AI 自动化产品。可以配合使用，但不是同一产品。",
      "faq.q3": "第一次怎么连接？",
      "faq.a3": "插入 USB，加入 visualbuild.local SoftAP（初始密码 build.me），打开托管页面，用同一访问密码登录。之后可在设置中修改密码。",
      "faq.q4": "可以用 Android 更新固件吗？",
      "faq.a4": "可以——ASB Burn 是独立的 Android / 桌面固件安装与恢复配套。",
      "faq.q5": "BLE 会一直开启吗？",
      "faq.a5": "BLE 指令接收为可选且默认关闭。SoftAP 稳定优先于常开射频功能。",
      "foot.privacy": "隐私",
      "foot.terms": "条款",
      "foot.refund": "退换",
      "foot.copy": "© 2026 VisualBuild。域名目标：visualbuild.shop"
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
