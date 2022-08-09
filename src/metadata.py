import json

with open("src/JSON/templates.json", "r") as file:
    METADATATEMPLATE = json.load(file).get("metadata")

class Metadata:
    def __init__(self, project):
        self.__project = project
        self.data = self.load()
        
    def load(self) -> dict:
        data = self.__project.read_json("metadata.json")
        if data is None:
            data = METADATATEMPLATE
        return data
    
    def save(self):
        self.__project.write_json("metadata.json", self.data, indent=2)
    
    def __repr__(self) -> str:
        return f"Infofile: {self['_songFilename']}"

    def __str__(self) -> str:
        return f"{self['_songFilename']}"

    def __iter__(self) -> list:
        return self.data.items()

    def __getitem__(self, __name: str):
        return self.data[__name]

    def __setitem__(self, key: str, value):
        self.update({key: value})

    def update(self, item: dict):
        self.data.update(item)

    def get(self, keyname, value=None):
        try:
            return self[keyname]
        except KeyError:
            if value is None:
                raise KeyError
            return value
        
if __name__ == "__main__":
    from project import main
    main()