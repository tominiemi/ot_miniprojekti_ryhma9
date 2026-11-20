
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

        for tiedot in data.values():
            tiedot = dict(tiedot)          
            viite = Reference(tiedot.pop("type"))
            for key, value in tiedot.items():
                viite.attributes[key] = value
            self.viitteet.append(viite)
        
    def kysy_syotetta(self):
        
        inp = ""
        while inp != "exit":
            inp = input("anna syote: ")

            if inp == "list":
                self.listObj.listaa(self.viitteet)

            if inp == "new":
                type = input("Valitse uusi (inproceedings / article / book): ")
                viite = Reference(type)
                for i in viite.attributes:
                    syote = input(i + ": ")
                    viite.set_attribute(i, syote)
                self.viitteet.append(viite)
                

        data = {
            f"viite{i}": {"type": viite.entry_type, **viite.attributes}
            for i, viite in enumerate(self.viitteet, start=1)
        }

        with open("viitteet.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


                

                
                                
