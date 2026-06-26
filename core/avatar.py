import configparser

def load_avatar_ini(path):
    cfg = configparser.ConfigParser()
    cfg.read(path)

    if "Avatar" not in cfg:
        raise ValueError("Invalid avatar INI: missing [Avatar] section")

    a = cfg["Avatar"]

    # R6 enforced
    head2 = torso2 = rightleg2 = leftleg2 = rightarm2 = leftarm2 = 1

    r15real = int(a.get("r15", 0))

    hats = a.get("hats", "").split("|")
    hat1 = int(hats[0]) if len(hats) > 0 and hats[0] else 0
    hat2 = int(hats[1]) if len(hats) > 1 and hats[1] else 0
    hat3 = int(hats[2]) if len(hats) > 2 and hats[2] else 0

    clothing = a.get("clothing", "").split("|")
    tshirt = int(clothing[0]) if len(clothing) > 0 and clothing[0] else 0
    shirt = int(clothing[1]) if len(clothing) > 1 and clothing[1] else 0
    pants = int(clothing[2]) if len(clothing) > 2 and clothing[2] else 0

    face = int(a.get("face", 0))

    return {
        "head2": head2,
        "torso2": torso2,
        "rightleg2": rightleg2,
        "leftleg2": leftleg2,
        "rightarm2": rightarm2,
        "leftarm2": leftarm2,
        "r15real": r15real,
        "hat1id": hat1,
        "hat2id": hat2,
        "hat3id": hat3,
        "shirtid": shirt,
        "tshirtid": tshirt,
        "pantsid": pants,
        "faceid": face
    }
