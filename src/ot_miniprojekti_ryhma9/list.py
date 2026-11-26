import json
from pathlib import Path
from reference import Reference
class List:

    def listaa(self, lista):
        for olio in lista:
            print(olio.get_viitekoodi())
            for key in olio.attributes:
                if key == "author":
                    print("author(s): ")
                    for author in sorted(olio.attributes["author"]):
                        print (author)
                else:
                    print(key + ": " + str(olio.attributes[key]))
            print("")

    def types(self):
        json_path = Path(__file__).parent / "bibtex_types.json"

        with open(json_path, "r", encoding="utf-8") as f:
            schema = json.load(f)

        for name in schema["bibtex"]:
            print(name)
        

        