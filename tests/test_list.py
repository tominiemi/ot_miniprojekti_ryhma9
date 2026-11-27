import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent / "src" / "ot_miniprojekti_ryhma9")
)

import json
import unittest
from unittest.mock import Mock, patch, mock_open
from ot_miniprojekti_ryhma9.reference import Reference
from ot_miniprojekti_ryhma9.list import List


def tee_viite(tyyppi, koodi="koodi", tags=None, **attributes):
    """Fake citation object, so the tests don't depend on Reference's validation."""
    viite = Mock()
    viite.entry_type = tyyppi
    viite.attributes = attributes
    viite.get_viitekoodi.return_value = koodi
    viite.get_tags.return_value = tags or []
    return viite


def tulosteet(mock_print):
    """All printed lines, with multiple print() arguments joined the way print joins them."""
    return [" ".join(str(arg) for arg in call.args) for call in mock_print.call_args_list]


class TestList(unittest.TestCase):

    def setUp(self):
        self.lista = List()


    def test_listaa(self):
        ref = Reference("article")
        ref.set_viitekoodi("hyva lahde")
        ref.set_attribute("title", "Testi artikkeli")
        ref.add_author("Meikalainen Matti")
        ref.set_attribute("year", "2002")

        with patch("builtins.print") as mock_print:
            self.lista.listaa([ref])

        printed = [str(call.args[0]) for call in mock_print.call_args_list]

        assert any("hyva lahde" in line for line in printed)
        assert any("Testi artikkeli" in line for line in printed)
        assert any("Meikalainen Matti" in line for line in printed)
        assert any("2002" in line for line in printed)

    def test_listaa_tyhjalla_listalla(self):
        with patch("builtins.print") as mock_print:
            self.lista.listaa([])

        mock_print.assert_not_called()

    def test_types(self):
        test_schema = {
            "bibtex": {
                "article": {},
                "book": {},
                "inproceedings": {}
            }
        }

        with patch(
            "builtins.open",
            mock_open(read_data=json.dumps(test_schema))
        ):
            with patch("builtins.print") as mock_print:
                self.lista.types()

        actual = [call.args[0] for call in mock_print.call_args_list]

        assert any("article" in line for line in actual)
        assert any("book" in line for line in actual)
        assert any("inproceedings" in line for line in actual)

    def test_muotoile_henkilot_tyhja(self):
        self.assertEqual(self.lista.muotoile_henkilot([]), "")
        self.assertEqual(self.lista.muotoile_henkilot(None), "")

    def test_muotoile_henkilot_jarjestaa_aakkosiin(self):
        tulos = self.lista.muotoile_henkilot(["virtanen Ville", "Aalto Aino"])
        self.assertEqual(tulos, "Aalto Aino, virtanen Ville")

    def test_article_kaikilla_kentilla(self):
        viite = tee_viite("article", author=["Meikalainen Matti"], year="2020",
                          title="Otsikko", journal="Lehti", volume="5",
                          number="2", pages="10-20")
        self.assertEqual(self.lista.muotoile_viite(viite),
                         "Meikalainen Matti (2020). Otsikko. Lehti, 5(2), 10-20.")

    def test_article_ilman_vapaaehtoisia_kenttia(self):
        viite = tee_viite("article", author=["Meikalainen Matti"], year="2020",
                          title="Otsikko", journal="Lehti")
        self.assertEqual(self.lista.muotoile_viite(viite),
                         "Meikalainen Matti (2020). Otsikko. Lehti.")

    def test_book_osoitteella(self):
        viite = tee_viite("book", author=["Kirjailija Kalle"], year="2019",
                          title="Kirja", publisher="Otava", address="Helsinki")
        self.assertEqual(self.lista.muotoile_viite(viite),
                         "Kirjailija Kalle (2019). Kirja. Otava, Helsinki.")

    def test_book_ilman_osoitetta(self):
        viite = tee_viite("book", author=["Kirjailija Kalle"], year="2019",
                          title="Kirja", publisher="Otava")
        self.assertEqual(self.lista.muotoile_viite(viite),
                         "Kirjailija Kalle (2019). Kirja. Otava.")

    def test_inproceedings_kaikilla_kentilla(self):
        viite = tee_viite("inproceedings", author=["Tutkija Tiina"], year="2021",
                          title="Paperi", booktitle="Konffa", pages="1-5",
                          publisher="ACM")
        self.assertEqual(self.lista.muotoile_viite(viite),
                         "Tutkija Tiina (2021). Paperi. In: Konffa, 1-5, ACM.")

    def test_conference_ilman_vapaaehtoisia_kenttia(self):
        viite = tee_viite("conference", author=["Tutkija Tiina"], year="2021",
                          title="Paperi", booktitle="Konffa")
        self.assertEqual(self.lista.muotoile_viite(viite),
                         "Tutkija Tiina (2021). Paperi. In: Konffa.")

    def test_muu_tyyppi(self):
        viite = tee_viite("misc", author=["Joku Jussi"], year="2022", title="Juttu")
        self.assertEqual(self.lista.muotoile_viite(viite),
                         "Joku Jussi (2022). Juttu.")

    def test_listaa_tagit_ei_tageja(self):
        viitteet = [tee_viite("misc", koodi="a"), tee_viite("misc", koodi="b")]

        with patch("builtins.print") as mock_print:
            self.lista.listaa_tagit(viitteet)

        mock_print.assert_called_once_with("No tags have been added to any citations.")

    def test_listaa_tagit_ryhmittelee_tagin_mukaan(self):
        v1 = tee_viite("misc", koodi="eka", tags=["ai", "ml"], title="Yksi", year="2020")
        v2 = tee_viite("misc", koodi="toka", tags=["ai"], title="Kaksi", year="2021")
        v3 = tee_viite("misc", koodi="kolmas", title="Kolme", year="2022")

        with patch("builtins.print") as mock_print:
            self.lista.listaa_tagit([v1, v2, v3])

        printed = tulosteet(mock_print)

        self.assertEqual(sum("tagged with" in rivi and "ai" in rivi for rivi in printed), 1)
        self.assertEqual(sum("tagged with" in rivi and "ml" in rivi for rivi in printed), 1)

        ai_kohta = next(i for i, r in enumerate(printed) if "tagged with" in r and "ai" in r)
        ml_kohta = next(i for i, r in enumerate(printed) if "tagged with" in r and "ml" in r)
        ai_osio = printed[ai_kohta:ml_kohta]
        ml_osio = printed[ml_kohta:]

        self.assertTrue(any(r.startswith("eka:") for r in ai_osio))
        self.assertTrue(any(r.startswith("toka:") for r in ai_osio))
        self.assertTrue(any(r.startswith("eka:") for r in ml_osio))
        self.assertFalse(any(r.startswith("toka:") for r in ml_osio))
        self.assertFalse(any(r.startswith("kolmas:") for r in printed))

    def test_listaa_yksi(self):
        viite = tee_viite("article", author=["virtanen Ville", "Aalto Aino"], title="Otsikko")

        with patch("builtins.print") as mock_print:
            self.lista.listaa_yksi(viite)

        self.assertEqual(tulosteet(mock_print), [
            "author: Aalto Aino, virtanen Ville",
            "title: Otsikko",
            "",
        ])


if __name__ == "__main__":
    unittest.main()