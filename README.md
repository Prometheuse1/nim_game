# 🎯 Jeu de Nim - Intelligence Artificielle & Statistiques

## Prérequis
- Python 3.8+
- Tkinter (inclus avec Python)
- Un serveur **MySQL** local (ex. via XAMPP, MAMP ou `mysql-server`)
- Le paquet Python `pymysql`

### Installation des dépendances
```bash
pip install pymysql
```

### Configuration de la base de données
1. Démarrez votre serveur MySQL local sur `localhost:3306`.
2. Créez la base de données :
   ```sql
   CREATE DATABASE nim_game;
   ```
3. Les tables (`joueurs`, `parties`) sont créées automatiquement au lancement du jeu.

> ⚠️ Par défaut, la connexion utilise l'utilisateur `root` sans mot de passe (voir `database.py`). Adaptez ces identifiants à votre configuration locale si nécessaire.

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
├── database.py    # Connexion et requêtes MySQL (pymysql)
├── settings.py    # Configuration, constantes et couleurs de l'interface
└── README.md
```

## Fonctionnalités
- Création/connexion de profils joueurs
- Mode Joueur vs Joueur
- Mode Joueur vs IA (4 niveaux de difficulté)
- Base de données MySQL (joueurs, historique des parties)
- Page de résultat de partie (durée, nombre de coups, vainqueur)
- Tableau de bord statistique global
- Statistiques détaillées par joueur (taux de victoire, historique)
- Classement des joueurs

## Niveaux de l'IA
| Niveau | Nom            | Stratégie                              |
|--------|----------------|-----------------------------------------|
| 1      | Débutant       | Coups aléatoires                       |
| 2      | Intermédiaire  | Heuristiques simples                   |
| 3      | Avancé         | Algorithme Minimax                     |
| 4      | Expert         | NimSum (XOR) - pratiquement imbattable |
