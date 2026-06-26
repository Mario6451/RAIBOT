import configparser

def convert_rblxhub_to_legacy(path):
    cfg = configparser.ConfigParser()
    cfg.read(path)

    avatar = cfg["Avatar"]

    hats = avatar.get("hats", "").split("|")
    clothing = avatar.get("clothing", "").split("|")
    body = avatar.get("bodycolor", "").split("|")

    return {
        "head": body[0],
        "torso": body[1],
        "leftarm": body[2],
        "rightarm": body[3],
        "leftleg": body[4],
        "rightleg": body[5],

        "hat1id": hats[0] if len(hats) > 0 else "0",
        "hat2id": hats[1] if len(hats) > 1 else "0",
        "hat3id": hats[2] if len(hats) > 2 else "0",

        "tshirtid": clothing[0] if len(clothing) > 0 else "0",
        "shirtid": clothing[1] if len(clothing) > 1 else "0",
        "pantsid": clothing[2] if len(clothing) > 2 else "0",

        "faceid": avatar.get("face", "0")
    }

def convert_to_sigmabinary(legacy):
    fields = [
        legacy["head"], legacy["torso"], legacy["leftarm"], legacy["rightarm"],
        legacy["leftleg"], legacy["rightleg"],
        legacy["hat1id"], legacy["hat2id"], legacy["hat3id"],
        legacy["shirtid"], legacy["tshirtid"], legacy["pantsid"], legacy["faceid"]
    ]

    joined = "|".join(fields)
    return joined.encode("utf-16le").hex()
