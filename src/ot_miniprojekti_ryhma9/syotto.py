
from list import List

class Syote:

    def __init__(self):
        self.listObj = List()

    def kysy_syotetta(self):
    
        inp = ""
        while inp != "exit":
            inp = input("anna syote: ")

            if inp == "list":
                self.listObj.listaa()

            if inp == "new ":
                            inp = input("Valitse uusi (inproceedings / article / book): ")
                            inp == type 
                            viite = reference(type)
                            for i in viite.attributes:
                                syote = input(i + ": ")
                                viite.set_attribute(i, syote)
                                
