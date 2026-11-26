from list import List
from reference import Reference
import json
from pathlib import Path

class Syote:

    def __init__(self):
        self.listObj = List()
        self.viitteet = []
        self.unsaved = False

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

    def tallenna_bib(self, filename="viitteet.bib"):
        with open(filename, "w", encoding="utf-8") as file:
            for viite in self.viitteet:
                file.write(viite.to_bibtex())
                file.write("\n\n")

    def kysy_syotetta(self, tiedosto="viitteet.json"):

        inp = ""
        while inp != "exit":
            inp = input("Give input: ")

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
                self.unsaved = True
                
                    

                self.viitteet.append(viite)
            elif inp == "types":
                print("\n")
                self.listObj.types()

            elif inp.startswith("edit"):
                osat = inp.split(maxsplit=1)

                if len(osat) != 2:
                    print("Usage: edit [code]")
                    continue

                viitekoodi = osat[1]
                
                viite = next(
                    (v for v in self.viitteet if v.viitekoodi == viitekoodi),
                    None
                )

                if viite is None:
                    print(f"Reference code '{viitekoodi}' not found")
                    continue

                print(f"\nEdit reference: '{viite.viitekoodi}'")
                print(f"Type: {viite.entry_type}\n")

                for key, value in viite.attributes.items():
                    uusi_arvo = input(f"{key} [{value}]: ")

                    if uusi_arvo.strip():
                        viite.set_attribute(key, uusi_arvo)

                print("\nReference updated")

                print("\n")

            elif inp == "bibtex":
                self.tallenna_bib()
                print("BibTeX file created!")
            
            elif inp.startswith("help"):
                osat = inp.split(" ")
                command = osat[1] if len(osat) > 1 else "Try again!"

                match command:
                    case "":
                        print("Available commands: types / new / list / delete / edit / exit / bibtex\n")
                    case "help":
                        print("Lists all available commands, (help [command]) prints specific commands info\n")
                    case "new":
                        print("Start adding a new citation (new [type])\n")
                    case "list":
                        print("Gives list of all existing citations\n")
                    case "delete":
                        print("Delete a citation (delete MISSING INSTRUCTIONS)\n")
                    case "edit":
                        print("Edit an existing citation (edit [Reference code])\n" \
                        "Asks for info again, type updated info, press enter to move next\n" \
                        "Just press enter, if you dont want to change the field\n")
                    case "exit":
                        print("Closes and shuts down the application,\nall additions are automatically saved.\n")
                    case "types":
                        print("Gives a list of the available types of citations\n")
                    case "bibtex":
                        print("Creates .bib file from current citations")

        if self.unsaved:
            talleennetaanko = input("Do you want to save? (y/n): ")

            if talleennetaanko.strip() == "y":
                data = {
                    f"{viite.viitekoodi}": {"type": viite.entry_type, **viite.attributes}
                    for i, viite in enumerate(self.viitteet, start=1)
                }
                with open(tiedosto, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
            