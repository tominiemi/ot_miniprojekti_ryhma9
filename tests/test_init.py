import unittest
from unittest.mock import Mock, call, patch

import ot_miniprojekti_ryhma9 as sovellus


class TestMain(unittest.TestCase):

    def aja_main(self):
        with patch("builtins.print") as mock_print, \
             patch("ot_miniprojekti_ryhma9.Syote") as mock_syote_luokka:
            sovellus.main()
        return mock_print, mock_syote_luokka

    def test_tulostaa_tervetulotekstin(self):
        mock_print, _ = self.aja_main()

        mock_print.assert_called_once()
        teksti = mock_print.call_args.args[0]
        self.assertIn("LaTeX-based citation application!", teksti)

    def test_tervetuloteksti_listaa_kaikki_komennot(self):
        mock_print, _ = self.aja_main()
        teksti = mock_print.call_args.args[0]

        for komento in ["help", "list", "list tags", "types", "new",
                        "edit", "bibtex", "delete", "exit"]:
            with self.subTest(komento=komento):
                self.assertIn(komento, teksti)

    def test_luo_yhden_syotteen(self):
        _, mock_syote_luokka = self.aja_main()

        mock_syote_luokka.assert_called_once_with()

    def test_lataa_viitteet_ennen_kuin_kysyy_syotetta(self):
        _, mock_syote_luokka = self.aja_main()
        syote = mock_syote_luokka.return_value

        self.assertEqual(syote.method_calls, [
            call.lataa_viitteet(),
            call.kysy_syotetta(),
        ])

    def test_tervetuloteksti_tulostetaan_ennen_sovelluksen_kaynnistysta(self):
        jarjestys = Mock()
        with patch("builtins.print") as mock_print, \
             patch("ot_miniprojekti_ryhma9.Syote") as mock_syote_luokka:
            jarjestys.attach_mock(mock_print, "print")
            jarjestys.attach_mock(mock_syote_luokka, "Syote")
            sovellus.main()

        nimet = [kutsu[0] for kutsu in jarjestys.mock_calls]
        self.assertEqual(nimet, [
            "print",
            "Syote",
            "Syote().lataa_viitteet",
            "Syote().kysy_syotetta",
        ])


if __name__ == "__main__":
    unittest.main()
