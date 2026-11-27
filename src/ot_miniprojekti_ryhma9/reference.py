from pathlib import Path

import json


class Reference:

    def __init__(self, entry_type):
        self.entry_type = entry_type.lower()
        self.attributes = {}
        self.viitekoodi = ""
        self.tagit = []

        # Haetaan JSON-määrittely
        json_path = Path(__file__).parent / "bibtex_types.json"

        with open(json_path, "r", encoding="utf-8") as file:
            self.schema = json.load(file)

        definition = self.get_definition()

        # Alustetaan pakolliset attribuutit
        for field in definition["required"]:
            if isinstance(field, list):
                for alternative in field:
                    self.attributes[alternative] = None
            else:
                self.attributes[field] = None
        if "author" in self.attributes:
            self.attributes["author"] = []


    
    def to_bibtex(self):
        entry_type = self.entry_type

        if entry_type == "conference":
            entry_type = "inproceedings"

        result = [f"@{entry_type}{{{self.viitekoodi},"]

        for key, value in self.attributes.items():

        # Ohitetaan tyhjät attribuutit
            if value is None or value == "" or value == []:
                continue

        # Author- ja editor-listat BibTeX-muotoon
            if key in ("author", "editor") and isinstance(value, list):
                value = " and ".join(value)

            result.append(f"    {key} = {{{value}}},")

    # Poistetaan viimeisen kentän pilkku
        if len(result) > 1:
            result[-1] = result[-1].rstrip(",")

        result.append("}")

        return "\n".join(result)
        
    def get_definition(self):
        if self.entry_type not in self.schema["bibtex"]:
            raise ValueError(
                f"Tuntematon BibTeX tyyppi: {self.entry_type}"
            )

        definition = self.schema["bibtex"][self.entry_type]

        # Käsitellään mahdollinen alias
        if "alias_of" in definition:
            definition = self.schema["bibtex"][definition["alias_of"]]

        return definition

    def get_attributes(self):
        return self.attributes

    def set_attribute(self, key, word):
        if key not in self.attributes:
            raise ValueError(f"Unknown attribute: {key}")

        self.attributes[key] = word

    def set_viitekoodi(self,viitekoodi):
        self.viitekoodi = viitekoodi

    def get_viitekoodi(self):
        return self.viitekoodi

    def add_author(self,author):
        if "author" not in self.attributes:
            raise ValueError("This reference type does not support authors")

        self.attributes["author"].append(author)

    def get_authors_sorted(self):
        return sorted(self.attributes["author"])

    def set_tag(self, tag):
        if tag not in self.tagit:
            self.tagit.append(tag)

    def get_tags(self):
        return self.tagit