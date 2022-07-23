from json import load, loads, dumps


class Info:
    def __init__(self, project):
        self.__project = project
        if "info.json" not in self.__project.read.namelist():
            self.__project.append.write("info.json", arcname=self.__project.name, mode="w", data = dumps(info_template, indent=2).encode("utf-8"))
    
    def __repr__(self) -> str:
        return f"Infofile: {self['_songFilename']}"

    def __str__(self) -> str:
        return f"{self['_songFilename']}"

    def __iter__(self) -> list:
        with self.__project.read.open("info.json", "r") as info_file:
            info = loads(info_file.read())
            return info.items()

    def __getitem__(self, __name: str):
        with self.__project.read.open("info.json", "r") as info_file:
            info = loads(info_file.read())
            return info[__name]

    def __setitem__(self, key: str, value):
        self.update({key: value})

    def update(self, info: dict):
        with self.__project.read.open("info.json", "r") as info_file:
            info = loads(info_file.read()).update(info)
        self.__project.append.write("info.json", arcname = self.__project.name, data = dumps(info).encode("utf-8"))

    def get(self, keyname, value=None):
        try:
            return self[keyname]
        except KeyError:
            if value is None:
                raise KeyError
            return value


info_template = load(open("src/templates.json", "r")).get("info")

if __name__ == "__main__":
    from project import Project
    project = Project("test.zip")
    project.info.update({"_songFilename": "test"})