"""Regression: StackHub Windows standalone EXE and localized install guidance."""
from pathlib import Path
import json
import re
import unittest

ROOT=Path(__file__).resolve().parents[1]
RELEASE=json.loads((ROOT/'stackhub-downloads.json').read_text(encoding='utf8'))
MARKETING=json.loads((ROOT/'stackhub-marketing.json').read_text(encoding='utf8'))
GUIDE=json.loads((ROOT/'hub-content.json').read_text(encoding='utf8'))
STACK=(ROOT/'stackhub.html').read_text(encoding='utf8')
SETUP=(ROOT/'stackhub-guide.html').read_text(encoding='utf8')
EXPECTED_URL='https://pub-31faf223c9e441d2941bfc7d9da9e2bd.r2.dev/visualbuild-firmware/StackHubBridge.exe'

class R2DownloadsTest(unittest.TestCase):
    def test_verified_windows_x64_standalone_release(self):
        self.assertEqual(RELEASE['product'],'StackHubBridge')
        self.assertEqual(RELEASE['release_channel'],'public-r2')
        self.assertEqual(RELEASE['r2_bucket'],'skill-builder-releases')
        self.assertEqual(RELEASE['r2_key'],'visualbuild-firmware/StackHubBridge.exe')
        self.assertEqual(set(RELEASE['downloads']),{'windows-x86_64'})
        win=RELEASE['downloads']['windows-x86_64']
        self.assertEqual(win['filename'],'StackHubBridge.exe')
        self.assertEqual(win['format'],'exe')
        self.assertEqual(win['url'],EXPECTED_URL)
        self.assertEqual(win['size_bytes'],50803494)
        self.assertEqual(win['sha256'],'b293c9c8f6e20fc4ffb4622c93e0e4d4434ab0f7d242ed620bdf9149c982bf97')
        self.assertNotIn('skill-builder-releases/',win['url'])
        self.assertNotIn('X-Amz-',win['url'])
        self.assertNotIn('offline_bl616_flash_tool_included',win)
        self.assertNotIn('exact_field_tested_rc4',win)

    def test_download_page_and_guide_share_one_windows_download_in_every_locale(self):
        for page in (STACK,SETUP):
            sections=re.findall(r'<section class="[^"]*(?:sh-downloads|sh-guide-downloads)[^"]*"[^>]*>.*?</section>',page,re.S)
            self.assertEqual(len(sections),7)
            for sec in sections:
                self.assertEqual(sec.count('href="'+EXPECTED_URL+'"'),1)
                self.assertNotIn('OfflineComplete-linux',sec)
                self.assertNotIn('OfflineComplete-windows',sec)
                self.assertNotIn('TAR.GZ',sec)
                self.assertNotIn('Offline ZIP',sec)
        self.assertEqual(STACK.count('<span class="eyebrow">WINDOWS</span>'),7)
        self.assertEqual(STACK.count('sh-download-guide-note'),7)

    def test_guidance_explains_exe_usb_memory_and_linux_pause(self):
        self.assertEqual(set(MARKETING),set(GUIDE))
        for lang,copy in MARKETING.items():
            self.assertTrue(copy['downloadTitle'])
            self.assertIn('Windows',copy['downloadWindows'])
            self.assertNotIn('downloadLinux',copy)
            note=copy['downloadGuideNote']
            for term in ('StackHubBridge.exe','USB','Memory MCP','Linux'):
                self.assertIn(term,note,(lang,term))
            self.assertIn('StackHubBridge.exe',GUIDE[lang]['ssteps'][3])
            self.assertIn('Memory MCP',GUIDE[lang]['ssteps'][3])
            self.assertIn('Bridge',GUIDE[lang]['ssteps'][3])
            self.assertIn(copy['downloadTitle'],STACK)
            self.assertIn(copy['downloadTitle'],SETUP)
        self.assertEqual(SETUP.count('StackHubBridge.exe'),21)

    def test_ai_fallback_is_preserved(self):
        self.assertEqual(set(MARKETING),set(GUIDE))
        for lang in MARKETING:
            self.assertEqual(MARKETING[lang]['aiTroubleshooting'],GUIDE[lang]['sAiTroubleshooting'])
        self.assertIn('优先切换到另一款支持 MCP 的 AI',STACK)
        self.assertIn('优先切换到另一款支持 MCP 的 AI',SETUP)
        self.assertIn('first try another MCP-compatible AI client',STACK)

if __name__=='__main__':unittest.main()
