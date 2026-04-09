# cowboy-maze

Cowboy Maze — Happy Pixelz
Version : 1.2.0
Python : 3.8+
Licence : GNU General Public License v3.0 (GPL-3.0)

Cowboy Maze est un jeu d'arcade rétro en mode texte (CLI) développé en Python. Incarnez un cowboy solitaire dans un monde post-apocalyptique infesté de zombies. Votre mission : traverser des labyrinthes dangereux pour sauver l'humanité... ou au moins votre peau.

"Il était une fois dans le futur d'un autre monde, la fin du monde..." — Extrait des crédits du jeu.

Fonctionnalités
Mode Histoire : 5 niveaux originaux avec une difficulté croissante (Plaine, Canyon, Enfer, Prison, L'Étroit).

Éditeur de Niveau : Créez vos propres maps et générez des codes de partage.

Mode Custom : Jouez aux niveaux créés par la communauté via des codes d'importation.

Boutique d'Âmes : Dépensez vos points pour personnaliser l'apparence du jeu (Skins pour le joueur, les murs et le sol).

Système Anti-Triche : Système de vérification par variable miroir pour détecter les modifications non autorisées du score.

IA de Zombies : Méfiez-vous des zombies enragés (@) qui vous traquent activement.

Comment Jouer
Commandes
ZQSD / Flèches : Se déplacer.

A : Tirer une balle (50% de chance de réussite, une seule fois par niveau).

P : Retourner au menu principal.

Entrée : Valider les menus.

Objectif
Atteignez la sortie située en bas à droite de la carte (9, 4) sans perdre toutes vos vies.

Installation et Lancement
Option 1 : Pour les développeurs (Source Python)
Prérequis : Avoir Python 3 installé.

Cloner le projet :
git clone https://github.com/zedka450/cowboy-maze.git
cd cowboy-maze

Lancer le jeu :
python "Cowboy Maze.py"

Option 2 : Pour les joueurs (Exécutable Windows)
Allez dans l'onglet Releases de ce dépôt GitHub.

Téléchargez la dernière version du fichier Cowboy Maze.exe.

Lancez directement l'exécutable pour jouer (aucune installation de Python requise).

Structure des fichiers
Cowboy Maze.py : Le moteur de jeu principal et l'interface.

save.json : Votre sauvegarde (score, inventaire, skins).


Sécurité (Anti-Cheat)
Le jeu intègre un système de contrôle de cohérence. Toute modification manuelle du score dans save.json sans mettre à jour la variable de contrôle interne entraînera une réinitialisation du score par le système de sécurité.

Crédits
Développeur : ZedKa450

Studio : Happy Pixelz (Studioz Development)

Inspirations : Cortex, Hey Bobby!, Minecraft.

