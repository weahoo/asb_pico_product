# FlexHub USB receiver

Open `index.html` in desktop Chrome / Edge, or deploy this directory at `/transfer/` over HTTPS. No backend, CDN scripts, analytics, or file uploads are used. File data flows through USB into the user-selected folder. Requires the dedicated pico2w_usb_transfer firmware, not the HID-only Flexhub firmware.

`FlexHub-Receiver.html` is the self-contained offline copy. The HTTPS page caches its shell using `sw.js`; browser cache eviction can remove offline availability. Increment the service-worker cache version when publishing an updated receiver.

Canonical UI source: `connecthub_pico2w_native/pico2w_usb_transfer/web/index.html`.
Firmware `tools/build.py` automatically exports here if this sibling repository exists. Override with `FLEXHUB_SITE_DIR`. To export without compiling, run:

```powershell
python ..\connecthub_pico2w_native\pico2w_usb_transfer\tools\web_assets.py --site-dir .
```

Pico captive portal: `/` offers send/receive; `/send` serves sender; `/receiver.html` downloads the offline receiver. LAN HTTP and captive mini-browsers cannot directly use Web Serial. USB CDC alone does not open a captive portal: the computer must join Pico Wi-Fi to fetch the offline page, or use this HTTPS receiver. No certificate bypass or insecure browser flags are required.
