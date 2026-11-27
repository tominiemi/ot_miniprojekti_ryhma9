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
        ref = Reference("article")
        ref.set_viitekoodi("hyva lahde")
        ref.set_attribute("title", "Testi artikkeli")
        ref.add_author("Meikalainen Matti")
        ref.set_attribute("year", "2002")

        lista = List()

        with patch("builtins.print") as mock_print:
            lista.listaa([ref])

        printed = [str(call.args[0]) for call in mock_print.call_args_list]

        assert any("hyva lahde" in line for line in printed)
        assert any("Testi artikkeli" in line for line in printed)
        assert any("Meikalainen Matti" in line for line in printed)
        assert any("2002" in line for line in printed)

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

        assert any("article" in line for line in actual)
        assert any("book" in line for line in actual)
        assert any("inproceedings" in line for line in actual)


if __name__ == "__main__":
    unittest.main()