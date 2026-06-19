TITRE="Jeu de Nim - IA & Statistiques"

LARGEUR_FENETRE=900
HAUTEUR_FENETRE=650

C_FOND="#1a1a2e"
C_PANNEAU="#16213e"
C_ACCENT="#0f3460"
C_BOUTON="#e94560"
C_BTN_HOVER="#c73652"
C_TEXTE="#eaeaea"
C_TEXTE_ALT="#a8a8b3"
C_PILE="#f5a623"
C_PILE_SEL="#ff6b35"
C_SUCCES="#4caf50"
C_ERREUR="#f44336"
C_OR="#ffd700"
C_ARGENT="#c0c0c0"
C_BRONZE="#cd7f32"
C_BORDURE="#0f3460"
C_HIGHLIGHT="#e94560"


F_TITRE=("Helvetica",22,"bold")
F_SOUS=("Helvetica",14,"bold")
F_NORMAL=("Helvetica",11)
F_SMALL=("Helvetica",9)
F_MONO=("Courier",11)
F_BIG=("Helvetica",28,"bold")
F_ICON=("Helvetica",18,"bold")

J_ID            =0
J_NOM           =1
J_DATE_CREATION =2
J_SCORE_TOTAL   =3
J_VICTOIRES     =4
J_DEFAITES      =5

P_ID            =0
P_JOUEUR1_ID    =1
P_JOUEUR2_ID    =2
P_MODE_JEU      =3
P_NIVEAU_IA     =4
P_PILES         =5
P_GAGNANT_ID    =6
P_PERDANT_ID    =7
P_DATE_PARTIE   =8
P_DUREE_SECONDES=9
P_NB_COUPS      =10

PILES_DEFAUT=[3,5,7]

NIVEAUX_IA={
    1:"Débutant",
    2:"Intermédiaire",
    3:"Avancé (Minimax)",
    4:"Expert (NimSum)"
}
MINIMAX_PROFONDEUR=6
