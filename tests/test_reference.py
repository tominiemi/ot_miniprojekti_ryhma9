import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent / "src" / "ot_miniprojekti_ryhma9")
)

import unittest
from reference import Reference



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
        

