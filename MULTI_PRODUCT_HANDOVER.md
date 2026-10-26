# Three-product site — 2026-10-26

## Pages
- index.html: VisualBuild three-product entry.
- flexhub.html: preserved original FlexHub product/checkout page. guide.html remains its guide and existing anchor URLs remain valid.
- transferhub.html / transferhub-guide.html: bidirectional transfer, browser requirements, existing online app and offline ZIP links.
- stackhub.html / stackhub-guide.html: hotspot configuration, WSS versus backend MCP, USB browser bridge, URL/JSON setup and limitations.

## Editing
Edit hub-content.json for seven-language content, hubs.css/hubs.js for presentation. Run python tools/build_hubs.py to regenerate the five new pages. FlexHub page and guide are maintained separately; do not replace flexhub.html with the generated catalog.

## Commerce
Existing FlexHub checkout configuration is unchanged. TransferHub and StackHub use contact enquiries and explicitly state that price/checkout is not configured. Add real product-specific prices and checkout URLs before enabling purchases; do not reuse the FlexHub checkout. Nothing has been pushed or published by this task.

## Validation
Headless Edge: five pages x seven languages, visible headings, 393px horizontal overflow and local CTA targets passed; JavaScript errors zero. Desktop/mobile screenshots and validation JSON are under tools/.
The transfer app, offline ZIP and firmware were not changed by this website task.
StackHub documentation is based on the available README and known workflows. Internal HANDOVER access was blocked by automatic approval review, so newer firmware-specific category/message-limit claims were deliberately not asserted.
Do not claim hardware acceptance or guaranteed transfer speed based on software tests.

## Pending hardware task
BL616 u4 is flashed. Pixel 7 keyboard page showed side-by-side control/keyboard layout. u5 fixes the layout, preserves BLE typing, is built/validated, and was flashed successfully on 2026-10-26. Normal boot and Pixel layout verification pending.
Firmware: D:/Repository/asb_pico_ds5/bl616/e2e/evidence/unicode-u5/flexhub_bl616-0.7.180-u5.bin
SHA256: 46e7f0c483f0d58d800c8fc33f72a7895ae66329cf2054dd7ba2cd49a345b472
