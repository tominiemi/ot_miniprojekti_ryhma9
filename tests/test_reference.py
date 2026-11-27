import sys
import json
from pathlib import Path
from unittest.mock import mock_open, patch
import unittest

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent / "src" / "ot_miniprojekti_ryhma9")
)

import pytest
from ot_miniprojekti_ryhma9.reference import Reference



class TestReference(unittest.TestCase):


    def setUp(self):
        self.testOlio = Reference("book")

    def test_set_attribute(self):
        self.testOlio.set_attribute("author", "Pekka")

        self.assertEqual(
            self.testOlio.get_attributes()["author"],
            "Pekka"
        )

    def test_get_attributes(self):
        self.testOlio.set_attribute("author","Pekka")
        self.testOlio.set_attribute("title","Pekan stoori")
        self.assertEqual(self.testOlio.get_attributes(),{"author":"Pekka","editor":None,"title":"Pekan stoori","publisher":None,"year":None})


    def test_set_viitekoodi(self, viitekoodi = "Moikka211"):
        self.testOlio.set_viitekoodi(viitekoodi)
        self.assertEqual(self.testOlio.get_viitekoodi(),viitekoodi)

    def test_get_viitekoodi(self):
        self.testOlio.set_viitekoodi("Heippa123")
        self.assertEqual(self.testOlio.get_viitekoodi(),"Heippa123")

    def test_get_definition_ei_oo(self):
        with self.assertRaises(ValueError):
            self.testOlio2 = Reference("sarjakuva")  


    def test_alias(self):
        self.testOlio3 = Reference("inproceedings")
        self.testOlio4 = Reference("conference")

        self.assertEqual(self.testOlio3.get_attributes(), self.testOlio4.get_attributes())


    def test_set_attribute_vaara(self):
            with self.assertRaises(ValueError):
                self.testOlio.set_attribute("ouwhdi", "awhdidh")

    def test_add_author_nostaa_virheen(self):
            self.testOlio5 = Reference("misc")
            with self.assertRaises(ValueError):
                self.testOlio5.add_author("Pena")

    def test_get_authors_sorted_toimii(self):
        self.testOlio.add_author("Aapinen Aapo")
        self.testOlio.add_author("Sininen Sini")
        self.testOlio.add_author("Banaani Bale")
        self.assertEqual(self.testOlio.get_authors_sorted(),["Aapinen Aapo","Banaani Bale","Sininen Sini"])
        
        

# Testeissä käytetään omaa pientä skeemaa, jotta ne eivät riipu
# oikean bibtex_types.json-tiedoston sisällöstä.
TEST_SCHEMA = {
    "bibtex": {
        "article": {
            "required": ["author", "title", "journal", "year"]
        },
        "book": {
            # lista = vaihtoehtoiset kentät
            "required": ["title", ["author", "editor"], "publisher", "year"]
        },
        "conference": {
            "required": ["author", "title", "booktitle", "year"]
        },
        "inproceedings": {
            "alias_of": "conference"
        },
    }
}


@pytest.fixture
def make_reference():
    """Luo Reference-olion ilman oikeaa JSON-tiedostoa."""
    def _make(entry_type):
        with patch(
            "ot_miniprojekti_ryhma9.reference.open",
            mock_open(read_data=json.dumps(TEST_SCHEMA)),
            create=True,
        ):
            return Reference(entry_type)
    return _make


# --- konstruktori ---

def test_entry_type_muunnetaan_pieniksi_kirjaimiksi(make_reference):
    ref = make_reference("ARTICLE")

    assert ref.entry_type == "article"


def test_viitekoodi_on_aluksi_tyhja(make_reference):
    ref = make_reference("article")

    assert ref.viitekoodi == ""


def test_pakolliset_kentat_alustetaan_oikein(make_reference):
    ref = make_reference("article")

    assert ref.attributes == {
        "author": [],
        "title": None,
        "journal": None,
        "year": None,
    }


def test_vaihtoehtoiset_kentat_lisataan_kaikki(make_reference):
    ref = make_reference("book")

    assert ref.attributes == {
        "title": None,
        "author": [],
        "editor": None,
        "publisher": None,
        "year": None,
    }


def test_skeema_ladataan_tiedostosta(make_reference):
    ref = make_reference("article")

    assert ref.schema == TEST_SCHEMA


