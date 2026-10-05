# VEX Numwork - RPG de Chasse aux Slimes

Un jeu RPG solo pour calculatrice Numwork basé sur votre projet VEX Discord. Capture des slimes mystérieux, progressa à travers les zones, et deviens le maître absolu !

## 🎮 Modes de Jeu

### 📍 Mode Aventure  
- **5 zones** avec difficulté croissante
- **Chasse optionnelle** : Rencontrez des slimes pour les tuer ou capturer
- **Combats en vagues** : Affrontez les habitants de chaque zone
- **Boss de zone** : Vainquez le boss pour passer à la zone suivante
- **Objectif** : Terminer toutes les zones et devenir champion !

### ⚔️ Mode Survie
- **Arène infinie** : Vagues sans fin de plus en plus difficiles
- **Progression de difficulté** : Chaque vague augmente la difficulté
- **Pas de sauvegarde** : Un run = une tentative, tu perds = c'est fini
- **Score** : Combien de vagues peux-tu survivre ?

## 🎯 Mécanique de Base

### 🔍 Chasse aux Slimes
Lors d'une chasse, tu rencontres un slime aléatoire. Tu as trois choix :
- **Attaquer (A)** : Tue le slime → XP + Or
- **Capturer (C)** : Tente de capturer (probabilité selon la rareté)
- **Fuir (F)** : S'enfuit sans gain

### ⚡ Combat
- Ton slime affronte une série d'ennemis
- Chaque tour : Tu attaques, l'ennemi riposte automatiquement
- Dégâts basés sur ATK/DEF + variation aléatoire ±2
- Vague gagnée = Reçois XP + Or, passe à l'ennemi suivant

### 📈 Progression
- **XP** : Reçu après chaque action (chasse/combat)
- **Niveaux** : Gagne XP pour passer des niveaux (coût augmente)
- **Or** : Récompense de combat
- **Roster** : Ta collection de slimes capturés

## 🐛 Les 9 Slimes

| Emoji | Nom | Rareté | Zone |
|-------|-----|--------|------|
| 🟢 | Gelée Commune | Commun | 1 |
| 🔵 | Blob Bleu | Commun | 1 |
| 🟣 | Essence Pourpre | Rare | 2 |
| 💎 | Cristal Rose | Rare | 2 |
| 🟡 | Gélatine d'Or | Épique | 3 |
| ⚫ | Blob Ombre | Épique | 3 |
| 🔴 | Masse Écarlate | Légendaire | 4 |
| ⚪ | Prisme Blanc | Légendaire | 4 |
| 🖤 | Abysse Primordiale | Mythique | 5 |

## 🚀 Lancement

```bash
python3 main.py
```

**Contrôles** :
- Menu principal : `(J)ouer (Q)uitter`
- Mode : `(1)Aventure (2)Survie`
- Zone : `(C)ombattre (H)unter (F)uir`
- Combat/Chasse : `(A)ttaquer (C)apturer (F)uir (S)uivant`
