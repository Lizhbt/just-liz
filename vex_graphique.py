"""
VEX Numwork - Interface graphique Pokemon-style
Utilise pygame pour Numwork (384x272)
"""

import pygame
import random
from enum import Enum

pygame.init()
SCREEN_WIDTH = 384
SCREEN_HEIGHT = 272
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("VEX")
clock = pygame.time.Clock()

# Couleurs
BLACK = (10, 14, 39)
DARK_BLUE = (26, 31, 58)
WHITE = (255, 255, 255)
GREEN = (0, 255, 136)
RED = (255, 51, 85)
YELLOW = (255, 200, 0)

class GameState(Enum):
    MENU = 1
    ZONE_SELECT = 2
    HUNT = 3
    COMBAT = 4
    POKEDEX = 5
    GAME_OVER = 6
    VICTORY = 7

class Slime:
    def __init__(self, emoji, nom, hp, atk, def_, xp, zone):
        self.emoji = emoji
        self.nom = nom
        self.hp = hp
        self.atk = atk
        self.def_ = def_
        self.xp = xp
        self.zone = zone

SLIMES = {
    1: Slime("🟢", "Gelée", 20, 10, 5, 10, 1),
    2: Slime("🟣", "Essence", 30, 15, 8, 25, 2),
    3: Slime("🟡", "Cristal", 40, 20, 12, 50, 3),
    4: Slime("🔴", "Masse", 60, 30, 15, 100, 4),
    5: Slime("🖤", "Abysse", 100, 50, 25, 200, 5),
}

def draw_text(text, x, y, size=16, color=WHITE):
    font = pygame.font.Font(None, size)
    txt = font.render(text, True, color)
    screen.blit(txt, (x, y))

def draw_box(x, y, w, h, color=DARK_BLUE, border=1):
    pygame.draw.rect(screen, color, (x, y, w, h))
    if border:
        pygame.draw.rect(screen, GREEN, (x, y, w, h), border)

def draw_hp_bar(x, y, current, max_hp, width=150):
    # Fond
    draw_box(x, y, width, 15, BLACK, 1)
    # Remplissage
    fill_width = (current / max_hp) * width if max_hp > 0 else 0
    pygame.draw.rect(screen, GREEN, (x+2, y+2, fill_width-4, 11))
    # Texte
    draw_text(f"{current}/{max_hp}", x+5, y-1, 12, WHITE)

def draw_button(x, y, text, width=80, height=30, selected=False):
    color = GREEN if selected else DARK_BLUE
    draw_box(x, y, width, height, color, 2)
    draw_text(text, x+5, y+5, 14, BLACK if selected else WHITE)

