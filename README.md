# 🎯 Jeu de Nim - Intelligence Artificielle & Statistiques

## Prérequis
- Python 3.8+
- Tkinter (inclus avec Python)
- SQLite3 (inclus avec Python)

**Aucune installation supplémentaire nécessaire !**

## Lancer le jeu
```bash
python main.py
```

## Structure du projet
```
nim_game/
├── main.py        # Interface graphique (Tkinter) + logique principale
├── player.py      # Gestion des joueurs
├── enemy.py       # Intelligence Artificielle (4 niveaux)
├── database.py    # Base de données SQLite
├── settings.py    # Configuration et constantes
└── nim_game.db    # Base de données (créée automatiquement)
```

## Fonctionnalités
- Création/connexion de profils joueurs
- Mode Joueur vs Joueur
- Mode Joueur vs IA (4 niveaux de difficulté)
- Base de données SQLite (parties, statistiques)
- Tableau de bord statistique
- Classement des joueurs

## Niveaux de l'IA
| Niveau | Nom        | Stratégie                          |
|--------|------------|------------------------------------|
| 1      | Débutant   | Coups aléatoires                   |
| 2      | Intermédiaire | Heuristiques simples            |
| 3      | Avancé     | Algorithme Minimax                 |
| 4      | Expert     | NimSum (XOR) - pratiquement imbattable |
