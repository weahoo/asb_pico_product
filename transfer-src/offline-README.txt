FlexHub Offline / 离线文件传输

1. Extract the ZIP / 全部解压 ZIP。
2. Open offline-guide.html for instructions in seven languages / 打开 offline-guide.html 查看七语言指南。
3. Open FlexHub-Receiver.html in desktop Chrome / Edge / 用电脑 Chrome 或 Edge 打开接收网页。
4. Connect USB, log in, select a folder / 连接 USB、登录、授权接收文件夹。
5. Phone joins transferhub and opens http://192.168.77.1/ to send / 手机连热点后从上述地址发送。

Requires dedicated transfer firmware. No passwords are bundled.
需要专用传输固件；离线包不含设备密码。
No internet required after downloading. Keep pages open and devices awake.
下载后无需互联网；传输时保持页面打开、设备唤醒。

Bidirectional firmware: USB computer chooses Send; phone chooses Receive and downloads. Confirm saving in the browser download list.
双向固件：USB 电脑选发送，手机选接收并下载。请在浏览器下载列表确认保存。

Resume / 断点续传
Updated firmware + receiver page: phone uploads retry automatically; after Wi-Fi returns, select the same file and click 继续传输 (resume). Keep the USB receiver page open and connected; paused state expires after 10 minutes. For computer-to-phone downloads, use Resume in the browser download list if supported; keep the USB source page open. Click Cancel after finishing to release the channel. Reboot, USB unplugging, receiver-page closure, or expiry requires restarting. Duplicate filenames are renamed.
更新固件与接收网页后：手机上传会自动重试；网络恢复后选择原文件，点击“继续传输”。保持电脑接收网页打开、USB 连接，暂停状态最多保留 10 分钟。电脑发往手机时，可在支持续传的浏览器下载列表点击继续；保持电脑发送网页打开，完成后点击取消释放通道。设备重启、USB 拔出、电脑网页关闭或超时后需要重新发送。同名文件自动改名。
Browser-side bounded buffers: 256 KiB for file reading and receiving writes. Actual speed depends on Wi-Fi, USB and storage; no hardware speed claim.
浏览器使用 256 KiB 有界读取及写入缓冲；实际速度取决于无线、USB 和磁盘，尚未完成板端测速。
