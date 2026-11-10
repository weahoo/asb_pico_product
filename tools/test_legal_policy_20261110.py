"""Regressions for privacy-first, multi-product policy copy."""
import re
import unittest
from pathlib import Path
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parent.parent
PAGES=("privacy","terms","refund","shipping","contact")
LANGS=("en","zh","de","fr","ja","ko","ar")
UNFILLED=(
    "[Your full legal name]","[Postal address / country]","[Phone number]",
    "[Contact email]","[Privacy contact email]","[Shipping regions]",
    "[Shipping carriers]","[Response time]","[Delivery time estimates by region]",
    "[Governing law / jurisdiction]","[Warranty period]","[Currency]",
)

class VisualBuildLegalPolicies(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.docs = {}
        for page in PAGES:
            content=(ROOT/(page+".html")).read_text(encoding="utf8")
            cls.docs[page]=(content, BeautifulSoup(content,"html.parser"))

    def test_all_five_pages_seven_languages_no_empty_personal_fields(self):
        for name,(content,soup) in self.docs.items():
            with self.subTest(page=name):
                self.assertEqual(len(soup.select('article.legal-doc')),7)
                self.assertFalse(soup.select('.ph'))
                for bad in UNFILLED:
                    self.assertNotIn(bad,content)
                self.assertNotIn("Pico 2 W",content)
                self.assertNotIn("BL616",content)
                self.assertEqual(soup.select_one('.brand-text b').get_text(strip=True),"VisualBuild")
                for lang in LANGS:
                    article=soup.select_one(f'article[data-l="{lang}"]')
                    self.assertIsNotNone(article)
                    self.assertIn("info@visualbuild.me",article.get_text())
                    links=[a.get("href","") for a in article.select('a[href]')]
                    self.assertIn("mailto:info@visualbuild.me",links)

    def test_privacy_describes_cloud_and_local_devices(self):
        content,_=self.docs['privacy']
        for word in ("StackHub","FlexHub","TransferHub","Vercel","Google Fonts",
                     "gateway","BYOK","MCP","info@visualbuild.me"):
            self.assertIn(word,content)

    def test_consumer_rights_not_removed(self):
        for name in ("terms","refund"):
            content,_=self.docs[name]
            for word in ("30-day","14-day","FlexHub","statutory", "info@visualbuild.me"):
                self.assertIn(word,content,(name,word))
        content,_=self.docs["refund"]
        self.assertIn("return address",content)

    def test_shipping_is_hardware_only_and_no_unverified_times(self):
        content,_=self.docs['shipping']
        self.assertIn("Digital StackHub services",content)
        self.assertIn("if a delivery estimate",content.lower())
        self.assertNotIn("[Processing time]",content)

    def test_policy_navigation_and_dates(self):
        for name,(content,soup) in self.docs.items():
            links=[a.get("href") for a in soup.select("footer a")]
            for target in ("privacy.html","terms.html","refund.html","shipping.html","contact.html"):
                if target != name and not (name=="contact" and target=="contact.html"):
                    self.assertIn(target,links)
            if name!="contact":
                self.assertIn("2026-11-10",content)

if __name__ == "__main__":
    unittest.main()
