
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