"""
Système de chasse aux slimes pour VEX Numwork
"""

import random
from slimes import SLIMES

class HuntEncounter:
    def __init__(self, zone):
        self.zone = zone
        self.slime_id = self.pick_slime()
        self.slime_data = SLIMES[self.slime_id]
        self.choice = None
        self.result = None
        self.finished = False

    def pick_slime(self):
        zone_slimes = [
            sid for sid, data in SLIMES.items()
            if data.get("zone") == self.zone
        ]
        return random.choice(zone_slimes) if zone_slimes else "slime_001"

    def kill(self):
        self.choice = "kill"
        self.result = {
            "action": "kill",
            "xp": int(self.slime_data["xp"] * 0.8),
            "gold": int(self.slime_data["xp"] * 0.3),
            "slime_captured": None,
        }
        self.finished = True

    def capture(self):
        self.choice = "capture"
        chance = self.slime_data["chance_capture"]

        if random.random() < chance:
            captured_slime = self.slime_data.copy()
            captured_slime["hp"] = int(captured_slime["hp"] * random.uniform(0.85, 1.15))
            captured_slime["atk"] = int(captured_slime["atk"] * random.uniform(0.85, 1.15))
            captured_slime["def"] = int(captured_slime["def"] * random.uniform(0.85, 1.15))
            captured_slime["vit"] = int(captured_slime["vit"] * random.uniform(0.85, 1.15))

            self.result = {
                "action": "capture",
                "success": True,
                "xp": self.slime_data["xp"],
                "gold": 0,
                "slime_captured": captured_slime,
            }
        else:
            self.result = {
                "action": "capture",
                "success": False,
                "xp": int(self.slime_data["xp"] * 0.5),
                "gold": 0,
                "slime_captured": None,
            }

        self.finished = True

    def flee(self):
        self.choice = "flee"
        self.result = {
            "action": "flee",
            "xp": 0,
            "gold": 0,
            "slime_captured": None,
        }
        self.finished = True
