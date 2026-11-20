
from list import List
from reference import Reference

class Syote:

    def __init__(self):
        self.listObj = List()

    def kysy_syotetta(self):
    
        inp = ""
        while inp != "exit":
            inp = input("anna syote: ")

            if inp == "list":
                self.listObj.listaa()

            if inp == "new":
                print("moikka")
                type = input("Valitse uusi (inproceedings / article / book): ")
                viite = Reference(type)
                for i in viite.attributes:
                    syote = input(i + ": ")
                    viite.set_attribute(i, syote)
                                
