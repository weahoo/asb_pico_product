# SmartHub by visualbuild.local

Product marketing site for **SmartHub** (asb_pico_ds5 SoftAP remote / Pico DualSense hub).

- Brand: SmartHub by visualbuild.local
- Manufacturer: visualbuild.me / visualbuild.local
- Domain target (later): visualbuild.shop
- Palette: orange · dark · white
- Languages: EN + 中文 (toggle in header)

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
assets/mark.svg Favicon / mark
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

- No GitHub push
- No Vercel / domain wiring
- No live Creem checkout — set `config.js` when ready

## Related

Firmware / SoftAP UI: `asb_pico_ds5`  
Older shop sketch (Render): `asb_pico_ds5/shop_site`
