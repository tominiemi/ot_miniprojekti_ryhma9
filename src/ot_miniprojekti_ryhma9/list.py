import json
from pathlib import Path

class List:

    def listaa(self):
        path = Path(__file__).parent / "bibtex_types.json"
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for key in data["bibtex"]:
            print(key)