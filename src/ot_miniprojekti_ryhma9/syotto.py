from list import List
from reference import Reference
import json
from pathlib import Path

class Syote:

    def __init__(self):
        self.listObj = List()
        self.viitteet = []

    def lataa_viitteet(self, tiedosto="viitteet.json"):
        if not Path(tiedosto).exists():
            return

        with open(tiedosto, "r", encoding="utf-8") as f:
            data = json.load(f)

        for koodi, tiedot in data.items():
            tiedot = dict(tiedot)
            viite = Reference(tiedot.pop("type"))
            viite.viitekoodi = koodi
            for key, value in tiedot.items():
                viite.attributes[key] = value
            self.viitteet.append(viite)

    def kysy_syotetta(self, tiedosto="viitteet.json"):

        inp = ""
        while inp != "exit":
            inp = input("Give input: ")

            if inp == "list":
                print("\n")
                self.listObj.listaa(self.viitteet)

            if inp == "new":
                type = input("Choose type for new citation (E.g inproceedings / article / book): ")
            elif inp == "new":
                type = input("Valitse uusi (inproceedings / article / book): ")
                try:
                    viite = Reference(type)
                except ValueError as e:
                    print(f"Virhe: {e}")
                    continue
                viite.set_viitekoodi(input("Reference code for your citation: "))
                for i in viite.attributes:
                    if i == "author":
                        syote = input("Enter author(s) Last name First name, separated by comma:")
                        print("")
                        authors = syote.split(",")
                        for author in authors:
                            author=author.strip()
                            if author:
                                viite.add_author(author)
                    else:
                        syote = input(i + ": ")
                        viite.set_attribute(i, syote)
                
                    syote = input(i + ": ")
                    viite.set_attribute(i, syote)

                self.viitteet.append(viite)
            if inp == "types":
                print("\n")
                self.listObj.types()
                print("\n")
            if inp == "help":
                print("Available commands: types / new / list / delete / edit / help / exit \n")

            elif inp == "types":
                self.listObj.types()

            elif inp == "help":
                print("Available commands: types / new / list")
        data = {
            f"{viite.viitekoodi}": {"type": viite.entry_type, **viite.attributes}
            for i, viite in enumerate(self.viitteet, start=1)
        }

        with open(tiedosto, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)