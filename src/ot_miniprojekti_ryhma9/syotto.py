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
            inp = input("\nGive input: ")

            if inp == "list":
                print("\n")
                self.listObj.listaa(self.viitteet)

            elif inp == "new":
                type = input("Choose type for new citation (E.g inproceedings / article / book): ")
            
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
                
                    

                self.viitteet.append(viite)
            elif inp == "types":
                print("\n")
                self.listObj.types()

            elif inp.startswith("edit"):
                osat = inp.split()

                if len(osat) < 2 or len(osat) > 3:
                    print("Usage: edit [code] or edit [code] [attribute]")
                    continue

                viitekoodi = osat[1]

                viite = next(
                    (v for v in self.viitteet if v.viitekoodi == viitekoodi),
                    None
                )

                if viite is None:
                    print(f"Reference code '{viitekoodi}' not found")
                    continue

                attribuutti = osat[2] if len(osat) == 3 else None

                if attribuutti and attribuutti not in viite.attributes:
                    print(f"Attribute '{attribuutti}' not found")
                    continue

                print(f"\nEdit reference:")
                print(f"Code: '{viite.viitekoodi}'")
                print(f"Type: {viite.entry_type}\n")
                self.listObj.listaa_yksi(viite)

                if (attribuutti):
                    muokattavat = {attribuutti: viite.attributes[attribuutti]}
                else:
                    muokattavat = viite.attributes

                for key, value in muokattavat.items():
                    if key == "author":
                        value = ", ".join(value)

                    uusi_arvo = input(f"{key} [{value}]: ")

                    if uusi_arvo.strip():
                        if key == "author":
                            authors = [author.strip() for author in uusi_arvo.split(",")]
                            viite.attributes[key] = authors
                        else:
                            viite.set_attribute(key, uusi_arvo)

                self.unsaved = True
                print("\nReference updated")
            elif inp == "help":
                print("Available commands: types / new / list / delete / edit / help / exit")

            
        data = {
            f"{viite.viitekoodi}": {"type": viite.entry_type, **viite.attributes}
            for i, viite in enumerate(self.viitteet, start=1)
        }

        with open(tiedosto, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)