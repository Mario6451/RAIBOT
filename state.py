import math

class WorldState:
    def __init__(self):
        self.self_pos = {"x": 0.0, "y": 0.0, "z": 0.0}
        self.players = {}

    def update_self(self, x: float, y: float, z: float):
        self.self_pos = {"x": x, "y": y, "z": z}

    def update_player(self, name: str, x: float, y: float, z: float):
        self.players[name] = {"x": x, "y": y, "z": z}

    def remove_player(self, name: str):
        if name in self.players:
            del self.players[name]

    def distance_to(self, name: str) -> float:
        if name not in self.players:
            return float("inf")
        p = self.players[name]
        dx = p["x"] - self.self_pos["x"]
        dz = p["z"] - self.self_pos["z"]
        return math.sqrt(dx * dx + dz * dz)

    def to_dict(self) -> dict:
        return {"self": self.self_pos, "players": self.players}
