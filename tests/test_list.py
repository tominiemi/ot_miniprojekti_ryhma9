import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent / "src" / "ot_miniprojekti_ryhma9")
)

import json
import unittest
from unittest.mock import patch, mock_open
from reference import Reference
from list import List


class TestList(unittest.TestCase):

    def test_listaa(self):
        reference = Reference("article")

        reference.set_attribute("title", "Testi artikkeli")
        reference.set_attribute("author", "Matti Meikäläinen")
        reference.set_attribute("year", "2002")

        lista = List()

        with patch("builtins.print") as mock_print:
            lista.listaa([reference])

        mock_print.assert_any_call(reference.get_viitekoodi())

        mock_print.assert_any_call("title: Testi artikkeli")
        mock_print.assert_any_call("author: Matti Meikäläinen")
        mock_print.assert_any_call("year: 2002")

        mock_print.assert_called_with("")

    def test_listaa_tyhjalla_listalla(self):
        lista = List()

        with patch("builtins.print") as mock_print:
            lista.listaa([])

        mock_print.assert_not_called()

    def test_types(self):
        lista = List()

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
                lista.types()

        actual = [call.args[0] for call in mock_print.call_args_list]

        expected = [
            "article",
            "book",
            "inproceedings"
        ]

        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()