import json
from pathlib import Path
from .list import List
from .reference import Reference

class Syote:

    def __init__(self):
        self.list_obj = List()
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
            tagit = tiedot.pop("tags", [])
            viite.tagit = tagit
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
            inp = input("Give input: ").strip()

            if inp.startswith("list") :
                osat = inp.split()
                command = osat[1] if len(osat) > 1 else ""
                
                match command:
                    case "":
                        self.listObj.listaa(self.viitteet)
                    case "tags":
                        self.listObj.listaa_tagit(self.viitteet)


                

            elif inp == "new":
                type = input("Choose type for new citation (E.g inproceedings / article / book): ")
            
                try:
                    viite = Reference(type)
                except ValueError as e:
                    print(f"Virhe: {e}")
                    continue
                
                samaKoodi = True
                while samaKoodi:
                    samaKoodi = False
                    inpViite = input("Reference code for your citation: ").strip()
                    
                    for v in self.viitteet:
                        if v.viitekoodi == inpViite:
                            samaKoodi = True
                    if samaKoodi:
                        print("Viitekoodi löytyy jo!")
                        continue
                viite.set_viitekoodi(inp_viite)
                for i in viite.attributes:
                    if i == "author":
                        syote = input("Enter author(s) Last name First name, separated by comma:")
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

            elif inp == "delete":
                print("which one to delete? (0 to cancel)")
                for ind, v in enumerate(self.viitteet):
                    print(ind+1, ":", v.viitekoodi)
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

            elif inp == "types":
                self.list_obj.types()

            elif inp.startswith("edit"):
                osat = inp.split()
                #osat = inp.split(maxsplit=1)

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
                    print("Attribute '{attribuutti}' not found")
                    continue

                print(f"\nEdit reference:")
                print(f"Code: '{viite.viitekoodi}'")
                print(f"Type: {viite.entry_type}\n")
                self.list_obj.listaa_yksi(viite)

                if attribuutti:
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

            elif inp.startswith("tag"):
                osat = inp.split()
                if len(osat) != 3:
                    print("Usage: tag [code] [tag]")
                    continue
                viitekoodi = osat[1]
                tagi = osat[2]
                for viite in self.viitteet:
                    if viite.get_viitekoodi()==viitekoodi:
                        viite.set_tag(tagi)
                        self.unsaved = True
                        print("Tag: ",tagi," set for citation: ",viite.get_viitekoodi())
                
                

            
            elif inp == "help":
                print("Available commands: types / new / list / delete / edit / help / exit")

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
                    f"{viite.viitekoodi}": {"type": viite.entry_type, **viite.attributes,"tags":viite.get_tags()}
                    for i, viite in enumerate(self.viitteet, start=1)
                }
                with open(tiedosto, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
