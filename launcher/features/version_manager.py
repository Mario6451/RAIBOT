def get_version_info(settings, version):
    launcher = settings["launcher"]

    avatar_system = launcher["avatar_system"].get(
        version,
        launcher["avatar_system"].get(version[:4], "legacy")
    )

    joinscript = launcher["joinscripts"].get(
        version,
        launcher["joinscripts"].get(version[:4])
    )

    params = launcher["join_parameters"][avatar_system]

    return {
        "avatar_system": avatar_system,
        "joinscript": joinscript,
        "parameters": params
    }
