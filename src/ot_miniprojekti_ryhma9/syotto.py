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

    def onko_cancel(self, syote):
        syote = input(syote).strip()

        if syote.lower() == "cancel":
            return None

        return syote

    
    def kysy_syotetta(self, tiedosto="viitteet.json"):

        inp = ""
        while inp != "exit":
            inp = input("Give input: ").strip()

            if inp == "list":
                self.listObj.listaa(self.viitteet)

            elif inp.startswith("new"):
                cancelled = False 
                
                osat = inp.split(" ")
                tyyppi = osat[1] if len(osat) > 1 else ""

                if tyyppi == "":
                        tyyppi = self.onko_cancel("Type cancel to cancel adding new citation\nChoose type for new citation (E.g inproceedings / article / book): ")
                        if tyyppi is None:
                            continue
                try:
                    viite = Reference(tyyppi)
                except ValueError as e:
                    print(f"Virhe: {e}")
                    continue
                        
                samaKoodi = True
                while samaKoodi:
                    samaKoodi = False
                    inpViite = self.onko_cancel("Reference code for your citation: ")
                    if inpViite is None:
                        break
                    
                    for v in self.viitteet:
                        if v.viitekoodi == inpViite:
                            samaKoodi = True
                            break
                    if samaKoodi:
                        print("Viitekoodi löytyy jo!")
                        continue
                if inpViite is None:
                    print("Cancelled creating a new citation\n")
                    continue
                viite.set_viitekoodi(inpViite)

                

                for i in viite.attributes:
                    if i == "author":
                        syote = self.onko_cancel("Enter author(s) Last name First name, separated by comma:")
                        if syote is None:
                            cancelled = True
                            break
                      
                        authors = syote.split(",")
                        for author in authors:
                            author=author.strip()
                            if author:
                                viite.add_author(author)
                    else:
                    
                        syote = self.onko_cancel(i + ": ")
                        if syote is None:
                            cancelled = True
                            break

                        viite.set_attribute(i, syote)
                if cancelled:
                    print("Cancelled creating a new citation\n")
                    continue
                self.unsaved = True
                self.viitteet.append(viite) 
                print("Greated new citation")
           
            elif inp.startswith("delete"):
                osat = inp.split(" ")
                poistettava = osat[1] if len(osat) > 1 else ""

                match poistettava:
                    case "":
                        print("which one to delete? (0 to cancel)")
                        for ind, v in enumerate(self.viitteet):
                            print(ind+1, ":", v.viitekoodi)
                        try:
                        
                            delInp = int(input("Number: "))
                            if delInp == 0:
                                continue
                            if delInp > len(self.viitteet) or delInp < 0:
                                print("Index not found :(")
                                continue

                            for ind, v in enumerate(self.viitteet):
                                if delInp == ind+1:
                                    print(v.viitekoodi, " deleted")
                                    self.viitteet.pop(ind)
                            self.unsaved = True
                            print("---------------------------------------")
                        except ValueError:
                            print("No number given, or it was faulty, no citation was deleted")
                    case _:
                        poistettu = False

                        for ind, v in enumerate(self.viitteet):
                            if poistettava == v.viitekoodi:
                                self.viitteet.pop(ind)
                                self.unsaved = True
                                poistettu = True
                                print(v.viitekoodi, " deleted")

                        if not poistettu:
                            print("Reference code doesnt refer to an existing citation, nothing was deleted.")

                                         

            elif inp == "types":
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
                self.unsaved = True
                print("\nReference updated")

                print("\n")

            elif inp == "bibtex":
                self.tallenna_bib()
                print("BibTeX file created!")
            
            elif inp.startswith("help"):
                osat = inp.split(" ")
                command = osat[1] if len(osat) > 1 else ""

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
                        print("Delete a citation by giving its index number")
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
                    case _:
                        print("Try again, no such command found!")

        if self.unsaved:
            talleennetaanko = input("Do you want to save? (y/n): ")

            if talleennetaanko.strip() == "y":
                data = {
                    f"{viite.viitekoodi}": {"type": viite.entry_type, **viite.attributes}
                    for i, viite in enumerate(self.viitteet, start=1)
                }
                with open(tiedosto, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
            