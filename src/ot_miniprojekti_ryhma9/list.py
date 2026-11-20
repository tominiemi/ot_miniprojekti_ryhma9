import json
from pathlib import Path
<<<<<<< HEAD
from reference import Reference
=======

>>>>>>> 1203450b22c517b6c77851c09ab7345e183db4db
class List:

    def listaa(self, lista):
        for olio in lista:
            for key in olio.attributes:
                print(key + ": " + str(olio.attributes[key].value()))

        

        