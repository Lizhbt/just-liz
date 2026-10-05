"""
Boucle de jeu principale et états pour VEX Numwork
"""

import random
from enum import Enum
from config import GameMode, ADVENTURE_ZONES, SURVIVAL_START_DIFFICULTY, SURVIVAL_DIFFICULTY_INCREMENT
from player import Player
from hunt import HuntEncounter
from combat import WaveCombat
from ui import UI

class GameState(Enum):
    MENU = 1
    MODE_SELECT = 2
    ADVENTURE_ZONE = 3
    HUNT = 4
    COMBAT = 5
    GAME_OVER = 6
    VICTORY = 7
    SURVIVAL_ARENA = 8

class VexGame:
    def __init__(self):
        self.state = GameState.MENU
        self.mode = None
        self.player = None
        self.current_zone = 1
        self.hunt_encounter = None
        self.wave_combat = None
        self.ui = UI()
        self.survival_wave = 0
        self.survival_difficulty = SURVIVAL_START_DIFFICULTY

    def run(self):
        while True:
            self.ui.clear()

            if self.state == GameState.MENU:
                self.handle_menu()
            elif self.state == GameState.MODE_SELECT:
                self.handle_mode_select()
            elif self.state == GameState.ADVENTURE_ZONE:
                self.handle_adventure_zone()
            elif self.state == GameState.HUNT:
                self.handle_hunt()
            elif self.state == GameState.COMBAT:
                self.handle_combat()
            elif self.state == GameState.GAME_OVER:
                self.handle_game_over()
            elif self.state == GameState.VICTORY:
                self.handle_victory()
            elif self.state == GameState.SURVIVAL_ARENA:
                self.handle_survival()

            print(self.ui.get_output())

            try:
                choice = input("\n> ").strip().upper()
                self.process_input(choice)
            except (EOFError, KeyboardInterrupt):
                break

    def handle_menu(self):
        self.ui.add_line("=== VEX NUMWORK ===")
        self.ui.add_line("Jeu RPG de slimes")
        self.ui.add_separator()
        self.ui.add_line("(J)ouer (Q)uitter")

    def handle_mode_select(self):
        self.ui.add_line("=== MODE ===")
        self.ui.add_line("(1) Aventure")
        self.ui.add_line("(2) Survie")
        self.ui.add_line("(M) Menu")

    def handle_adventure_zone(self):
        if self.current_zone > ADVENTURE_ZONES:
            self.state = GameState.VICTORY
            return

        self.ui.draw_player_status(self.player)
        self.ui.add_line(f"=== ZONE {self.current_zone} ===")
        self.ui.add_line("Que faire?")
        self.ui.add_separator()
        self.ui.add_line("(C)ombattre")
        self.ui.add_line("(H)unter slimes")
        self.ui.add_line("(F)uir")

    def handle_hunt(self):
        if not self.hunt_encounter:
            self.hunt_encounter = HuntEncounter(self.current_zone)

        if not self.hunt_encounter.finished:
            self.ui.draw_player_status(self.player)
            self.ui.draw_hunt_encounter(self.hunt_encounter)
        else:
            self.ui.draw_player_status(self.player)
            self.ui.draw_hunt_result(self.hunt_encounter.result)
            self.ui.add_line("(S)uivant (C)ontinuer")

    def handle_combat(self):
        if not self.wave_combat:
            active_slime = self.player.get_active_slime()
            if not active_slime:
                self.state = GameState.GAME_OVER
                return

            self.wave_combat = WaveCombat(
                active_slime,
                self.current_zone,
                difficulty=1.0
            )

        status = self.wave_combat.get_status()
        if status:
            self.ui.draw_player_status(self.player)
            self.ui.draw_combat_status(status)

            if status["finished"]:
                self.ui.add_line(f"Resultat: {'VICTOIRE' if status['won'] else 'DEFAITE'}")
                self.ui.add_line("(S)uivant")

    def handle_game_over(self):
        self.ui.draw_game_over("Tu as ete vaincu!", self.player)

    def handle_victory(self):
        self.ui.draw_victory(self.player)

    def handle_survival(self):
        if not self.wave_combat:
            active_slime = self.player.get_active_slime()
            if not active_slime:
                self.state = GameState.GAME_OVER
                return

            zone_difficulty = min(self.survival_wave // 2 + 1, 5)
            self.wave_combat = WaveCombat(
                active_slime,
                zone_difficulty,
                difficulty=self.survival_difficulty
            )

        status = self.wave_combat.get_status()
        if status:
            self.ui.draw_player_status(self.player)
            self.ui.add_line(f"*** SURVIE ***")
            self.ui.add_line(f"Vague: {self.survival_wave}")
            self.ui.add_line(f"Diff: {self.survival_difficulty:.1f}x")
            self.ui.add_separator()
            self.ui.draw_combat_status(status)

            if status["finished"]:
                if status["won"]:
                    self.ui.add_line("Victoire!")
                    self.survival_wave += 1
                    self.survival_difficulty += SURVIVAL_DIFFICULTY_INCREMENT
                    self.wave_combat = None
                else:
                    self.ui.add_line("Vague perdue!")
                self.ui.add_line("(S)uivant (Q)uitter")

    def process_input(self, choice):
        if self.state == GameState.MENU:
            if choice == "J":
                self.state = GameState.MODE_SELECT
            elif choice == "Q":
                exit()

        elif self.state == GameState.MODE_SELECT:
            if choice == "1":
                self.start_adventure()
            elif choice == "2":
                self.start_survival()
            elif choice == "M":
                self.state = GameState.MENU

        elif self.state == GameState.ADVENTURE_ZONE:
            if choice == "C":
                self.wave_combat = None
                self.hunt_encounter = None
                self.state = GameState.COMBAT
            elif choice == "H":
                self.hunt_encounter = None
                self.state = GameState.HUNT
            elif choice == "F":
                self.state = GameState.GAME_OVER

        elif self.state == GameState.HUNT:
            if not self.hunt_encounter.finished:
                if choice == "A":
                    self.hunt_encounter.kill()
                elif choice == "C":
                    self.hunt_encounter.capture()
                elif choice == "F":
                    self.hunt_encounter.flee()
            else:
                if choice == "S":
                    self.apply_hunt_rewards()
                    self.wave_combat = None
                    self.state = GameState.COMBAT
                elif choice == "C":
                    self.hunt_encounter = None
                    self.state = GameState.ADVENTURE_ZONE

        elif self.state == GameState.COMBAT:
            if not self.wave_combat.finished:
                if choice == "A":
                    self.wave_combat.player_attack()
                elif choice == "F":
                    self.wave_combat.finished = True
            else:
                if choice == "S":
                    self.apply_combat_rewards()
                    if self.wave_combat.current_combat and self.wave_combat.current_combat.player_won:
                        self.current_zone += 1
                        if self.current_zone > ADVENTURE_ZONES:
                            self.state = GameState.VICTORY
                        else:
                            self.state = GameState.ADVENTURE_ZONE
                    else:
                        self.state = GameState.GAME_OVER

        elif self.state == GameState.GAME_OVER:
            if choice == "R":
                self.restart_game()
            elif choice == "Q":
                self.state = GameState.MENU

        elif self.state == GameState.VICTORY:
            if choice == "R":
                self.restart_game()
            elif choice == "Q":
                self.state = GameState.MENU

        elif self.state == GameState.SURVIVAL_ARENA:
            if not self.wave_combat or not self.wave_combat.finished:
                if self.wave_combat:
                    if choice == "A":
                        self.wave_combat.player_attack()
                    elif choice == "F":
                        self.wave_combat.finished = True
            else:
                if choice == "S":
                    self.apply_combat_rewards()
                    if self.wave_combat.current_combat and self.wave_combat.current_combat.player_won:
                        self.wave_combat = None
                    else:
                        self.state = GameState.GAME_OVER
                elif choice == "Q":
                    self.state = GameState.GAME_OVER

    def start_adventure(self):
        self.mode = GameMode.ADVENTURE
        self.player = Player("Aventurier")
        self.current_zone = 1

        from slimes import SLIMES
        starter_slime = SLIMES["slime_001"].copy()
        self.player.add_slime(starter_slime)

        self.state = GameState.ADVENTURE_ZONE

    def start_survival(self):
        self.mode = GameMode.SURVIVAL
        self.player = Player("Survivant")
        self.survival_wave = 1
        self.survival_difficulty = 0.8

        from slimes import SLIMES
        starter_slime = SLIMES["slime_003"].copy()
        self.player.add_slime(starter_slime)

        self.state = GameState.SURVIVAL_ARENA

    def apply_hunt_rewards(self):
        result = self.hunt_encounter.result
        self.player.add_xp(result["xp"])
        self.player.add_gold(result["gold"])

        if result["slime_captured"]:
            self.player.add_slime(result["slime_captured"])

    def apply_combat_rewards(self):
        if self.wave_combat.finished:
            if self.wave_combat.current_combat and self.wave_combat.current_combat.player_won:
                rewards = self.wave_combat.rewards
                self.player.add_xp(rewards["xp"])
                self.player.add_gold(rewards["gold"])

    def restart_game(self):
        self.player = None
        self.hunt_encounter = None
        self.wave_combat = None
        self.current_zone = 1
        self.survival_wave = 0
        self.state = GameState.MODE_SELECT
