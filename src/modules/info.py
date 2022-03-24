from json import load, loads, dumps


class Info:
    def __init__(self, project):
        self.project = project
        zipfile = self.project.read()
        if "info.json" not in zipfile.namelist():
            with zipfile.open("info.json", "w") as info_file:
                info_file.write(dumps(info_template, indent=2).encode("utf-8"))
    
    def __repr__(self) -> str:
        return f"Infofile: {self['_songFilename']}"

    def __str__(self) -> str:
        return f"{self['_songFilename']}"

    def __iter__(self) -> list:
        zipfile = self.project.read()
        with zipfile.open("info.json", "r") as info_file:
            info = loads(info_file.read())
            return info.items()

    def __getitem__(self, __name: str):
        zipfile = self.project.read()
        with zipfile.open("info.json", "r") as info_file:
            info = loads(info_file.read())
            return info[__name]

    def __setitem__(self, key: str, value):
        self.update({key: value})

    def update(self, info: dict):
        zipfile_data = self.project.write()
        with zipfile_data.open("info.json", "w") as info_file:
            info = loads(info_file.read()).update(info)
            info_file.write(dumps(info).encode("utf-8"))

    def get(self, keyname, value=None):
        try:
            return self[keyname]
        except KeyError:
            if value is None:
                raise KeyError
            return value


info_template = load(open("src/modules/templates.json", "r")).get("info")

if __name__ == "__main__":
    from project import Project
    info = Info(Project("test.zip"))
    info.update({"name": "test"})