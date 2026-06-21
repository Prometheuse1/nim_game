TITRE="Jeu de Nim - IA & Statistiques"

LARGEUR_FENETRE=900
HAUTEUR_FENETRE=650

C_FOND="#11121c"
C_PANNEAU="#1a1d2e"
C_ACCENT="#242842"
C_SURVOL="#2e3354"
C_BORDURE="#2a2e4a"
C_BOUTON="#ef4565"
C_BTN_HOVER="#d4314f"
C_BOUTON_TEXTE="#ffffff"
C_TEXTE="#f1f1f6"
C_TEXTE_ALT="#9a9db3"
C_TEXTE_DIM="#6b6e87"
C_PILE="#f5a623"
C_PILE_SEL="#ff7a45"
C_SUCCES="#3ddc84"
C_ERREUR="#ff5470"
C_OR="#ffd54a"
C_ARGENT="#d6d9e3"
C_BRONZE="#d98a4f"
C_HIGHLIGHT="#ef4565"
C_NIV1="#3ddc84"
C_NIV2="#4fb8e8"
C_NIV3="#ef4565"
C_NIV4="#ffd54a"

F_TITRE=("Helvetica",24,"bold")
F_SOUS=("Helvetica",13,"bold")
F_NORMAL=("Helvetica",11)
F_SMALL=("Helvetica",9)
F_MONO=("Courier",11)
F_BIG=("Helvetica",30,"bold")
F_ICON=("Helvetica",18,"bold")

ESP_XS=4
ESP_S=8
ESP_M=16
ESP_L=24
ESP_XL=40

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