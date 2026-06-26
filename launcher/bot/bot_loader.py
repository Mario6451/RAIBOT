import configparser

def load_avatar(path):
    cfg = configparser.ConfigParser()
    cfg.read(path)

    avatar = cfg["Avatar"]
    return {k: avatar.get(k, "0") for k in avatar}
