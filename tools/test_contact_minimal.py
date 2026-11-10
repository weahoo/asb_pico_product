"""Regression checks for the privacy-first VisualBuild contact page."""
import re
import unittest
from pathlib import Path
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parent.parent
LANGS=("en","zh","de","fr","ja","ko","ar")

class ContactPageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html=(ROOT/"contact.html").read_text(encoding="utf8")
        cls.dom=BeautifulSoup(cls.html,"html.parser")

    def test_seven_languages_have_email(self):
        for lang in LANGS:
            with self.subTest(lang=lang):
                article=self.dom.select_one(f'article.contact-doc[data-l="{lang}"]')
                self.assertIsNotNone(article)
                self.assertEqual(len(article.select('a[href="mailto:info@visualbuild.me"]')),1)

    def test_no_missing_personal_details_or_placeholders(self):
        self.assertEqual(self.dom.select(".ph"),[])
        self.assertEqual(self.dom.select(".legal-toc"),[])
        for fragment in ("[Your full legal name]","[Postal address / country]",
                         "[Phone number]","[VAT ID, if applicable]","[Response time]"):
            self.assertNotIn(fragment,self.html)

    def test_brand_and_safe_product_subject(self):
        self.assertIn("VisualBuild",self.html)
        self.assertIn('product.toLowerCase()',self.html)
        self.assertIn('Object.prototype.hasOwnProperty.call',self.html)
        self.assertNotIn("Personal address:",self.html)

    def test_contact_only_has_an_email_action(self):
        for article in self.dom.select("article.contact-doc"):
            links=[a.get("href") for a in article.select("a[href]")]
            self.assertEqual(links,["mailto:info@visualbuild.me"])
            self.assertNotIn("bl616",article.get_text(" ",strip=True).lower())

if __name__=="__main__":
    unittest.main()
