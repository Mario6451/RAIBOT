# avatar_loader.py

import configparser


def load_avatar_ini(path):
    """
    Loads an RBLXHUB-style avatar.ini file and returns a dict.
    """
    config = configparser.ConfigParser()
    config.read(path, encoding="utf-8")

    av = config["Avatar"]

    # Parse body colors (6 values)
    body = av["bodycolor"].split("|")
    body = [int(x) if x else 0 for x in body]

    # Parse hats (3 values)
    hats = av["hats"].split("|")
    hats = [int(x) if x else 0 for x in hats]

    # Parse clothing (3 values)
    clothing = av["clothing"].split("|")
    clothing = [int(x) if x else 0 for x in clothing]

    # Parse package (6 values, ignored for R6 but kept)
    package = av["package"].split("|")
    package = [int(x) if x else 0 for x in package]

    return {
        "name": av["name"],
        "playerid": int(av["playerid"]),
        "membership": av["membership"],
        "r15": int(av["r15"]),
        "bodycolor": body,
        "hats": hats,
        "package": package,
        "clothing": clothing,
        "face": int(av["face"])
    }


def build_avatar_string(data):
    """
    Converts parsed avatar.ini data into the 14-field avatar string
    used by December 2016 Roblox.
    """

    b = data["bodycolor"]     # 6 values
    h = data["hats"]          # 3 values
    c = data["clothing"]      # 3 values

    fields = [
        b[0], b[1], b[2], b[3], b[4], b[5],   # body colors
        data["r15"],                          # R6/R15 flag
        h[0], h[1], h[2],                     # hats
        c[0], c[1], c[2],                     # clothing
        data["face"]                          # face
    ]

    return "|".join(str(x) for x in fields)


def encode_avatar_binary(avatar_string):
    """
    Encodes the 14-field avatar string into UTF-16LE hex binary
    suitable for the December 2016 Roblox client.
    """
    return avatar_string.encode("utf-16le").hex()
