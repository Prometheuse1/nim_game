# =============================================
#  settings.py - Configuration du jeu de Nim
# =============================================

# Titre de la fenetre
TITRE = "Jeu de Nim - IA & Statistiques"

# Dimensions de la fenetre principale
LARGEUR_FENETRE = 900
HAUTEUR_FENETRE = 650

# Couleurs (format Tkinter)
COULEUR_FOND        = "#1a1a2e"
COULEUR_PANNEAU     = "#16213e"
COULEUR_ACCENT      = "#0f3460"
COULEUR_BOUTON      = "#e94560"
COULEUR_BOUTON_HOVER= "#c73652"
COULEUR_TEXTE       = "#eaeaea"
COULEUR_TEXTE_ALT   = "#a8a8b3"
COULEUR_PILE        = "#f5a623"
COULEUR_PILE_SEL    = "#ff6b35"
COULEUR_SUCCES      = "#4caf50"
COULEUR_ERREUR      = "#f44336"
COULEUR_OR          = "#ffd700"
COULEUR_ARGENT      = "#c0c0c0"
COULEUR_BRONZE      = "#cd7f32"

# Polices
POLICE_TITRE   = ("Helvetica", 22, "bold")
POLICE_SOUS    = ("Helvetica", 14, "bold")
POLICE_NORMAL  = ("Helvetica", 11)
POLICE_SMALL   = ("Helvetica", 9)
POLICE_MONO    = ("Courier", 11)

# Configuration par defaut des piles
PILES_DEFAUT = [3, 5, 7]

# Niveaux de difficulte de l'IA
NIVEAUX_IA = {
    1: "Débutant",
    2: "Intermédiaire",
    3: "Avancé (Minimax)",
    4: "Expert (NimSum)"
}




# Profondeur maximale du Minimax
MINIMAX_PROFONDEUR = 6
