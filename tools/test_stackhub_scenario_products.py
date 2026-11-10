"""Three independent products and the transparent StackHub scenario visual."""
import json
import struct
import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT=Path(__file__).resolve().parents[1]
HOME=json.loads((ROOT/"home-family-content.json").read_text(encoding="utf8"))
STACK=json.loads((ROOT/"stackhub-marketing.json").read_text(encoding="utf8"))
INDEX=(ROOT/"index.html").read_text(encoding="utf8")
PAGE=(ROOT/"stackhub.html").read_text(encoding="utf8")
CSS=(ROOT/"hubs.css").read_text(encoding="utf8")
IMAGE="assets/stackhub-scenario-sketch-transparent.png"


class SiteIndependenceTest(unittest.TestCase):
    def test_three_distinct_hardware_products_in_all_languages(self):
        self.assertEqual(set(HOME),{"zh","en","ja","de","fr","ko","ar"})
        for language,copy in HOME.items():
            self.assertTrue(copy["headline"])
            self.assertTrue(copy["lead"])
            self.assertTrue(copy["coreTitle"])
            self.assertIn(copy["headline"],INDEX,language)
            self.assertIn(copy["coreTitle"],INDEX,language)
        # Buyer-facing messaging explains value without raising an imagined
        # "one device / three modes" comparison in any language.
        forbidden=[
            "并非同一设备", "三种模式", "三款独立产品", "独立硬件产品",
            "not three modes", "not interchangeable modes", "separate hardware products",
            "three independent products", "three distinct products",
            "1台の機器の3モード", "単一製品のモード切替",
            "keine drei modi", "nicht um austauschbare betriebsarten",
            "et non trois modes", "ce ne sont pas des modes interchangeables",
            "세 가지 모드가 아니라", "전환하는 모드가 아닙니다",
            "وليست ثلاثة أوضاع لجهاز واحد", "أوضاعاً قابلة للتبديل"
        ]
        fields=["headline","lead","coreEyebrow","coreTitle","coreDesc",
                "detailEyebrow","familyTag"]
        for language,copy in HOME.items():
            text=" ".join(copy[key] for key in fields).lower()
            for phrase in forbidden:
                self.assertNotIn(phrase.lower(),text,f"{language}: {phrase}")
                self.assertNotIn(phrase.lower(),INDEX.lower(),phrase)
        self.assertIn("StackHub",HOME["en"]["lead"])
        self.assertIn("FlexHub",HOME["en"]["lead"])
        self.assertIn("TransferHub",HOME["en"]["lead"])
        self.assertNotIn("一种设备形态",INDEX)
        self.assertNotIn("One familiar form",INDEX)
        self.assertNotIn("assets/product-illustration.svg",INDEX)
        self.assertNotIn("family-branch-stem",INDEX)
        for product in ["StackHub","FlexHub","TransferHub"]:
            self.assertGreaterEqual(INDEX.count(product),7)

    def test_transparent_illustration_is_an_rgba_png(self):
        raw=(ROOT/IMAGE).read_bytes()
        self.assertEqual(raw[:8],bytes([137,80,78,71,13,10,26,10]))
        self.assertEqual(raw[12:16],b"IHDR")
        width,height=struct.unpack(">II",raw[16:24])
        self.assertEqual((width,height),(1012,920))
        self.assertEqual(raw[25],6)  # PNG color type RGBA

    def test_stackhub_scene_is_visible_every_language(self):
        self.assertEqual(PAGE.count('src="'+IMAGE+'"'),7)
        self.assertEqual(PAGE.count('class="sh-illustration"'),7)
        self.assertIn(".sh-landing .sh-illustration-art img",CSS)
        for lang in HOME:
            self.assertTrue(STACK[lang]["sceneTitle"])
            self.assertTrue(STACK[lang]["sceneAlt"])
            self.assertTrue(STACK[lang]["sceneCaption"])
            self.assertIn(STACK[lang]["sceneTitle"],PAGE)
            self.assertIn(STACK[lang]["sceneCaption"].replace("&","&amp;"),PAGE)
        # Other product pages are not relabeled as different modes of StackHub.
        for product in ("flexhub","transferhub"):
            self.assertNotIn("stackhub-scenario-sketch-transparent.png",
                             (ROOT/(product+".html")).read_text(encoding="utf8"))


if __name__=="__main__":
    unittest.main()
