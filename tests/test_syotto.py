import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).parent.parent / "src" / "ot_miniprojekti_ryhma9"),
)

from syotto import Syote

class TestSyote(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.tiedosto = Path(self.tmp.name) / "testViitteet.json"
        self.s = Syote()

    def tearDown(self):
        self.tmp.cleanup()

    def test_lataa_viitteet(self):
        self.tiedosto.write_text(json.dumps({
            "viite1": {
                "type": "article",
                "author": "Smith",
                "title": "Foo",
                "journal": "J",
                "year": "2020",
            }
        }), encoding="utf-8")

        self.s.lataa_viitteet(self.tiedosto)

        self.assertEqual(len(self.s.viitteet), 1)
        viite = self.s.viitteet[0]
        self.assertEqual(viite.entry_type, "article")
        self.assertEqual(viite.attributes["author"], "Smith")
        self.assertEqual(viite.viitekoodi, "viite1")

if __name__ == "__main__":
    unittest.main()