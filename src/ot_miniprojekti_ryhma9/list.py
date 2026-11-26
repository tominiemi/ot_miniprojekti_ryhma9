import json
from pathlib import Path
from reference import Reference

class List:

    def listaa(self, lista):
        for olio in lista:
            print(f"{olio.get_viitekoodi()}: {self.muotoile_viite(olio)}")


    def muotoile_henkilot(self, henkilot):
        if not henkilot:
            return ""

        return ", ".join(henkilot)

    def muotoile_viite(self, viite):
        a = viite.attributes
        tyyppi = viite.entry_type

        author = self.muotoile_henkilot(a.get("author"))

        tekija = author
        year = a.get("year", "")
        title = a.get("title", "")

        if tyyppi == "article":
            result = f"{tekija} ({year}). {title}. {a.get('journal', '')}"

            if a.get("volume"):
                result += f", {a['volume']}"

            if a.get("number"):
                result += f"({a['number']})"

            if a.get("pages"):
                result += f", {a['pages']}"

        elif tyyppi == "book":
            result = f"{tekija} ({year}). {title}. {a.get('publisher', '')}"

            if a.get("address"):
                result += f", {a['address']}"

        elif tyyppi in ("inproceedings", "conference"):
            result = f"{tekija} ({year}). {title}. In: {a.get('booktitle', '')}"

            if a.get("pages"):
                result += f", {a['pages']}"

            if a.get("publisher"):
                result += f", {a['publisher']}"

        else:
            result = f"{tekija} ({year}). {title}"

        return result + "."



    def types(self):
        json_path = Path(__file__).parent / "bibtex_types.json"

        with open(json_path, "r", encoding="utf-8") as f:
            schema = json.load(f)

        for name in schema["bibtex"]:
            print(name)