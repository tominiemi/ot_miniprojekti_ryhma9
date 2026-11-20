import json
from pathlib import Path
from reference import Reference
class List:

    def listaa(self, lista):
        for olio in lista:
            print(olio.get_viitekoodi())
            for key in olio.attributes:
                print(key + ": " + str(olio.attributes[key]))
            print("")

        

        