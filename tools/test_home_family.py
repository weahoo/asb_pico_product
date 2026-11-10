"""Regression checks for the seven-language connected Hub family homepage."""
import json
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
COPY=json.loads((ROOT/'home-family-content.json').read_text(encoding='utf-8'))
HTML=(ROOT/'index.html').read_text(encoding='utf-8')
CSS=(ROOT/'hubs.css').read_text(encoding='utf-8')

class Markup(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids=[]
        self.links=[]
        self.images=[]
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if 'id' in d:self.ids.append(d['id'])
        if tag=='a':self.links.append(d.get('href',''))
        if tag=='img':self.images.append(d.get('src',''))

class FamilyHomeTest(unittest.TestCase):
    def test_seven_complete_locales(self):
        self.assertEqual(set(COPY),{'zh','en','ja','de','fr','ko','ar'})
        required=['headline','lead','coreTitle','coreDesc','futureName',
          'stackShort','flexShort','transferShort','stackPitch','flexPitch',
          'transferPitch','coming','explore','guide']
        for lang,item in COPY.items():
            for field in required:
                self.assertTrue(item.get(field),f'{lang}.{field}')
            for name in ['stackPoints','flexPoints','transferPoints']:
                self.assertEqual(len(item[name]),3,f'{lang}.{name}')
    def test_product_order_every_locale(self):
        for lang in COPY:
            ids=[f'family-{product}-{lang}' for product in ['stackhub','flexhub','transferhub']]
            positions=[HTML.index('id="'+name+'"') for name in ids]
            self.assertEqual(positions,sorted(positions),lang)
            self.assertIn('data-lang="'+lang+'"',HTML)
    def test_independent_product_badges_replace_single_shared_device_picture(self):
        # Keep the original SVG available, but do not imply a single device
        # branches into three hardware products.
        self.assertTrue((ROOT/'assets/product-illustration.svg').is_file())
        self.assertNotIn('src="assets/product-illustration.svg"',HTML)
        for suffix in ('stack','flex','transfer'):
            self.assertEqual(HTML.count('family-product-badge-'+suffix),7)
        self.assertNotIn('family-branch-stem',HTML)
    def test_connected_branches_and_future_without_checkout(self):
        self.assertEqual(HTML.count('family-branch-stem'),0)
        self.assertEqual(HTML.count('family-node-future'),7)
        self.assertEqual(HTML.count('family-node-stackhub'),7)
        self.assertEqual(HTML.count('family-node-flexhub'),7)
        self.assertEqual(HTML.count('family-node-transferhub'),7)
        self.assertNotIn('href="futurehub.html"',HTML)
    def test_no_duplicate_ids_and_product_navigation(self):
        m=Markup();m.feed(HTML)
        self.assertEqual(len(m.ids),len(set(m.ids)))
        for page in ['stackhub.html','flexhub.html','transferhub.html']:
            self.assertIn(page,m.links)
            self.assertTrue((ROOT/page).exists())
        self.assertEqual(m.images.count('assets/product-illustration.svg'),0)
    def test_public_pages_are_customer_facing(self):
        public_files=['index.html','stackhub.html','transferhub.html',
                      'stackhub-guide.html','transferhub-guide.html','flexhub.html']
        internal_phrases=[
            '不能宣称','绝对隔离','零泄露','空气隔离','物理零连接',
            '安全审查','Creem','测试环境','测试结账','测试价','测试模式',
            'not a zero-exchange air gap','security review','test checkout',
            'Test mode:','tools/install_host.py','YOUR_URL_ENCODED_KEY',
            'one board does not run all three',
            'not three modes', 'not interchangeable modes',
            '并非同一设备的三种模式', '三款独立硬件产品',
        ]
        for name in public_files:
            markup=(ROOT/name).read_text(encoding='utf-8')
            for phrase in internal_phrases:
                self.assertNotIn(phrase.lower(),markup.lower(),f'{name}: {phrase}')

    def test_guides_offer_steps_and_email_mcp_choice(self):
        import re
        a=(ROOT/'stackhub-guide.html').read_text(encoding='utf-8')
        b=(ROOT/'transferhub-guide.html').read_text(encoding='utf-8')
        for language in COPY:
            for data in [a,b]:
                match=re.search(r'<article class="lang-block[^"]*" data-lang="'+language+r'">(.*?)</article>',data,re.S)
                self.assertIsNotNone(match,language)
                self.assertGreaterEqual(match.group(1).count('<li>'),5,language)
        self.assertIn('Authorization: Bearer',a)
        self.assertIn('完整 MCP URL',a)
        self.assertIn('http://192.168.77.1/',b)
        self.assertIn('http://192.168.78.1/',a)
        self.assertNotIn('python tools/install_host.py',a)

    def test_pricing_status_has_no_internal_payment_mode_text(self):
        javascript=(ROOT/'stackhub-pricing.js').read_text(encoding='utf-8')
        self.assertNotIn("billing_mode",javascript)
        self.assertNotIn("测试环境",javascript)
        self.assertNotIn("Test mode",javascript)

    def test_three_accent_colors_and_responsive_connections(self):
        for selector in ['.family-node-stackhub','.family-node-flexhub',
                         '.family-node-transferhub','.family-node-future',
                         '.family-product-badge-stack','.family-product-badges']:
            self.assertIn(selector,CSS)
        self.assertIn('#6d43cc',CSS)
        self.assertIn('#ff6a1a',CSS)
        self.assertIn('#575b64',CSS)
        self.assertIn('@media(max-width:660px)',CSS)

if __name__=='__main__':unittest.main()
