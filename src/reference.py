import json


class Reference:

    def __init__(self, entry_type):
        self.entry_type = entry_type.lower()
        self.attributes = {}

        # Haetaan JSON-määrittely
        definition = self.get_definition()

        # Alustetaan pakolliset attribuutit
        for field in definition["required"]:
            if isinstance(field, list):
                for alternative in field:
                    self.attributes[alternative] = None
            else:
                self.attributes[field] = None

        # Alustetaan valinnaiset attribuutit
        



    def get_definition(self):
        if self.entry_type not in self.schema["bibtex"]:
            raise ValueError(
                f"Unknown BibTeX type: {self.entry_type}"
            )

        definition = self.schema["bibtex"][self.entry_type]

        # Käsitellään mahdollinen alias
        if "alias_of" in definition:
            definition = self.schema["bibtex"][definition["alias_of"]]

        return definition
        


    