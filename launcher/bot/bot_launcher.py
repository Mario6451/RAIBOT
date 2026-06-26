from launcher.features.version_manager import get_version_info
from launcher.features.join_builder import build_join_url

def launch_bot(settings, bot_avatar, version, extra):
    info = get_version_info(settings, version)

    base_url = settings["launcher"]["base_url"]
    joinscript = info["joinscript"]
    params = info["parameters"]

    values = {}
    values.update(bot_avatar)
    values.update(extra)

    url = build_join_url(base_url, joinscript, params, values)
    return url
