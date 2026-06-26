class Bot:
    def __init__(self, name, controller, avatar_ini, ip, port, user_id, membership):
        self.name = name
        self.controller = controller
        self.avatar_ini = avatar_ini
        self.ip = ip
        self.port = port
        self.user_id = user_id
        self.membership = membership
        self.x = 0
        self.y = 0

class BotManager:
    def __init__(self):
        self.bots = []

    def add_bot(self, bot):
        self.bots.append(bot)

    def remove_bot(self, bot):
        if bot in self.bots:
            bot.controller.kill()
            self.bots.remove(bot)

    def get_bot_by_name(self, name):
        for b in self.bots:
            if b.name == name:
                return b
        return None

BOT_MANAGER = BotManager()
