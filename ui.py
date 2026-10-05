"""
Interface utilisateur pour Numwork
Affichage texte optimisé pour petit écran (384x272)
"""

class UI:
    def __init__(self, width=384, height=272):
        self.width = width
        self.height = height
        self.lines = []

    def clear(self):
        self.lines = []

    def add_line(self, text, padding=0):
        text_str = str(text)
        if padding > 0:
            text_str = text_str.center(self.width // 10)
        self.lines.append(text_str[:self.width // 8])

    def add_separator(self):
        self.lines.append("-" * (self.width // 8))

    def draw_player_status(self, player):
        self.add_line(f"[{player.name}]")
        self.add_line(f"Lvl {player.level} XP:{player.xp}/{player.xp_next_level}")
        self.add_line(f"Gold: {player.gold}")
        if player.get_active_slime():
            slime = player.get_active_slime()
            self.add_line(f"Equipe: {slime['emoji']} {slime['nom']}")
        self.add_separator()

    def draw_hunt_encounter(self, encounter):
        self.add_line("*** CHASSE ***")
        self.add_line(f"{encounter.slime_data['emoji']} {encounter.slime_data['nom']}")
        self.add_line(f"Rarete: {encounter.slime_data['rarete']}")
        self.add_separator()
        self.add_line("(A)ttaquer (C)apturer (F)uir")

    def draw_hunt_result(self, result):
        self.add_line("*** RESULTAT ***")
        if result["action"] == "kill":
            self.add_line(f"+{result['xp']} XP")
            self.add_line(f"+{result['gold']} Gold")
        elif result["action"] == "capture":
            if result["success"]:
                self.add_line("Capture OK!")
                self.add_line(f"+{result['xp']} XP")
            else:
                self.add_line("Echappee...")
                self.add_line(f"+{result['xp']} XP")
        elif result["action"] == "flee":
            self.add_line("Fuite...")

    def draw_combat_status(self, combat_status):
        self.add_line(f"COMBAT Vague {combat_status['wave']}/{combat_status['total_waves']}")
        self.add_separator()
        self.add_line(f"{combat_status['enemy_name']}")
        hp_bar = self.draw_bar(combat_status['enemy_hp'], combat_status['enemy_max_hp'], 10)
        self.add_line(f"Enemy: {hp_bar}")
        self.add_separator()
        self.add_line("(A)ttaquer (F)uir")

    def draw_bar(self, current, max_val, length=10):
        if max_val == 0:
            return "[" + "=" * length + "]"
        filled = int((current / max_val) * length)
        return "[" + "=" * filled + "-" * (length - filled) + "]"

    def draw_zone_intro(self, zone, player):
        self.add_line(f"=== ZONE {zone} ===")
        self.add_line(f"Lvl {player.level}")
        self.add_line("Pret? (O)ui (N)on")

    def draw_zone_boss_intro(self, zone):
        self.add_line(f"*** BOSS ZONE {zone} ***")
        self.add_line("Attention! Ennemi puissant!")
        self.add_line("(A)ttaquer (F)uir")

    def draw_game_over(self, reason, player):
        self.add_line("*** GAME OVER ***")
        self.add_line(reason)
        self.add_separator()
        self.add_line(f"Lvl {player.level}")
        self.add_line(f"Slimes: {len(player.roster)}")
        self.add_line(f"Gold: {player.gold}")
        self.add_line("(R)ecommencer (Q)uitter")

    def draw_victory(self, player):
        self.add_line("*** VICTOIRE ***")
        self.add_line("Tu as terasse tous les bosses!")
        self.add_separator()
        self.add_line(f"Lvl {player.level}")
        self.add_line(f"Slimes captures: {len(player.roster)}")
        self.add_line(f"Gold total: {player.gold}")
        self.add_line("(R)ecommencer (Q)uitter")

    def get_output(self):
        return "\n".join(self.lines)
