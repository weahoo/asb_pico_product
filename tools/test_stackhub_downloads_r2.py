"""RC4 public R2 download URLs and alternate-AI troubleshooting copy."""
from pathlib import Path
import json
import unittest


ROOT=Path(__file__).resolve().parents[1]
RELEASE=json.loads((ROOT/'stackhub-downloads.json').read_text(encoding='utf8'))
MARKETING=json.loads((ROOT/'stackhub-marketing.json').read_text(encoding='utf8'))
GUIDE=json.loads((ROOT/'hub-content.json').read_text(encoding='utf8'))
STACK=(ROOT/'stackhub.html').read_text(encoding='utf8')
SETUP=(ROOT/'stackhub-guide.html').read_text(encoding='utf8')


class R2DownloadsTest(unittest.TestCase):
    def test_expected_verified_sources(self):
        self.assertEqual(RELEASE['source_sha'],'79a0b56f675c02708cdcd2ceae4591ac944bdb19')
        self.assertEqual(RELEASE['release_channel'],'developer-candidate')
        self.assertFalse(RELEASE['signed'])
        self.assertEqual(set(RELEASE['downloads']),{'windows-x86_64','linux-x86_64'})
        for platform,data in RELEASE['downloads'].items():
            self.assertTrue(data['url'].startswith('https://pub-31faf223c9e441d2941bfc7d9da9e2bd.r2.dev/'))
            self.assertNotIn('X-Amz-',data['url'])
            self.assertIn(platform,data['url'])
            self.assertIn(data['run_id'],data['url'])
            self.assertIn(data.get('source_sha', RELEASE['source_sha']), data['url'])
            self.assertTrue(data['url'].endswith(data['filename']))
            self.assertEqual(len(data['sha256']),64)
            self.assertGreater(data['size_bytes'],20_000_000)

    def test_windows_is_identical_to_field_tested_rc4(self):
        win=RELEASE['downloads']['windows-x86_64']
        self.assertEqual(win['source_sha'],'594198d28430ca38fd699b074a32451d16b0959d')
        self.assertEqual(win['run_id'],'42659988215')
        self.assertEqual(win['size_bytes'],103477152)
        self.assertEqual(win['sha256'],'97e8681767c2a780e2353d825fb5e5ec3cee0c55db87ce71db3d67dbd4e7d86b')
        self.assertEqual(win['tested_exe_sha256'],'86112ee20bf97e821daef75daa4304ac1648745e31941b8eec2456a9f93162a9')
        self.assertTrue(win['offline_bl616_flash_tool_included'])
        self.assertTrue(win['exact_field_tested_rc4'])
        self.assertNotIn('downloadDesc',MARKETING['zh'])
        self.assertNotIn('downloadCaution',MARKETING['en'])

    def test_downloads_available_in_both_pages_each_locale(self):
        for d in RELEASE['downloads'].values():
            self.assertEqual(STACK.count('href="'+d['url']+'"'),7)
            self.assertEqual(SETUP.count('href="'+d['url']+'"'),7)
        for lang in MARKETING:
            copy=MARKETING[lang]
            self.assertTrue(copy['downloadTitle'])
            self.assertTrue(copy['downloadWindows'])
            self.assertTrue(copy['downloadLinux'])
            self.assertNotIn('downloadDesc',copy)
            self.assertNotIn('downloadCaution',copy)
            self.assertIn(copy['downloadTitle'],STACK)
            self.assertIn(copy['downloadTitle'],SETUP)

    def test_download_copy_is_compact(self):
        self.assertEqual(MARKETING['zh']['downloadTitle'],'下载 Stackhub 桌面支持应用')
        self.assertNotIn('WINDOWS / LINUX / R2',STACK)
        self.assertEqual(STACK.count('WINDOWS / LINUX</span>'),7)
        for page in (STACK,SETUP):
            self.assertNotIn('Windows 与 Linux x86_64 离线完整包',page)
            self.assertNotIn('未签名测试版。Windows 包内含',page)
            self.assertNotIn('sh-download-caution',page)

    def test_ai_fallback_note_every_locale(self):
        self.assertEqual(set(MARKETING),set(GUIDE))
        for lang in MARKETING:
            self.assertTrue(MARKETING[lang]['aiTroubleshooting'])
            self.assertEqual(MARKETING[lang]['aiTroubleshooting'],GUIDE[lang]['sAiTroubleshooting'])
        self.assertIn('优先切换到另一款支持 MCP 的 AI',STACK)
        self.assertIn('优先切换到另一款支持 MCP 的 AI',SETUP)
        self.assertIn('first try another MCP-compatible AI client',STACK)


if __name__=='__main__':
    unittest.main()
