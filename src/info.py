from json import load, dumps


class Info:
    def __init__(self, project):
        self.project = project
        if "info.json" not in self.project.zip.namelist():
            with self.project.zip.open("info.json", "w") as info_file:
                info_file.write(dumps(info_template, indent=2).encode("utf-8"))
    
    def __repr__(self) -> str:
        return f"Infofile: {self['_songFilename']}"

    def __str__(self) -> str:
        return f"{self['_songFilename']}"

    def __iter__(self) -> list:
        with self.project.zip.open("info.json", "r") as info_file:
            info = load(info_file)
            return info.items()

    def __getitem__(self, __name: str):
        with self.project.zip.open("info.json", "r") as info_file:
            info = load(info_file)
            return info[__name]

    def __setitem__(self, key: str, value):
        self.update({key: value})

    def update(self, info: dict):
        with self.project.zip.open("info.json", "w") as info_file:
            info = load(info_file).update(info)
            info_file.write(dumps(info))

    def get(self, keyname, value):
        try:
            return self[keyname]
        except KeyError:
            return value


info_template = load(open("src/templates.json", "r")).get("info")

if __name__ == "__main__":
    print(info_template)