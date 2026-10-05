"""
Profil joueur et gestion du roster
"""

import uuid

class Player:
    def __init__(self, name="Aventurier"):
        self.name = name
        self.level = 1
        self.xp = 0
        self.xp_next_level = 50
        self.gold = 0
        self.roster = []
        self.active_slime_idx = None

    def add_xp(self, amount):
        self.xp += amount

        while self.xp >= self.xp_next_level:
            self.xp -= self.xp_next_level
            self.level += 1
            self.xp_next_level = int(self.xp_next_level * 1.2)
            return True
        return False

    def add_gold(self, amount):
        self.gold += amount

    def add_slime(self, slime_data):
        slime = {
            "id": str(uuid.uuid4())[:8],
            "nom": slime_data["nom"],
            "emoji": slime_data["emoji"],
            "rarete": slime_data["rarete"],
            "hp": slime_data["hp"],
            "atk": slime_data["atk"],
            "def": slime_data["def"],
            "vit": slime_data["vit"],
        }
        self.roster.append(slime)

        if self.active_slime_idx is None:
            self.active_slime_idx = 0

        return slime

    def get_active_slime(self):
        if not self.roster or self.active_slime_idx is None:
            return None
        return self.roster[self.active_slime_idx]

    def set_active_slime(self, idx):
        if 0 <= idx < len(self.roster):
            self.active_slime_idx = idx
            return True
        return False

    def has_slimes(self):
        return len(self.roster) > 0

    def get_stats_summary(self):
        return {
            "level": self.level,
            "xp": self.xp,
            "xp_to_next": self.xp_next_level,
            "gold": self.gold,
            "roster_size": len(self.roster),
            "active_slime": self.get_active_slime(),
        }
