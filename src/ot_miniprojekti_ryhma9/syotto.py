
from list import List
from reference import Reference
import json

class Syote:



    def __init__(self):
        self.listObj = List()
        self.viitteet = []

    def kysy_syotetta(self):
        
        inp = ""
        while inp != "exit":
            inp = input("anna syote: ")

            if inp == "list":
                self.listObj.listaa(self.viitteet)

            if inp == "new":
                type = input("Valitse uusi (inproceedings / article / book): ")
                try:
                    viite = Reference(type)
                except ValueError as e:
                    print(f"Virhe: {e}")
                    continue
                viite.set_viitekoodi(input("Viitekoodi: "))
                for i in viite.attributes:
                    syote = input(i + ": ")
                    viite.set_attribute(i, syote)
                
                self.viitteet.append(viite)

        data = {f"viite{i}": viite.attributes for i, viite in enumerate(self.viitteet, start=1)}

        with open("viitteet.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


                

                
                                
