# TransferHub resume and buffering — 2026-10-27

Source locations:
- Pico: D:\Repository\connecthub_pico2w_native\pico2w_usb_transfer
- BL616: D:\Repository\blb616_connect\bl616_usb_transfer
- Shared web source: D:\Repository\asb_pico_product\transfer-src
- Generated website/offline package: D:\Repository\asb_pico_product\transfer

Implemented:
- Protocol 3. Existing bidirectional commands retained.
- Phone -> USB: retry idempotent chunks/end; retain the active upload for 10 minutes after wireless interruption. GET /api/resume?id= returns authenticated owner-only offset, sequence, prefix CRC, size and saved state. Sender checks original file name/size/lastModified and the complete acknowledged prefix CRC before continuing. Sender session token and task metadata use sessionStorage; file contents are not stored there.
- USB receiver recognizes exact duplicate chunks and completed-end retries; only one final disk commit. Bounded 256 KiB write buffer reduces filesystem calls.
- USB -> phone: retain the source and capability URL for 10 minutes after HTTP connection ends. Support single open-ended Range: bytes=N- requests, 206, Content-Range, ETag and Accept-Ranges. Malformed/out-of-bounds ranges return 416. Download manager resume depends on browser support; it is not automatic on every mobile browser. Keep the source page open. Click Cancel after completion to release the channel.
- Browser read-ahead cache: 256 KiB; table CRC32; progress rendering at most 10 Hz. Firmware reads headers in bounded blocks instead of byte-at-a-time socket calls. Board chunk sizes remain Pico 8192 / BL616 2048 forward and 2048 reverse.

Limits:
- This is recovery from Wi-Fi/HTTP interruption while USB and the computer page remain connected.
- Board reboot, USB disconnect, closing/reloading the computer page, timeout, or explicit cancel requires restarting. No durable power-loss checkpoint is claimed.
- A file is complete only after receiver close/commit ACK; reverse downloads must be checked in the browser download list.
- One transfer/direction at a time, configured max 4 GiB (not hardware-tested at this size).
- Firmware AND downloaded/offline receiver must be updated together. Default SSID: transferhub. Passwords unchanged.
- No firmware flashing, website publication or git push performed.

Validation:
- Production BL616 C with Linux socket/FreeRTOS shims passed ASan+UBSan: CRC/base64, auth/limits, resume owner isolation, duplicate upload chunk, changed duplicate rejection, idempotent end, reverse bytes, zero file, CRC failure, range at unaligned offset 3001, invalid ranges, expiry, cancel.
- Existing tools/test_web.py and tools/test_duplex_web.py passed in Edge headless.
- tools/test_resume_web.py: 700001 bytes, 86 USB chunks -> 3 disk writes; duplicate chunks/end do not duplicate output; simulated HTTP response lost after ACK resumed at offset4096 without a new start; wrong file rejected; reverse source sought to offset3001.
- Browser CRC microbenchmark (not device throughput): 1 MiB old bitwise 100.7ms vs lookup 4.7ms in one run. No real-world MB/s claim.
- Pico and BL616 builds succeeded; see evidence/resume-release.json after final build.

Hardware test:
1. Flash the correct board image; use the newly generated receiver/offline ZIP.
2. USB computer opens receiver and chooses destination. Phone joins transferhub.
3. Upload a several-MB file. Interrupt phone Wi-Fi for 10-20 seconds, reconnect. Automatic retry or select the identical file and click 继续传输. Compare SHA256 source/destination.
4. Send from USB computer to phone. Interrupt Wi-Fi; reconnect and use Resume in browser Downloads. Check final SHA256, then Cancel to release channel.
5. Measure identical files before/after under the same Wi-Fi/USB/storage conditions. No hardware throughput measurement has been made yet.
