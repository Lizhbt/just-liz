"""
Système de combat PvE pour VEX Numwork
"""

import random
from slimes import SLIMES

class CombatEncounter:
    def __init__(self, player_slime, enemy_slime_id, difficulty=1.0):
        self.player_slime = player_slime
        self.enemy_id = enemy_slime_id
        self.enemy_data = SLIMES[enemy_slime_id].copy()
        self.difficulty = difficulty

        self.player_hp = player_slime["hp"]
        self.enemy_hp = int(self.enemy_data["hp"] * difficulty)
        self.enemy_max_hp = self.enemy_hp

        self.turn = 0
        self.log = []
        self.finished = False
        self.player_won = False

    def calculate_damage(self, attacker, defender):
        base = max(1, int(attacker["atk"] * 1.4 - defender["def"] * 0.6))
        variance = random.randint(-2, 2)
        return max(1, base + variance)

    def player_attack(self):
        if self.finished:
            return

        damage = self.calculate_damage(self.player_slime, self.enemy_data)
        self.enemy_hp -= damage
        self.log.append(f"{self.player_slime['nom']} -> {damage} dmg")

        if self.enemy_hp <= 0:
            self.finished = True
            self.player_won = True
            self.log.append(f"Victoire! +{self.enemy_data['xp']} XP")
            return

        self.enemy_turn()

    def enemy_turn(self):
        damage = self.calculate_damage(self.enemy_data, self.player_slime)
        self.player_hp -= damage
        self.log.append(f"{self.enemy_data['nom']} -> {damage} dmg")

        if self.player_hp <= 0:
            self.finished = True
            self.player_won = False
            self.log.append("Defaite...")

    def get_log(self, last_n=4):
        return self.log[-last_n:] if self.log else []

    def get_reward(self):
        if self.player_won:
            return {
                "xp": self.enemy_data["xp"],
                "gold": int(self.enemy_data["xp"] * 0.5),
            }
        return {"xp": 0, "gold": 0}


class WaveCombat:
    def __init__(self, player_slime, zone, difficulty=1.0):
        self.player_slime = player_slime
        self.zone = zone
        self.difficulty = difficulty
        self.wave = 0
        self.current_combat = None
        self.rewards = {"xp": 0, "gold": 0}
        self.finished = False

        self.enemies = self.generate_enemies()
        self.start_wave()

    def generate_enemies(self):
        slime_ids = list(SLIMES.keys())
        zone_slimes = [s for s in slime_ids if SLIMES[s].get("zone") == self.zone]

        enemies = []
        for i in range(min(self.zone, 3)):
            if zone_slimes:
                enemies.append(random.choice(zone_slimes))
            else:
                enemies.append(random.choice(slime_ids))

        return enemies

    def start_wave(self):
        self.wave += 1
        if self.wave > len(self.enemies):
            self.finished = True
            return

        enemy_id = self.enemies[self.wave - 1]
        wave_difficulty = self.difficulty * (1 + (self.wave - 1) * 0.2)
        self.current_combat = CombatEncounter(
            self.player_slime, enemy_id, wave_difficulty
        )

    def player_attack(self):
        if not self.current_combat or self.finished:
            return

        self.current_combat.player_attack()

        if self.current_combat.finished:
            if self.current_combat.player_won:
                reward = self.current_combat.get_reward()
                self.rewards["xp"] += reward["xp"]
                self.rewards["gold"] += reward["gold"]
                self.start_wave()
            else:
                self.finished = True

    def get_status(self):
        if not self.current_combat:
            return None

        return {
            "wave": self.wave,
            "total_waves": len(self.enemies),
            "player_hp": max(0, self.current_combat.player_hp),
            "enemy_hp": max(0, self.current_combat.enemy_hp),
            "enemy_max_hp": self.current_combat.enemy_max_hp,
            "enemy_name": self.current_combat.enemy_data["nom"],
            "finished": self.current_combat.finished,
            "won": self.current_combat.player_won if self.current_combat.finished else None,
        }