def test_oikea_json_tiedosto_ladataan_polusta():
    m = mock_open(read_data=json.dumps(TEST_SCHEMA))

    with patch("ot_miniprojekti_ryhma9.reference.open", m, create=True):
        Reference("article")

    path = m.call_args.args[0]
    assert Path(path).name == "bibtex_types.json"
    assert m.call_args.args[1] == "r"
    assert m.call_args.kwargs["encoding"] == "utf-8"


# --- get_definition ---

def test_tuntematon_tyyppi_aiheuttaa_virheen(make_reference):
    with pytest.raises(ValueError, match="Tuntematon BibTeX tyyppi: foo"):
        make_reference("foo")


def test_get_definition_palauttaa_maarittelyn(make_reference):
    ref = make_reference("article")

    assert ref.get_definition() == TEST_SCHEMA["bibtex"]["article"]


def test_alias_ratkaistaan_alkuperaiseen_tyyppiin(make_reference):
    ref = make_reference("inproceedings")

    assert ref.get_definition() == TEST_SCHEMA["bibtex"]["conference"]
    assert "booktitle" in ref.attributes


# --- attribuutit ---

def test_get_attributes_palauttaa_attribuutit(make_reference):
    ref = make_reference("article")

    assert ref.get_attributes() is ref.attributes


def test_set_attribute_asettaa_arvon(make_reference):
    ref = make_reference("article")

    ref.set_attribute("title", "Testiartikkeli")

    assert ref.get_attributes()["title"] == "Testiartikkeli"


def test_set_attribute_tuntemattomalla_avaimella_aiheuttaa_virheen(make_reference):
    ref = make_reference("article")

    with pytest.raises(ValueError, match="Unknown attribute: foo"):
        ref.set_attribute("foo", "bar")


# --- viitekoodi ---

def test_set_viitekoodi_ja_get_viitekoodi(make_reference):
    ref = make_reference("article")

    ref.set_viitekoodi("Matti2026")

    assert ref.get_viitekoodi() == "Matti2026"


# --- to_bibtex ---

def test_to_bibtex_palauttaa_oikean_artikkeliviitteen(make_reference):
    ref = make_reference("article")
    ref.set_viitekoodi("Malli2026")
    ref.add_author("Malli Maija")
    ref.set_attribute("title", "Python programming")
    ref.set_attribute("journal", "Python Journal")
    ref.set_attribute("year", "2026")

    expected = (
        "@article{Malli2026,\n"
        "    author = {Malli Maija},\n"
        "    title = {Python programming},\n"
        "    journal = {Python Journal},\n"
        "    year = {2026}\n"
        "}"
    )

    assert ref.to_bibtex() == expected


def test_to_bibtex_useampi_kirjoittaja(make_reference):
    ref = make_reference("article")
    ref.set_viitekoodi("Test2026")
    ref.add_author("Malli Maija")
    ref.add_author("Meikäläinen Matti")
    ref.set_attribute("title", "Test title")
    ref.set_attribute("journal", "Test journal")
    ref.set_attribute("year", "2026")

    result = ref.to_bibtex()

    assert "author = {Malli Maija and Meikäläinen Matti}" in result


def test_to_bibtex_ohittaa_tyhjät_attribuutit(make_reference):
    ref = make_reference("article")
    ref.set_viitekoodi("Test2026")
    ref.set_attribute("title", "Test title")
    ref.set_attribute("journal", "Test journal")
    ref.set_attribute("year", "2026")

    result = ref.to_bibtex()

    assert "author =" not in result
    assert "None" not in result


def test_to_bibtex_muodostaa_conference_aliasin(make_reference):
    ref = make_reference("conference")
    ref.set_viitekoodi("Conference2026")
    ref.add_author("Malli Maija")
    ref.set_attribute("title", "Conference paper")
    ref.set_attribute("booktitle", "Python Conference")
    ref.set_attribute("year", "2026")

    result = ref.to_bibtex()

    assert result.startswith("@inproceedings{Conference2026,")
    assert "@conference{" not in result


def test_to_bibtex_sulkee_viitteen_aaltosulkeella(make_reference):
    ref = make_reference("article")

    result = ref.to_bibtex()

    assert result.endswith("}")


   
