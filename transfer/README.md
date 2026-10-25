# Universal FlexHub Transfer receiver

The same website and self-contained offline HTML support both Pico Transfer Hub and BL616 Transfer Hub. Use dedicated transfer firmware, not HID-only or StackHub MCP gateway firmware. USB chooser includes Pico VID 2e8a and the current BL616 development CDC ffff:ffff. No manual board selection is required in the page.

Canonical source is ../transfer-src: index.html (role template), portal.html, offline-i18n.json, offline-README.txt, offline_assets.py and web_assets.py. Both firmware build generators read this shared source by default; FLEXHUB_TRANSFER_SOURCE can override the source folder. Project snapshots remain available for standalone builds.

Pico uses 8192-byte chunks and BL616 uses 2048-byte chunks; the sender uses the /api/start response and the receiver accepts either. Login, folder selection, CRC, per-write ACK and final-save ACK are identical.

index.html and FlexHub-Receiver.html are byte-identical to the HTML in FlexHub-Offline.zip and both projects. The site is HTTPS/static; offline HTML uses file:// in desktop Chrome/Edge/Chromium. Phone/tablet captive pages are senders or receiver-download portals, not USB Web Serial hosts.

Generate website without compiling:
python ..\connecthub_pico2w_native\pico2w_usb_transfer\tools\web_assets.py --site-dir .

Cache version: flexhub-transfer-v4-universal. Deploy this transfer folder to update the public website. Repository updates alone do not publish it. Existing compatible transfer firmware can use the new external receiver without reflashing; refreshing firmware-embedded downloads requires flashing the rebuilt transfer image.
