import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

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

    def test_lataa_puuttuva_tiedosto(self):
        ei_ole = Path(self.tmp.name) / "ei_ole.json"

        self.s.lataa_viitteet(ei_ole)

        self.assertEqual(self.s.viitteet, [])

    def test_helpKomento(self):
        with patch("builtins.input", side_effect=["help", "exit"]), \
        patch("builtins.print") as mock_print:
            self.s.kysy_syotetta(self.tiedosto)

        mock_print.assert_any_call("Available commands: types / new / list")

    def test_new(self):
        with patch("builtins.input", side_effect=[
            "new",
            "article",
            "viite1",
            "Smith",
            "Foo",
            "J",
            "2020",
            "exit"
        ]):
            self.s.kysy_syotetta(self.tiedosto)

        data = json.loads(self.tiedosto.read_text(encoding="utf-8"))

        self.assertEqual(len(data), 1)
        self.assertEqual(data["viite1"]["type"], "article")
        self.assertEqual(data["viite1"]["author"], "Smith")
        self.assertEqual(data["viite1"]["title"], "Foo")
        self.assertEqual(data["viite1"]["journal"], "J")
        self.assertEqual(data["viite1"]["year"], "2020")

    def test_virheellinen_new(self):
        with patch("builtins.input", side_effect=[
            "new",
            "invalid",
            "exit"
        ]):
            with patch("builtins.print") as mock_print:
                self.s.kysy_syotetta(self.tiedosto)

        mock_print.assert_called_once_with(
            "Virhe: Tuntematon BibTeX tyyppi: invalid"
        )

        self.assertTrue(self.tiedosto.exists())

    def test_edit(self):
        self.tiedosto.write_text(json.dumps({
            "ABC123": {
                "type": "article",
                "author": "Taavetti",
                "title": "Artikkelin Artikkeli",
                "journal": "Maaginen lehdistö",
                "year": "1999"
            }
        }),encoding="utf-8")

        self.s.lataa_viitteet(self.tiedosto)

        with patch("builtins.input", side_effect=[
            "edit ABC123",
            "",
            "Pertti",
            "",
            "",
            "exit"
        ]):
            self.s.kysy_syotetta(self.tiedosto)

            data = json.loads(self.tiedosto.read_text(encoding="utf-8"))

            self.assertEqual(data["ABC123"]["type"], "article")
            self.assertEqual(data["ABC123"]["author"], "Pertti")
            self.assertEqual(data["ABC123"]["title"], "Artikkelin Artikkeli")
            self.assertEqual(data["ABC123"]["Journal"], "Maaginen lehdistö")
            self.assertEqual(data["ABC123"]["year"], "1999")


if __name__ == "__main__":
    unittest.main()