class Game:
    def __init__(self):
        self.level = 1
        self.xp = 0
        self.xp_needed = 50
        self.zone = 1
        self.roster = [SLIMES[1]]
        self.discovered = {1: True}
        self.player_slime = self.roster[0]
        self.player_hp = self.player_slime.hp
        self.state = GameState.MENU
        self.running = True

        # Hunt state
        self.hunt_stage = 0
        self.hunt_enemy = None
        self.hunt_enemy_hp = 0

        # Combat state
        self.combat_enemy = None
        self.combat_enemy_hp = 0

    def draw_menu(self):
        screen.fill(BLACK)

        # Titre
        font = pygame.font.Font(None, 48)
        txt = font.render("VEX", True, GREEN)
        screen.blit(txt, (SCREEN_WIDTH//2 - 40, 40))

        # Sous-titre
        draw_text("Numwork Edition", SCREEN_WIDTH//2 - 60, 100, 20, WHITE)

        # Boutons
        draw_button(SCREEN_WIDTH//2 - 50, 150, "JOUER", 100, 40, True)
        draw_button(SCREEN_WIDTH//2 - 50, 200, "POKEDEX", 100, 40)

        draw_text("Appuie sur ENTER pour jouer", 60, 250, 12, WHITE)

    def draw_zone_select(self):
        screen.fill(BLACK)

        draw_text(f"ZONE {self.zone}", 10, 20, 24, GREEN)
        draw_text(f"Level {self.level}  XP {self.xp}/{self.xp_needed}", 10, 50, 14, WHITE)
        draw_text(f"Équipe: {self.player_slime.emoji} {self.player_slime.nom}", 10, 70, 12, WHITE)

        # Affiche le slime de la zone
        slime = SLIMES[self.zone]
        font = pygame.font.Font(None, 80)
        txt = font.render(slime.emoji, True, WHITE)
        screen.blit(txt, (SCREEN_WIDTH//2 - 40, 100))

        draw_text(slime.nom, SCREEN_WIDTH//2 - 40, 170, 16, WHITE)

        # Options
        draw_text("(C) Combat  (H) Chasse  (P) Pokedex", 20, 235, 11, YELLOW)

    def draw_hunt(self):
        screen.fill(BLACK)

        draw_text("CHASSE", 10, 10, 20, GREEN)

        # Grand emoji du slime
        font = pygame.font.Font(None, 100)
        txt = font.render(self.hunt_enemy.emoji, True, WHITE)
        screen.blit(txt, (SCREEN_WIDTH//2 - 50, 50))

        draw_text(self.hunt_enemy.nom, SCREEN_WIDTH//2 - 30, 160, 18, WHITE)

        if self.hunt_stage == 0:
            draw_text("Rencontré!", SCREEN_WIDTH//2 - 40, 190, 14, YELLOW)
            draw_text("(A) Tuer  (C) Capturer  (F) Fuir", 20, 230, 11, WHITE)
        elif self.hunt_stage == 1:
            draw_text("Vaincu!", SCREEN_WIDTH//2 - 40, 190, 14, GREEN)
            draw_text(f"+{int(self.hunt_enemy.xp*0.8)} XP", SCREEN_WIDTH//2 - 30, 220, 14, GREEN)
            draw_text("(ENTER) Continuer", 70, 250, 11, WHITE)
        else:
            captured = len(self.roster) > len([s for s in self.roster if s != self.hunt_enemy])
            draw_text("Capturé!" if captured else "Échappé!", SCREEN_WIDTH//2 - 50, 190, 14, GREEN)
            draw_text(f"+{self.hunt_enemy.xp} XP", SCREEN_WIDTH//2 - 30, 220, 14, GREEN)
            draw_text("(ENTER) Continuer", 70, 250, 11, WHITE)

    def draw_combat(self):
        screen.fill(BLACK)

        # Infos joueur (bas)
        draw_text(f"{self.player_slime.nom}", 10, 200, 16, WHITE)
        draw_hp_bar(10, 220, self.player_hp, self.player_slime.hp, 150)

        # Ennemi (haut)
        draw_text(f"{self.combat_enemy.nom}", 10, 10, 16, WHITE)
        draw_hp_bar(10, 30, self.combat_enemy_hp, self.combat_enemy.hp, 150)

        # Gros emoji ennemi
        font = pygame.font.Font(None, 70)
        txt = font.render(self.combat_enemy.emoji, True, WHITE)
        screen.blit(txt, (SCREEN_WIDTH - 80, 70))

        # Actions
        draw_button(10, 240, "ATQ", 50, 25, True)
        draw_button(70, 240, "FUY", 50, 25)

    def draw_pokedex(self):
        screen.fill(BLACK)

        draw_text("POKEDEX", 10, 10, 20, GREEN)
        draw_text(f"Capturés: {len(self.roster)-1}/{5}", 10, 40, 14, WHITE)

        # Affiche 4 slimes par écran en grille
        for i, (id_, slime) in enumerate(SLIMES.items()):
            if i >= 4:
                break

            col = i % 2
            row = i // 2
            x = 50 + col * 150
            y = 80 + row * 80

            # Boite
            draw_box(x-30, y-30, 110, 70, DARK_BLUE, 2)

            # Emoji
            font = pygame.font.Font(None, 50)
            if id_ in self.discovered or slime in self.roster:
                txt = font.render(slime.emoji, True, WHITE)
                screen.blit(txt, (x-15, y-25))
                draw_text(slime.nom, x-25, y+15, 11, WHITE)
            else:
                txt = font.render("?", True, RED)
                screen.blit(txt, (x-5, y-25))

        draw_text("(R) Retour", 10, 250, 11, YELLOW)

    def draw_game_over(self):
        screen.fill(BLACK)
        draw_text("DEFAITE!", SCREEN_WIDTH//2 - 60, 80, 32, RED)
        draw_text("Ton slime est KO...", SCREEN_WIDTH//2 - 80, 150, 16, WHITE)
        draw_text("(R) Recommencer", SCREEN_WIDTH//2 - 80, 220, 12, YELLOW)

    def draw_victory(self):
        screen.fill(BLACK)
        draw_text("VICTOIRE!", SCREEN_WIDTH//2 - 60, 80, 32, GREEN)
        draw_text(f"Level {self.level}  Slimes: {len(self.roster)}", SCREEN_WIDTH//2 - 80, 150, 16, WHITE)
        draw_text("(R) Recommencer", SCREEN_WIDTH//2 - 80, 220, 12, YELLOW)

    def add_xp(self, amount):
        self.xp += amount
        while self.xp >= self.xp_needed:
            self.xp -= self.xp_needed
            self.level += 1
            self.xp_needed = 50 + (self.level - 1) * 10
            self.player_slime.hp += 5
            self.player_hp = self.player_slime.hp

    def start_hunt(self):
        self.hunt_enemy = SLIMES[self.zone]
        self.hunt_enemy_hp = self.hunt_enemy.hp
        self.state = GameState.HUNT
        self.hunt_stage = 0

    def start_combat(self):
        self.combat_enemy = SLIMES[self.zone]
        self.combat_enemy_hp = self.combat_enemy.hp
        self.player_hp = self.player_slime.hp
        self.state = GameState.COMBAT

    def hunt_kill(self):
        xp_gain = int(self.hunt_enemy.xp * 0.8)
        self.add_xp(xp_gain)
        self.hunt_stage = 1

    def hunt_capture(self):
        if random.random() < 0.6:
            self.roster.append(self.hunt_enemy)
            self.discovered[self.zone] = True
            self.add_xp(self.hunt_enemy.xp)
        else:
            self.add_xp(int(self.hunt_enemy.xp * 0.5))
        self.hunt_stage = 2

    def hunt_flee(self):
        self.state = GameState.ZONE_SELECT

    def combat_attack(self):
        dmg = 5 + random.randint(0, 10)
        self.combat_enemy_hp -= dmg

        if self.combat_enemy_hp <= 0:
            xp_gain = int(self.combat_enemy.xp * 1.5)
            self.add_xp(xp_gain)
            self.zone += 1
            if self.zone > 5:
                self.state = GameState.VICTORY
            else:
                self.state = GameState.ZONE_SELECT
        else:
            enemy_dmg = 3 + random.randint(0, 8)
            self.player_hp -= enemy_dmg
            if self.player_hp <= 0:
                self.state = GameState.GAME_OVER

    def combat_flee(self):
        self.state = GameState.ZONE_SELECT

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if self.state == GameState.MENU:
                    if event.key == pygame.K_RETURN:
                        self.state = GameState.ZONE_SELECT

                elif self.state == GameState.ZONE_SELECT:
                    if event.key == pygame.K_c:
                        self.start_combat()
                    elif event.key == pygame.K_h:
                        self.start_hunt()
                    elif event.key == pygame.K_p:
                        self.state = GameState.POKEDEX

                elif self.state == GameState.HUNT:
                    if self.hunt_stage == 0:
                        if event.key == pygame.K_a:
                            self.hunt_kill()
                        elif event.key == pygame.K_c:
                            self.hunt_capture()
                        elif event.key == pygame.K_f:
                            self.hunt_flee()
                    else:
                        if event.key == pygame.K_RETURN:
                            self.state = GameState.ZONE_SELECT

                elif self.state == GameState.COMBAT:
                    if event.key == pygame.K_a:
                        self.combat_attack()
                    elif event.key == pygame.K_f:
                        self.combat_flee()

                elif self.state == GameState.POKEDEX:
                    if event.key == pygame.K_r:
                        self.state = GameState.ZONE_SELECT

                elif self.state == GameState.GAME_OVER or self.state == GameState.VICTORY:
                    if event.key == pygame.K_r:
                        self.__init__()

    def draw(self):
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.ZONE_SELECT:
            self.draw_zone_select()
        elif self.state == GameState.HUNT:
            self.draw_hunt()
        elif self.state == GameState.COMBAT:
            self.draw_combat()
        elif self.state == GameState.POKEDEX:
            self.draw_pokedex()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()
        elif self.state == GameState.VICTORY:
            self.draw_victory()

        pygame.display.flip()

    def update(self):
        self.handle_input()
        self.draw()
        clock.tick(30)

    def run(self):
        while self.running:
            self.update()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
