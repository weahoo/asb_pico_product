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
            self.assertIn(RELEASE['source_sha'],data['url'])
            self.assertTrue(data['url'].endswith(data['filename']))
            self.assertEqual(len(data['sha256']),64)
            self.assertGreater(data['size_bytes'],20_000_000)

    def test_downloads_available_in_both_pages_each_locale(self):
        for d in RELEASE['downloads'].values():
            self.assertEqual(STACK.count('href="'+d['url']+'"'),7)
            self.assertEqual(SETUP.count('href="'+d['url']+'"'),7)
        for lang in MARKETING:
            copy=MARKETING[lang]
            self.assertTrue(copy['downloadTitle'])
            self.assertTrue(copy['downloadWindows'])
            self.assertTrue(copy['downloadLinux'])
            self.assertTrue(copy['downloadCaution'])
            self.assertIn(copy['downloadTitle'],STACK)
            self.assertIn(copy['downloadTitle'],SETUP)

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
