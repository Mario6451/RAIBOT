import os
import json

DEFAULT_AVATAR = """[Avatar]
head=0
torso=0
leftarm=0
rightarm=0
leftleg=0
rightleg=0
hat1id=0
hat2id=0
hat3id=0
shirtid=0
tshirtid=0
pantsid=0
faceid=0
"""

DEFAULT_PROFILE = {
    "behavior": {},
    "settings": {}
}

def create_bot_folder(name):
    folder = os.path.join("bots", name)
    os.makedirs(folder, exist_ok=True)

    with open(os.path.join(folder, "avatar.ini"), "w") as f:
        f.write(DEFAULT_AVATAR)

    with open(os.path.join(folder, "profile.json"), "w") as f:
        json.dump(DEFAULT_PROFILE, f, indent=4)

    return folder
