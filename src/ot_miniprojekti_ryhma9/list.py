import json
from pathlib import Path

class List:

    def listaa(self, lista):
        if len(lista) == 0:
            return
        print("\nReferences:\n------------------------------------------")
        for olio in lista:
            print(f"{olio.get_viitekoodi()}: {self.muotoile_viite(olio)}")
        print("------------------------------------------\n")


    def muotoile_henkilot(self, henkilot):
        if not henkilot:
            return ""

        return ", ".join(sorted(henkilot, key=str.casefold))

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
        print("\n--------------------------------")
        json_path = Path(__file__).parent / "bibtex_types.json"

        with open(json_path, "r", encoding="utf-8") as f:
            schema = json.load(f)

        for name in schema["bibtex"]:
            print(name)
        print("--------------------------------\n")

    def listaa_tagit(self,lista):
        tagi_lista=[]
        for viite in lista:
            if not viite.get_tags():
                continue
            else:
                for tagi in viite.get_tags():
                    if tagi in tagi_lista:
                        continue
                    else:
                        tagi_lista.append(tagi)
        if not tagi_lista:
            print("No tags have been added to any citations.")
        else:
            
            for tagi in tagi_lista:
                print("Citations tagged with ",tagi,":\n")
                for viite in lista:
                    if tagi in viite.get_tags():
                        print(f"{viite.get_viitekoodi()}: {self.muotoile_viite(viite)}")


    def listaa_yksi(self, olio):
        for key, value in olio.attributes.items():

            if key == "author":
                value = self.muotoile_henkilot(value)

            print(key + ": " + str(value))

        print("")