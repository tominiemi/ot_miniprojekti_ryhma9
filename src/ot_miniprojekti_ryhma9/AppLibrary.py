import io
import tempfile
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from syotto import Syote


class AppLibrary:
    def __init__(self):
        self._tmp = tempfile.TemporaryDirectory()
        self._tiedosto = Path(self._tmp.name) / "testViitteet.json"
        self._syote = Syote()
        self._inputs = []
        self._output = ""

    def input(self, value):
        self._inputs.append(value)

    def run_application(self):
        puskuri = io.StringIO()
        with patch("builtins.input", side_effect=[*self._inputs, "exit", "n"]), \
            redirect_stdout(puskuri):
            self._syote.kysy_syotetta(self._tiedosto)
        self._output = puskuri.getvalue()
        self._inputs = []

    def output_should_contain(self, value):
        if value not in self._output:
            raise AssertionError(f'Output "{value}" is not in {self._output}')