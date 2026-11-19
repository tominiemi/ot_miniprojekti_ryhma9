import json


class Reference:
    def __init__(self,type):
        with open("bibtex_types.json", "r", encoding="utf-8") as file:
            data = json.load(file)


    