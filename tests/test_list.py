import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent / "src" / "ot_miniprojekti_ryhma9")
)

import unittest
from unittest.mock import patch
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

        mock_print.assert_any_call("title: Testi artikkeli")
        mock_print.assert_any_call("author: Matti Meikäläinen")
        mock_print.assert_any_call("year: 2002")


if __name__ == "__main__":
    unittest.main()