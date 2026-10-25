# Bidirectional Transfer Hub — 2026-10-25

Protocol v2 supports both Wi-Fi phone → USB computer and USB computer → Wi-Fi phone. One file and one direction at a time. Pico and BL616 share the same website and offline HTML from D:/Repository/asb_pico_product/transfer-src.

## Use
1. Connect the board to the computer with a USB data cable. Open the website over HTTPS or extract the offline ZIP and open FlexHub-Receiver.html with desktop Chrome/Edge. Log in through the USB chooser.
2. Phone → computer: choose Receive on the USB page, grant a destination folder; log in on the phone hotspot page, choose Send and select a file.
3. Computer → phone: choose Send on USB, select and offer a file. On the phone hotspot page choose Receive and Download. Use a normal browser if the captive window cannot download. No computer destination folder is required to send.
4. For computer → phone the final message only confirms submission to the download connection. Confirm the saved file in the phone browser download list.

No internet is required with downloaded HTML. The computer does not need to join the hotspot. USB Web Serial requires an appropriate secure context; the board HTTP/captive page cannot directly access USB. Preserve the existing device credentials.

## Protocol and limits
Old one-way firmware remains usable for phone → computer; reverse transfer requires this firmware. AUTH advertises protocol 2. New commands: OFFER tag name64 size, RDATA id sequence chunk_crc cumulative_crc base64, RCANCEL. Responses: offer, reverse_pull, reverse_done. HTTP: /api/reverse, /api/reverse/claim, /api/download?ticket=..., /api/reverse/cancel. Download tickets are short-lived and single-use.

Reverse chunks are 2048 bytes on both boards, verified before socket writes; only a bounded chunk is buffered. A corrupt first chunk returns HTTP 502; a later failure truncates the declared-length download. Disconnects, timeout and cancellation release the channel. Configured file limit is 4 GiB, not hardware-tested at that size. No resume. Keep both browsers open and devices awake.

## Validation and release status
Both firmware builds and forward/reverse headless Edge browser tests passed. Production BL616 transfer C ran on a POSIX host with FreeRTOS shims and ASan/UBSan: binary content, zero size, mutual exclusion, one-use tickets, first/mid-stream CRC failures, cancellation and expiration passed. Browser download was tested via a local HTTP server with exact binary comparison and UTF-8 filename.

This is software validation, not board/Pixel hardware validation. Neither device was flashed and the public website was not deployed. See evidence/duplex-release.json for hashes and evidence. Existing gateway firmware on the attached Pico is untouched.

Run tools/test_web.py and tools/test_duplex_web.py after tools/build.py. The production-C host test lives in BL616 tests/test_reverse.c and uses tests/shim; run on Linux with gcc and pthreads. Pico uses the same reverse implementation; its platform integration is build-checked, not separately host-emulated.
