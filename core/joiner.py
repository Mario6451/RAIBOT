from core.settings import SETTINGS

def build_join_url(ip, port, username, user_id, membership, sigma):
    base = SETTINGS["join_url"]
    return (
        f"{base}?placeid=1818"
        f"&ip={ip}"
        f"&port={port}"
        f"&user={username}"
        f"&id={user_id}"
        f"&mship={membership}"
        f"&binary={sigma}"
    )
