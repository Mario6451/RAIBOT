def make_sigma_binary(avatar):
    parts = [
        avatar["head2"], avatar["torso2"], avatar["rightleg2"], avatar["leftleg2"],
        avatar["rightarm2"], avatar["leftarm2"], avatar["r15real"],
        avatar["hat1id"], avatar["hat2id"], avatar["hat3id"],
        avatar["shirtid"], avatar["tshirtid"], avatar["pantsid"], avatar["faceid"]
    ]
    joined = "|".join(str(p) for p in parts)
    return joined.encode("utf-8").hex().upper()
