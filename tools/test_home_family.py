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
    def test_reuses_flexhub_svg_without_editing_source(self):
        self.assertTrue((ROOT/'assets/product-illustration.svg').is_file())
        self.assertEqual(HTML.count('src="assets/product-illustration.svg"'),7)
    def test_connected_branches_and_future_without_checkout(self):
        self.assertEqual(HTML.count('family-branch-stem'),7)
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
        self.assertEqual(m.images.count('assets/product-illustration.svg'),7)
    def test_three_accent_colors_and_responsive_connections(self):
        for selector in ['.family-node-stackhub','.family-node-flexhub',
                         '.family-node-transferhub','.family-node-future',
                         '.family-node-grid::before','.family-branch-stem']:
            self.assertIn(selector,CSS)
        self.assertIn('#6d43cc',CSS)
        self.assertIn('#ff6a1a',CSS)
        self.assertIn('#575b64',CSS)
        self.assertIn('@media(max-width:660px)',CSS)

if __name__=='__main__':unittest.main()
