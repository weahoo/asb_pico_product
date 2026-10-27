# Transfer Hub — throughput and resume update (2026-10-27)

## Changes in this build
- Phone -> USB computer: negotiated chunk size increased to 16 KiB on Pico 2 W and 8 KiB on BL616. This reduces per-chunk HTTP/USB ACK cycles while retaining per-chunk CRC, duplicate-chunk idempotency, prefix CRC checks and final whole-file CRC/close acknowledgement.
- USB computer -> phone: reverse chunks increased from 2 KiB to 4 KiB. Firmware packet storage, USB command-line buffers, BL616 CDC RX ring and browser validation were updated together.
- C CRC32 changed from bit-at-a-time calculation to a 256-entry lookup table.
- The shared receiver HTML and offline ZIP were regenerated; Pico and BL616 receiver hashes match.

## Resume behavior and limits
- Phone -> computer: sender retries the current chunk; if retries are exhausted, the same file can resume from the authenticated device offset after its prefix CRC is checked. The device retains transfer state for up to 10 minutes. Keep the USB receiver page, device and USB connection alive; a power loss/reboot is not resumable.
- Computer -> phone: the source file remains available while the USB sender page stays open. The HTTP download endpoint supports Range: bytes=N-, 206, Content-Range and ETag; continuation depends on the mobile browser/download manager honoring Range. The source/capability is retained for up to 10 minutes after a download connection ends.
- Resume metadata is not a durable disk journal; closing the USB sender page, restarting firmware or losing the source File handle prevents continuation.

## Validation
- Pico firmware build: PASS. BL616 firmware build: PASS.
- Headless browser regressions: Pico web, duplex and resume tests PASS; BL616 web and duplex tests PASS.
- BL616 production C tests with AddressSanitizer and UndefinedBehaviorSanitizer: transfer/auth/CRC test PASS; reverse streaming/range-resume/CRC/cancel/expiry test PASS.
- Offline receiver HTML hashes match between Pico, BL616 and shared export.
- NOT yet verified on hardware: no real-device throughput benchmark after this optimization. The firmware artifacts below are built but this optimized build has not been flashed; website is not published. Do not infer a USB-direct-copy speed claim from software tests.
