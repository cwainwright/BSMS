import files
import json

METADATATEMPLATE = files.get_template("metadata")

class Metadata:
    def __init__(self, project):
        self.__project = project
        if self.filename not in self.__project.namelist:
            with open(self.__project.filepath/self.filename, "w") as file:
                json.dump(METADATATEMPLATE, file, indent=4)
        self.data = self.load()
    
    @property
    def filename(self) -> str:
        return "metadata.metadata"
    
    def load(self) -> dict:
        data = self.__project.read_json(self.filename)
        if data is None:
            data = METADATATEMPLATE
        return data
    
    def save(self):
        self.__project.write_json(self.filename, self.data, indent=2)
    
    def __repr__(self) -> str:
        return f"Infofile: {self['_songFilename']}"

    def __str__(self) -> str:
        return f"{self['_songFilename']}"

    def __iter__(self) -> list:
        return self.data.items()

    def __getitem__(self, __name: str):
        return self.data[__name]

    def __setitem__(self, key: str, value):
        self.data.update({key: value})

    def get(self, __key, __value=None):
        try:
            return self[__key]
        except KeyError:
            if __value is None:
                raise KeyError
            return __value
        
    def set(self, __key, __value):
        self.data.update({__key: __value})