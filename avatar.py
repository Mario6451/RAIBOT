import configparser

class AvatarData:
    def __init__(self, path: str):
        self.path = path

    def load(self) -> dict:
        config = configparser.ConfigParser()
        config.read(self.path)
        avatar = config["Avatar"]

        return {
            "name": avatar.get("name", "Robot1"),
            "playerid": int(avatar.get("playerid", "0")),
            "membership": avatar.get("membership", "None"),
            "r15": int(avatar.get("r15", "0")),
            "bodycolor": avatar.get("bodycolor", "").split("|"),
            "hats": [int(x) for x in avatar.get("hats", "").split("|") if x],
            "package": avatar.get("package", "").split("|"),
            "clothing": [int(x) for x in avatar.get("clothing", "").split("|") if x],
            "face": int(avatar.get("face", "0"))
        }
