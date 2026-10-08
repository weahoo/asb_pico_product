# Flexhub 

Product marketing site for **Flexhub** (asb_pico_ds5 SoftAP remote / Pico DualSense hub).

- Brand: Flexhub
- Manufacturer: visualbuild.me / visualbuild.local
- Domain target (later): visualbuild.shop
- Palette (max 4 site colors): white `#ffffff` · near-black `#1a1a1a` · product orange `#ff6a1a` (accent) · soft gray `#e8e8e8`. No red in site chrome.
- Product illustration: keep the original line drawing — white device body with red accents (matches the real hardware); do not recolor
- Languages: EN + 中文 (toggle in header)
- Audience: end customers (not developers). Tone: sunny, friendly, benefit-first, minimal tech talk
- Storefront copy rule: **no ASB Agent / MCP / AI / Skill / enterprise automation narrative** on customer pages. Product sells mouse · keyboard · drawing pad · USB/Bluetooth HID · optional spare remote. `asb.local` is only the SoftAP page address from firmware, not a product brand claim.
- Messaging pillars: (1) your phone, tablet or computer becomes a **mouse, keyboard and drawing pad**, (2) works with phones, tablets and computers (old or new), (3) no app for everyday use (app only for updates). Remote control is only a small bonus, never the headline.
- Two usage modes (confirmed against asb_pico_ds5 firmware `src/main.cpp` chooseLink/startSharedRadio and SoftAP UI strings): **USB** — Flexhub plugged into the target device with a USB data cable acts as a USB keyboard/mouse; **Bluetooth** — Flexhub on power only (charger/power bank) advertises as `flexhub` and is paired in the target device's Bluetooth settings. Mode is picked automatically at power-up; replug to switch. In both modes the controlling phone/tablet/computer joins Flexhub's Wi-Fi hotspot (`asb.local`) and uses the web page — no app.

## Stack

Static HTML / CSS / JS (no build step).

```
index.html      Landing page
styles.css      Theme
site.js         i18n + buy button wiring
config.js       price / Creem checkout URL (empty until launch)
privacy.html    Placeholder
terms.html      Placeholder
refund.html     Placeholder
assets/mark.svg                 Favicon / mark
assets/product-illustration.svg Hero product illustration (SVG, colored for white backgrounds)
```

## Preview locally

From this directory:

```bash
cd /Volumes/TSD302/Repository/asb_pico_product
python3 -m http.server 4173
```

Open http://127.0.0.1:4173/

Or open `index.html` directly in a browser (i18n and relative assets still work).

## Not done yet (by design)

- No Vercel / domain wiring yet
- No live Creem checkout — set `config.js` when ready

## Related

Firmware / SoftAP UI: `asb_pico_ds5`  
Older shop sketch (Render): `asb_pico_ds5/shop_site`


## SEO / GEO (on-page)

English-first storefront SEO for overseas discovery. Live preview: `https://asbpicoproduct.vercel.app` · canonical/shop: `https://visualbuild.shop/`.

Files added for crawlers / AI answer engines:

- `robots.txt`, `sitemap.xml`
- `llms.txt` — short entity facts for ChatGPT/Perplexity-style citation (no ASB/AI claims)
- JSON-LD `Organization` + `WebSite` + `Product` + `FAQPage` in `index.html`

Primary EN keywords: SoftAP Wi‑Fi remote, phone as mouse/keyboard/drawing pad, old phone remote, no app, Flexhub, BLE HID / flexhub.

**Do not auto-publish narrative changes to production without an explicit OK** if Vercel is wired to this repo.
