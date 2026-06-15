# =============================================
#  main.py - Application principale Jeu de Nim
# =============================================

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import time
import threading

import database as db
import player as pl
import enemy as en
from settings import *
from player import (
    J_ID, J_NOM, J_DATE_CREATION, J_SCORE_TOTAL, J_VICTOIRES, J_DEFAITES, J_NULS,
    P_ID, P_JOUEUR1_ID, P_JOUEUR2_ID, P_MODE_JEU, P_NIVEAU_IA, P_PILES,
    P_GAGNANT_ID, P_PERDANT_ID, P_DATE_PARTIE, P_DUREE_SECONDES, P_NB_COUPS,
)


# ================================================
#  Utilitaires visuels
# ================================================

def bouton_style(btn, couleur=COULEUR_BOUTON, texte=COULEUR_TEXTE):
    """Applique un style uniforme aux boutons."""
    btn.config(
        bg=couleur, fg=texte,
        activebackground=COULEUR_BOUTON_HOVER, activeforeground=texte,
        relief="flat", cursor="hand2",
        font=POLICE_NORMAL, padx=12, pady=6
    )


def label_titre(parent, texte, couleur=COULEUR_TEXTE, police=POLICE_TITRE):
    lbl = tk.Label(parent, text=texte, bg=COULEUR_PANNEAU,
                   fg=couleur, font=police)
    return lbl


def frame_carte(parent, **kw):
    """Frame avec style 'carte'."""
    f = tk.Frame(parent, bg=COULEUR_ACCENT,
                 highlightbackground=COULEUR_BOUTON,
                 highlightthickness=1, **kw)
    return f


# ================================================
#  ECRAN D'ACCUEIL
# ================================================

class EcranAccueil:
    def __init__(self, app):
        self.app = app
        self.frame = tk.Frame(app.root, bg=COULEUR_FOND)
        self._construire()

    def _construire(self):
        f = self.frame

        # En-tete
        tk.Label(f, text="🎯 JEU DE NIM", bg=COULEUR_FOND,
                 fg=COULEUR_OR, font=("Helvetica", 32, "bold")).pack(pady=(40, 5))
        tk.Label(f, text="Intelligence Artificielle & Statistiques",
                 bg=COULEUR_FOND, fg=COULEUR_TEXTE_ALT,
                 font=POLICE_SOUS).pack(pady=(0, 30))

        # Zone centrale
        centre = tk.Frame(f, bg=COULEUR_FOND)
        centre.pack(expand=True)

        # Selectionner joueur
        carte = frame_carte(centre, padx=30, pady=20)
        carte.pack(padx=20, pady=10, fill="x")

        tk.Label(carte, text="👤 Connexion joueur", bg=COULEUR_ACCENT,
                 fg=COULEUR_OR, font=POLICE_SOUS).pack(anchor="w", pady=(0, 10))

        row = tk.Frame(carte, bg=COULEUR_ACCENT)
        row.pack(fill="x")

        tk.Label(row, text="Pseudo :", bg=COULEUR_ACCENT,
                 fg=COULEUR_TEXTE, font=POLICE_NORMAL).pack(side="left")

        self.entry_nom = tk.Entry(row, font=POLICE_NORMAL, width=18,
                                  bg=COULEUR_FOND, fg=COULEUR_TEXTE,
                                  insertbackground=COULEUR_TEXTE,
                                  relief="flat")
        self.entry_nom.pack(side="left", padx=8)

        btn_conn = tk.Button(row, text="Connexion",
                             command=self._connexion)
        bouton_style(btn_conn)
        btn_conn.pack(side="left", padx=4)

        btn_creer = tk.Button(row, text="Créer profil",
                              command=self._creer_profil)
        bouton_style(btn_creer, couleur=COULEUR_SUCCES)
        btn_creer.pack(side="left", padx=4)

        # Liste joueurs
        tk.Label(carte, text="Joueurs existants (double-clic pour connexion) :",
                 bg=COULEUR_ACCENT, fg=COULEUR_TEXTE_ALT,
                 font=POLICE_SMALL).pack(anchor="w", pady=(12, 2))

        self.liste_joueurs = tk.Listbox(carte, bg=COULEUR_FOND, fg=COULEUR_TEXTE,
                                        font=POLICE_NORMAL, height=5,
                                        selectbackground=COULEUR_BOUTON,
                                        relief="flat")
        self.liste_joueurs.pack(fill="x", pady=(0, 4))
        self.liste_joueurs.bind("<Double-Button-1>", self._connexion_liste)

        self._rafraichir_liste()

        # Bouton statistiques globales
        btn_stats = tk.Button(f, text="📊 Statistiques globales",
                              command=self.app.afficher_stats_globales)
        bouton_style(btn_stats, couleur=COULEUR_ACCENT)
        btn_stats.pack(pady=8)

        # Info joueur connecte
        self.lbl_connecte = tk.Label(f, text="", bg=COULEUR_FOND,
                                     fg=COULEUR_SUCCES, font=POLICE_SOUS)
        self.lbl_connecte.pack(pady=4)

        if self.app.joueur_actif:
            self._afficher_connecte()

    def _rafraichir_liste(self):
        self.liste_joueurs.delete(0, tk.END)
        for j in pl.liste_joueurs():
            self.liste_joueurs.insert(
                tk.END,
                f"  {j[J_NOM]}  |  🏆 {j[J_VICTOIRES]}V  {j[J_DEFAITES]}D  |  ⭐ {j[J_SCORE_TOTAL]} pts"
            )
        self._joueurs = pl.liste_joueurs()

    def _connexion(self):
        nom = self.entry_nom.get().strip()
        ok, resultat = pl.selectionner_joueur(nom)
        if ok:
            self.app.joueur_actif = resultat
            self._afficher_connecte()
        else:
            messagebox.showerror("Erreur", resultat)

    def _connexion_liste(self, event):
        idx = self.liste_joueurs.curselection()
        if not idx:
            return
        joueur = self._joueurs[idx[0]]
        self.app.joueur_actif = joueur
        self.entry_nom.delete(0, tk.END)
        self.entry_nom.insert(0, joueur[J_NOM])
        self._afficher_connecte()

    def _creer_profil(self):
        nom = self.entry_nom.get().strip()
        ok, resultat = pl.creer_profil(nom)
        if ok:
            self.app.joueur_actif = resultat
            self._rafraichir_liste()
            self._afficher_connecte()
            messagebox.showinfo("Profil créé",
                                f"Bienvenue {resultat[J_NOM]} ! Profil créé avec succès.")
        else:
            messagebox.showerror("Erreur", resultat)

    def _afficher_connecte(self):
        j = self.app.joueur_actif
        self.lbl_connecte.config(
            text=f"✅ Connecté : {j[J_NOM]}  |  ⭐ {j[J_SCORE_TOTAL]} pts  |  "
                 f"🏆 {j[J_VICTOIRES]}V / {j[J_DEFAITES]}D")
        self.app.afficher_menu_principal()

    def afficher(self):
        self.frame.pack(fill="both", expand=True)

    def cacher(self):
        self.frame.pack_forget()


# ================================================
#  MENU PRINCIPAL
# ================================================

class MenuPrincipal:
    def __init__(self, app):
        self.app = app
        self.frame = tk.Frame(app.root, bg=COULEUR_FOND)
        self._construire()

    def _construire(self):
        f = self.frame

        self.lbl_bienvenue = tk.Label(f, text="", bg=COULEUR_FOND,
                                      fg=COULEUR_OR, font=POLICE_TITRE)
        self.lbl_bienvenue.pack(pady=(30, 5))

        tk.Label(f, text="Que souhaitez-vous faire ?",
                 bg=COULEUR_FOND, fg=COULEUR_TEXTE_ALT,
                 font=POLICE_SOUS).pack(pady=(0, 20))

        centre = tk.Frame(f, bg=COULEUR_FOND)
        centre.pack(expand=True)

        boutons = [
            ("⚔️  Joueur vs Joueur",    COULEUR_BOUTON,  self.app.lancer_jcj),
            ("🤖  Joueur vs IA",         "#7c4dff",       self.app.lancer_jcia),
            ("👤  Mon profil",           COULEUR_ACCENT,  self.app.afficher_profil),
            ("📊  Statistiques",         "#00897b",       self.app.afficher_stats_globales),
            ("🔓  Changer de joueur",    "#546e7a",       self.app.deconnecter),
        ]

        for texte, couleur, cmd in boutons:
            btn = tk.Button(centre, text=texte, command=cmd, width=28)
            bouton_style(btn, couleur=couleur)
            btn.pack(pady=6)

    def mettre_a_jour(self):
        if self.app.joueur_actif:
            self.lbl_bienvenue.config(
                text=f"Bonjour, {self.app.joueur_actif[J_NOM]} ! 👋")

    def afficher(self):
        self.mettre_a_jour()
        self.frame.pack(fill="both", expand=True)

    def cacher(self):
        self.frame.pack_forget()


# ================================================
#  ECRAN DE CONFIGURATION DE PARTIE
# ================================================

class EcranConfig:
    """Permet de configurer le mode et les piles avant de jouer."""

    def __init__(self, app, mode):
        self.app = app
        self.mode = mode  # 'JcJ' ou 'JcIA'
        self.frame = tk.Frame(app.root, bg=COULEUR_FOND)
        self.niveau_ia = tk.IntVar(value=1)
        self.joueur2_id = None
        self._construire()

    def _construire(self):
        f = self.frame
        titre = "⚔️ Joueur vs Joueur" if self.mode == "JcJ" else "🤖 Joueur vs IA"

        label_titre(f, titre, COULEUR_OR).pack(pady=(25, 5))

        # ----- Config piles -----
        carte_piles = frame_carte(f, padx=20, pady=15)
        carte_piles.pack(padx=30, pady=10, fill="x")

        tk.Label(carte_piles, text="Configuration des piles",
                 bg=COULEUR_ACCENT, fg=COULEUR_TEXTE, font=POLICE_SOUS).pack(anchor="w")
        tk.Label(carte_piles,
                 text="Entrez les tailles séparées par des virgules (ex: 3,5,7)",
                 bg=COULEUR_ACCENT, fg=COULEUR_TEXTE_ALT, font=POLICE_SMALL).pack(anchor="w")

        self.entry_piles = tk.Entry(carte_piles, font=POLICE_MONO, width=20,
                                    bg=COULEUR_FOND, fg=COULEUR_OR,
                                    insertbackground=COULEUR_OR, relief="flat")
        self.entry_piles.insert(0, ",".join(str(p) for p in PILES_DEFAUT))
        self.entry_piles.pack(anchor="w", pady=6)

        row_piles = tk.Frame(carte_piles, bg=COULEUR_ACCENT)
        row_piles.pack(anchor="w")
        presets = [("3,5,7", "Classique"), ("1,3,5,7", "4 piles"), ("5,5,5", "Symétrique")]
        for val, nom in presets:
            tk.Button(row_piles, text=nom,
                      command=lambda v=val: self._preset(v),
                      font=POLICE_SMALL, bg=COULEUR_FOND,
                      fg=COULEUR_TEXTE, relief="flat",
                      padx=6, pady=2).pack(side="left", padx=3)

        # ----- Mode JcJ : choisir joueur 2 -----
        if self.mode == "JcJ":
            carte_j2 = frame_carte(f, padx=20, pady=15)
            carte_j2.pack(padx=30, pady=5, fill="x")

            tk.Label(carte_j2, text="Joueur 2", bg=COULEUR_ACCENT,
                     fg=COULEUR_TEXTE, font=POLICE_SOUS).pack(anchor="w")

            row = tk.Frame(carte_j2, bg=COULEUR_ACCENT)
            row.pack(anchor="w", pady=5)
            tk.Label(row, text="Pseudo :", bg=COULEUR_ACCENT,
                     fg=COULEUR_TEXTE, font=POLICE_NORMAL).pack(side="left")
            self.entry_j2 = tk.Entry(row, font=POLICE_NORMAL, width=16,
                                     bg=COULEUR_FOND, fg=COULEUR_TEXTE,
                                     insertbackground=COULEUR_TEXTE, relief="flat")
            self.entry_j2.pack(side="left", padx=8)

        # ----- Mode JcIA : choisir niveau -----
        if self.mode == "JcIA":
            carte_ia = frame_carte(f, padx=20, pady=15)
            carte_ia.pack(padx=30, pady=5, fill="x")

            tk.Label(carte_ia, text="Niveau de l'IA",
                     bg=COULEUR_ACCENT, fg=COULEUR_TEXTE, font=POLICE_SOUS).pack(anchor="w")

            for niv, nom in NIVEAUX_IA.items():
                tk.Radiobutton(carte_ia, text=f"  Niveau {niv} : {nom}",
                               variable=self.niveau_ia, value=niv,
                               bg=COULEUR_ACCENT, fg=COULEUR_TEXTE,
                               selectcolor=COULEUR_FOND,
                               activebackground=COULEUR_ACCENT,
                               font=POLICE_NORMAL).pack(anchor="w", pady=2)

        # ----- Boutons -----
        row_btn = tk.Frame(f, bg=COULEUR_FOND)
        row_btn.pack(pady=15)

        btn_jouer = tk.Button(row_btn, text="🎮 Jouer !", command=self._lancer)
        bouton_style(btn_jouer, couleur=COULEUR_SUCCES)
        btn_jouer.pack(side="left", padx=10)

        btn_retour = tk.Button(row_btn, text="← Retour",
                               command=self.app.afficher_menu_principal)
        bouton_style(btn_retour, couleur=COULEUR_ACCENT)
        btn_retour.pack(side="left", padx=10)

    def _preset(self, valeur):
        self.entry_piles.delete(0, tk.END)
        self.entry_piles.insert(0, valeur)

    def _lancer(self):
        # Valider les piles
        try:
            piles = [int(x.strip()) for x in self.entry_piles.get().split(",")]
            if not piles or any(p <= 0 for p in piles) or len(piles) > 8:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur",
                "Piles invalides. Entrez des nombres positifs séparés par des virgules.")
            return

        joueur2 = None
        if self.mode == "JcJ":
            nom_j2 = self.entry_j2.get().strip()
            if not nom_j2:
                messagebox.showerror("Erreur", "Entrez le pseudo du joueur 2.")
                return
            ok, res = pl.selectionner_joueur(nom_j2)
            if not ok:
                if messagebox.askyesno("Joueur inconnu",
                    f"'{nom_j2}' n'existe pas. Créer ce profil ?"):
                    ok, res = pl.creer_profil(nom_j2)
                    if not ok:
                        messagebox.showerror("Erreur", res)
                        return
                else:
                    return
            joueur2 = res
            if joueur2[J_ID] == self.app.joueur_actif[J_ID]:
                messagebox.showerror("Erreur", "Les deux joueurs doivent être différents.")
                return

        niveau = self.niveau_ia.get() if self.mode == "JcIA" else 0

        self.app.lancer_partie(piles, self.mode, joueur2, niveau)

    def afficher(self):
        self.frame.pack(fill="both", expand=True)

    def cacher(self):
        self.frame.pack_forget()


# ================================================
#  ECRAN DE JEU
# ================================================

class EcranJeu:
    TAILLE_OBJET = 26  # hauteur en pixels de chaque objet dans la pile

    def __init__(self, app, piles, mode, joueur2, niveau_ia):
        self.app = app
        self.piles = list(piles)
        self.piles_initiales = list(piles)
        self.mode = mode
        self.joueur1 = app.joueur_actif
        self.joueur2 = joueur2  # tuple ou None (IA)
        self.niveau_ia = niveau_ia
        self.tour_joueur1 = True  # True = J1, False = J2/IA
        self.pile_selectionnee = None
        self.nb_retrait = tk.IntVar(value=1)
        self.debut_temps = time.time()
        self.nb_coups = 0
        self.partie_terminee = False

        self.frame = tk.Frame(app.root, bg=COULEUR_FOND)
        self._construire()

    # ----- Construction de l'interface -----

    def _construire(self):
        f = self.frame

        # En-tete
        self.lbl_titre = tk.Label(f, text="", bg=COULEUR_FOND,
                                  fg=COULEUR_OR, font=POLICE_TITRE)
        self.lbl_titre.pack(pady=(15, 2))

        self.lbl_tour = tk.Label(f, text="", bg=COULEUR_FOND,
                                 fg=COULEUR_TEXTE, font=POLICE_SOUS)
        self.lbl_tour.pack(pady=(0, 10))

        # Zone des piles (canvas)
        self.canvas_frame = tk.Frame(f, bg=COULEUR_PANNEAU,
                                     highlightbackground=COULEUR_ACCENT,
                                     highlightthickness=2)
        self.canvas_frame.pack(padx=20, pady=5, fill="x")

        self.canvas = tk.Canvas(self.canvas_frame, bg=COULEUR_PANNEAU,
                                height=240, highlightthickness=0)
        self.canvas.pack(fill="x", pady=10, padx=10)
        self.canvas.bind("<Button-1>", self._clic_canvas)

        # Zone de controle
        ctrl = frame_carte(f, padx=20, pady=12)
        ctrl.pack(padx=20, pady=8, fill="x")

        tk.Label(ctrl, text="Pile sélectionnée :",
                 bg=COULEUR_ACCENT, fg=COULEUR_TEXTE_ALT,
                 font=POLICE_NORMAL).grid(row=0, column=0, sticky="w")

        self.lbl_pile_sel = tk.Label(ctrl, text="Aucune",
                                     bg=COULEUR_ACCENT, fg=COULEUR_PILE_SEL,
                                     font=POLICE_SOUS)
        self.lbl_pile_sel.grid(row=0, column=1, padx=15)

        tk.Label(ctrl, text="Nombre à retirer :",
                 bg=COULEUR_ACCENT, fg=COULEUR_TEXTE_ALT,
                 font=POLICE_NORMAL).grid(row=1, column=0, sticky="w", pady=5)

        self.spin_retrait = tk.Spinbox(ctrl, from_=1, to=1,
                                       textvariable=self.nb_retrait,
                                       width=6, font=POLICE_NORMAL,
                                       bg=COULEUR_FOND, fg=COULEUR_OR,
                                       buttonbackground=COULEUR_ACCENT,
                                       relief="flat")
        self.spin_retrait.grid(row=1, column=1, padx=15)

        self.btn_jouer = tk.Button(ctrl, text="✅ Jouer ce coup",
                                   command=self._jouer_coup)
        bouton_style(self.btn_jouer, couleur=COULEUR_SUCCES)
        self.btn_jouer.grid(row=0, column=2, rowspan=2, padx=15)

        # Message d'erreur / info
        self.lbl_message = tk.Label(f, text="", bg=COULEUR_FOND,
                                    fg=COULEUR_ERREUR, font=POLICE_NORMAL)
        self.lbl_message.pack(pady=3)

        # Infos en bas
        info = tk.Frame(f, bg=COULEUR_FOND)
        info.pack(pady=5)

        self.lbl_j1_info = tk.Label(info, text="", bg=COULEUR_FOND,
                                    fg=COULEUR_TEXTE_ALT, font=POLICE_SMALL)
        self.lbl_j1_info.pack(side="left", padx=20)

        self.lbl_j2_info = tk.Label(info, text="", bg=COULEUR_FOND,
                                    fg=COULEUR_TEXTE_ALT, font=POLICE_SMALL)
        self.lbl_j2_info.pack(side="left", padx=20)

        # Bouton quitter
        btn_quit = tk.Button(f, text="🏠 Quitter la partie",
                             command=self._quitter)
        bouton_style(btn_quit, couleur="#546e7a")
        btn_quit.pack(pady=8)

        self._mettre_a_jour_affichage()

    # ----- Dessin des piles -----

    def _dessiner_piles(self):
        self.canvas.delete("all")
        n = len(self.piles)
        largeur = self.canvas.winfo_width() or 800
        largeur_pile = largeur // (n + 1)
        hauteur = 220

        self._zones_piles = []

        for i, taille in enumerate(self.piles):
            x_centre = int(largeur_pile * (i + 0.8))
            couleur = COULEUR_PILE_SEL if i == self.pile_selectionnee else COULEUR_PILE

            x1 = x_centre - 30
            x2 = x_centre + 30
            self._zones_piles.append((x1, x2, i))

            for j in range(taille):
                y_bas = hauteur - 10 - j * (self.TAILLE_OBJET + 3)
                y_haut = y_bas - self.TAILLE_OBJET
                self.canvas.create_rectangle(
                    x_centre - 20, y_haut,
                    x_centre + 20, y_bas,
                    fill=couleur, outline=COULEUR_FOND, width=2
                )

            self.canvas.create_text(
                x_centre, hauteur + 5,
                text=f"Pile {i + 1}\n({taille})",
                fill=COULEUR_TEXTE, font=POLICE_SMALL,
                anchor="n"
            )

            if i == self.pile_selectionnee:
                self.canvas.create_text(
                    x_centre, 10,
                    text="▼ Sélectionnée",
                    fill=COULEUR_PILE_SEL, font=POLICE_SMALL,
                    anchor="n"
                )

    def _clic_canvas(self, event):
        if self.partie_terminee:
            return
        if self.mode == "JcIA" and not self.tour_joueur1:
            return

        x = event.x
        for x1, x2, i in self._zones_piles:
            if x1 <= x <= x2 and self.piles[i] > 0:
                self.pile_selectionnee = i
                self.spin_retrait.config(to=self.piles[i])
                if self.nb_retrait.get() > self.piles[i]:
                    self.nb_retrait.set(1)
                self.lbl_pile_sel.config(text=f"Pile {i + 1} ({self.piles[i]} objets)")
                self._dessiner_piles()
                self.lbl_message.config(text="")
                return

    # ----- Logique de jeu -----

    def _mettre_a_jour_affichage(self):
        nom_j1 = self.joueur1[J_NOM]
        if self.mode == "JcJ":
            nom_j2 = self.joueur2[J_NOM]
        else:
            nom_j2 = f"IA Niveau {self.niveau_ia} ({NIVEAUX_IA[self.niveau_ia]})"

        self.lbl_titre.config(text=f"{nom_j1}  ⚔️  {nom_j2}")

        if self.tour_joueur1:
            self.lbl_tour.config(
                text=f"🎯 Tour de : {nom_j1}", fg=COULEUR_PILE)
        else:
            self.lbl_tour.config(
                text=f"🎯 Tour de : {nom_j2}",
                fg=COULEUR_PILE_SEL if self.mode == "JcJ" else "#7c4dff")

        self.lbl_j1_info.config(
            text=f"{nom_j1} | ⭐{self.joueur1[J_SCORE_TOTAL]} pts | 🏆{self.joueur1[J_VICTOIRES]}V")

        if self.joueur2:
            self.lbl_j2_info.config(
                text=f"{nom_j2} | ⭐{self.joueur2[J_SCORE_TOTAL]} pts | 🏆{self.joueur2[J_VICTOIRES]}V")
        else:
            self.lbl_j2_info.config(text=nom_j2)

        self.frame.after(50, self._dessiner_piles)

    def _jouer_coup(self):
        if self.partie_terminee:
            return
        if self.pile_selectionnee is None:
            self.lbl_message.config(text="⚠️ Cliquez sur une pile pour la sélectionner !")
            return

        try:
            nb = int(self.nb_retrait.get())
        except (ValueError, tk.TclError):
            nb = 1

        taille_pile = self.piles[self.pile_selectionnee]
        if nb < 1 or nb > taille_pile:
            self.lbl_message.config(
                text=f"⚠️ Retirez entre 1 et {taille_pile} objets.")
            return

        self._appliquer_coup(self.pile_selectionnee, nb)

    def _appliquer_coup(self, idx_pile, nb):
        self.piles[idx_pile] -= nb
        self.nb_coups += 1
        self.pile_selectionnee = None
        self.lbl_pile_sel.config(text="Aucune")
        self.nb_retrait.set(1)
        self.spin_retrait.config(to=1)
        self.lbl_message.config(text="")

        if all(p == 0 for p in self.piles):
            self._fin_partie()
            return

        self.tour_joueur1 = not self.tour_joueur1
        self._mettre_a_jour_affichage()

        if self.mode == "JcIA" and not self.tour_joueur1:
            self.lbl_message.config(text="🤖 L'IA réfléchit...", fg=COULEUR_TEXTE_ALT)
            self.btn_jouer.config(state="disabled")
            self.frame.after(800, self._tour_ia)

    def _tour_ia(self):
        idx, nb = en.jouer_ia(self.piles, self.niveau_ia)
        self.btn_jouer.config(state="normal")
        if idx is None:
            return
        self.lbl_message.config(
            text=f"🤖 L'IA retire {nb} objet(s) de la pile {idx + 1}", fg="#7c4dff")
        self._appliquer_coup(idx, nb)

    def _fin_partie(self):
        self.partie_terminee = True
        duree = int(time.time() - self.debut_temps)

        j1_a_gagne = self.tour_joueur1

        if self.mode == "JcIA":
            if j1_a_gagne:
                gagnant_nom = self.joueur1[J_NOM]
                gagnant_id = self.joueur1[J_ID]
                perdant_id = None
                pl.enregistrer_resultat(self.joueur1[J_ID], victoire=True)
                msg_result = f"🎉 Félicitations {gagnant_nom}, vous avez battu l'IA !"
                couleur_msg = COULEUR_SUCCES
            else:
                gagnant_nom = f"IA Niveau {self.niveau_ia}"
                gagnant_id = None
                perdant_id = self.joueur1[J_ID]
                pl.enregistrer_resultat(self.joueur1[J_ID], victoire=False)
                msg_result = "😔 L'IA a gagné. Réessayez !"
                couleur_msg = COULEUR_ERREUR

            db.enregistrer_partie(
                joueur1_id=self.joueur1[J_ID],
                joueur2_id=None,
                mode_jeu="JcIA",
                niveau_ia=self.niveau_ia,
                piles_initiales=self.piles_initiales,
                gagnant_id=gagnant_id,
                perdant_id=perdant_id,
                duree_secondes=duree,
                nb_coups=self.nb_coups
            )

        else:  # JcJ
            if j1_a_gagne:
                gagnant = self.joueur1
                perdant = self.joueur2
            else:
                gagnant = self.joueur2
                perdant = self.joueur1

            pl.enregistrer_resultat(gagnant[J_ID], victoire=True)
            pl.enregistrer_resultat(perdant[J_ID], victoire=False)

            db.enregistrer_partie(
                joueur1_id=self.joueur1[J_ID],
                joueur2_id=self.joueur2[J_ID],
                mode_jeu="JcJ",
                niveau_ia=0,
                piles_initiales=self.piles_initiales,
                gagnant_id=gagnant[J_ID],
                perdant_id=perdant[J_ID],
                duree_secondes=duree,
                nb_coups=self.nb_coups
            )
            msg_result = f"🏆 {gagnant[J_NOM]} remporte la partie !"
            couleur_msg = COULEUR_OR

        # Mettre a jour le joueur actif en memoire
        self.app.joueur_actif = db.get_joueur_par_id(self.joueur1[J_ID])

        # Afficher resultat
        self._dessiner_piles()
        self.lbl_tour.config(text="")
        self.lbl_message.config(text=msg_result, fg=couleur_msg,
                                font=POLICE_SOUS)
        self.btn_jouer.config(state="disabled")

        self.frame.after(200, lambda: self._popup_fin(msg_result, duree))

    def _popup_fin(self, msg, duree):
        popup = tk.Toplevel(self.app.root)
        popup.title("Fin de partie")
        popup.configure(bg=COULEUR_FOND)
        popup.resizable(False, False)
        popup.transient(self.app.root)
        popup.grab_set()

        tk.Label(popup, text="🎯 Partie terminée !", bg=COULEUR_FOND,
                 fg=COULEUR_OR, font=POLICE_TITRE).pack(pady=(20, 5), padx=30)
        tk.Label(popup, text=msg, bg=COULEUR_FOND,
                 fg=COULEUR_TEXTE, font=POLICE_SOUS).pack(pady=5)
        tk.Label(popup, text=f"⏱ Durée : {duree}s  |  🎮 Coups joués : {self.nb_coups}",
                 bg=COULEUR_FOND, fg=COULEUR_TEXTE_ALT, font=POLICE_NORMAL).pack(pady=3)

        row = tk.Frame(popup, bg=COULEUR_FOND)
        row.pack(pady=15)

        def rejouer():
            popup.destroy()
            self.app.lancer_partie(
                self.piles_initiales, self.mode,
                self.joueur2, self.niveau_ia)

        btn_rejouer = tk.Button(row, text="🔄 Rejouer", command=rejouer)
        bouton_style(btn_rejouer, couleur=COULEUR_SUCCES)
        btn_rejouer.pack(side="left", padx=8)

        btn_menu = tk.Button(row, text="🏠 Menu principal",
                             command=lambda: [popup.destroy(), self.app.afficher_menu_principal()])
        bouton_style(btn_menu, couleur=COULEUR_ACCENT)
        btn_menu.pack(side="left", padx=8)

        popup.wait_window()

    def _quitter(self):
        if not self.partie_terminee:
            if not messagebox.askyesno("Quitter",
                    "Quitter la partie en cours ? Elle ne sera pas enregistrée."):
                return
        self.app.afficher_menu_principal()

    def afficher(self):
        self.frame.pack(fill="both", expand=True)
        self.frame.update()
        self._dessiner_piles()

    def cacher(self):
        self.frame.pack_forget()


# ================================================
#  ECRAN PROFIL JOUEUR
# ================================================

class EcranProfil:
    def __init__(self, app):
        self.app = app
        self.frame = tk.Frame(app.root, bg=COULEUR_FOND)

    def _construire(self):
        for w in self.frame.winfo_children():
            w.destroy()

        j = self.app.joueur_actif
        stats = pl.afficher_stats(j)
        f = self.frame

        label_titre(f, f"👤 Profil de {j[J_NOM]}", COULEUR_OR).pack(pady=(20, 5))

        # Statistiques
        carte = frame_carte(f, padx=25, pady=15)
        carte.pack(padx=30, pady=10, fill="x")

        tk.Label(carte, text="📈 Statistiques", bg=COULEUR_ACCENT,
                 fg=COULEUR_TEXTE, font=POLICE_SOUS).pack(anchor="w", pady=(0, 10))

        infos = [
            ("⭐ Score total",       stats["score"]),
            ("🏆 Victoires",         stats["victoires"]),
            ("💀 Défaites",          stats["defaites"]),
            ("🤝 Nuls",              stats["nuls"]),
            ("🎮 Parties jouées",    stats["total_parties"]),
            ("📊 Taux de victoire",  f"{stats['taux_victoire']} %"),
            ("📅 Membre depuis",     stats["date_creation"]),
        ]

        grille = tk.Frame(carte, bg=COULEUR_ACCENT)
        grille.pack(fill="x")
        for i, (label, val) in enumerate(infos):
            tk.Label(grille, text=label, bg=COULEUR_ACCENT,
                     fg=COULEUR_TEXTE_ALT, font=POLICE_NORMAL,
                     anchor="w").grid(row=i, column=0, sticky="w", padx=5, pady=2)
            tk.Label(grille, text=str(val), bg=COULEUR_ACCENT,
                     fg=COULEUR_OR, font=POLICE_NORMAL).grid(
                         row=i, column=1, sticky="w", padx=20)

        # Historique
        carte_h = frame_carte(f, padx=25, pady=15)
        carte_h.pack(padx=30, pady=5, fill="x")

        tk.Label(carte_h, text="📜 Historique des parties",
                 bg=COULEUR_ACCENT, fg=COULEUR_TEXTE, font=POLICE_SOUS).pack(anchor="w", pady=(0, 8))

        historique = pl.historique(j[J_ID], limite=10)
        if historique:
            entetes = ["Date", "Mode", "Adversaire", "Résultat", "Durée", "Coups"]
            colonnes_largeurs = [16, 5, 14, 8, 7, 6]
            ent_str = "  ".join(h.ljust(l) for h, l in zip(entetes, colonnes_largeurs))
            tk.Label(carte_h, text=ent_str, bg=COULEUR_ACCENT,
                     fg=COULEUR_TEXTE_ALT, font=POLICE_MONO).pack(anchor="w")

            for partie in historique:
                date = str(partie[P_DATE_PARTIE] or "")[:16]
                mode = partie[P_MODE_JEU]
                # parties.* = 11 cols (0-10), then j1.nom=11, j2.nom=12, jg.nom=13
                nom_j1 = partie[11] or "?"
                nom_j2 = partie[12] or "?"
                if mode == "JcIA":
                    adv = f"IA N{partie[P_NIVEAU_IA]}"
                elif partie[P_JOUEUR1_ID] == j[J_ID]:
                    adv = nom_j2
                else:
                    adv = nom_j1

                gagnant_id = partie[P_GAGNANT_ID]
                if gagnant_id == j[J_ID]:
                    res = "✅ Victoire"
                elif gagnant_id is None and mode == "JcIA":
                    res = "❌ Défaite"
                elif gagnant_id != j[J_ID] and gagnant_id is not None:
                    res = "❌ Défaite"
                else:
                    res = "🤝 Nul"

                duree = f"{partie[P_DUREE_SECONDES]}s"
                coups = str(partie[P_NB_COUPS])

                vals = [date, mode, adv, res, duree, coups]
                ligne = "  ".join(str(v).ljust(l) for v, l in zip(vals, colonnes_largeurs))
                tk.Label(carte_h, text=ligne, bg=COULEUR_ACCENT,
                         fg=COULEUR_TEXTE, font=POLICE_MONO).pack(anchor="w")
        else:
            tk.Label(carte_h, text="Aucune partie jouée pour le moment.",
                     bg=COULEUR_ACCENT, fg=COULEUR_TEXTE_ALT,
                     font=POLICE_NORMAL).pack()

        # Boutons
        row = tk.Frame(f, bg=COULEUR_FOND)
        row.pack(pady=12)

        btn_retour = tk.Button(row, text="← Retour",
                               command=self.app.afficher_menu_principal)
        bouton_style(btn_retour, couleur=COULEUR_ACCENT)
        btn_retour.pack(side="left", padx=8)

        btn_suppr = tk.Button(row, text="🗑 Supprimer mon profil",
                              command=self._supprimer)
        bouton_style(btn_suppr, couleur=COULEUR_ERREUR)
        btn_suppr.pack(side="left", padx=8)

    def _supprimer(self):
        nom = self.app.joueur_actif[J_NOM]
        if messagebox.askyesno("Confirmer",
                f"Supprimer définitivement le profil de {nom} et tout son historique ?"):
            pl.supprimer(self.app.joueur_actif[J_ID])
            self.app.joueur_actif = None
            messagebox.showinfo("Supprimé", f"Le profil '{nom}' a été supprimé.")
            self.app.deconnecter()

    def afficher(self):
        self._construire()
        self.frame.pack(fill="both", expand=True)

    def cacher(self):
        self.frame.pack_forget()


# ================================================
#  ECRAN STATISTIQUES GLOBALES
# ================================================

class EcranStats:
    def __init__(self, app):
        self.app = app
        self.frame = tk.Frame(app.root, bg=COULEUR_FOND)

    def _construire(self):
        for w in self.frame.winfo_children():
            w.destroy()

        stats = db.get_statistiques_globales()
        # stats is a tuple: (total, moy, par_niveau, classement)
        # total   = (count,)
        # moy     = rounded value
        # par_niveau = list of (niveau_ia, count) tuples
        # classement = list of (nom, score_total, victoires, defaites, nuls, total) tuples
        total_val      = stats[0][0] if stats[0] else 0
        duree_moy      = stats[1]
        par_niveau_lst = stats[2]
        classement_lst = stats[3]

        f = self.frame

        label_titre(f, "📊 Statistiques Globales", COULEUR_OR).pack(pady=(20, 5))

        # Infos generales
        carte = frame_carte(f, padx=25, pady=15)
        carte.pack(padx=30, pady=8, fill="x")

        tk.Label(carte, text="Informations générales", bg=COULEUR_ACCENT,
                 fg=COULEUR_TEXTE, font=POLICE_SOUS).pack(anchor="w", pady=(0, 8))

        row_info = tk.Frame(carte, bg=COULEUR_ACCENT)
        row_info.pack(fill="x")

        blocs = [
            ("🎮\nParties jouées", total_val),
            ("⏱\nDurée moyenne",  f"{duree_moy}s"),
        ]
        for label, val in blocs:
            bloc = tk.Frame(row_info, bg=COULEUR_FOND, padx=20, pady=10)
            bloc.pack(side="left", padx=8, pady=4)
            tk.Label(bloc, text=str(val), bg=COULEUR_FOND,
                     fg=COULEUR_OR, font=("Helvetica", 20, "bold")).pack()
            tk.Label(bloc, text=label, bg=COULEUR_FOND,
                     fg=COULEUR_TEXTE_ALT, font=POLICE_SMALL).pack()

        # Parties par niveau IA
        # par_niveau_lst : list of (niveau_ia, nb) tuples
        if par_niveau_lst:
            carte_niv = frame_carte(f, padx=25, pady=12)
            carte_niv.pack(padx=30, pady=5, fill="x")

            tk.Label(carte_niv, text="Parties JcIA par niveau",
                     bg=COULEUR_ACCENT, fg=COULEUR_TEXTE, font=POLICE_SOUS).pack(anchor="w")

            for row_niv in par_niveau_lst:
                niv = row_niv[0]
                nb  = row_niv[1]
                nom_niv = NIVEAUX_IA.get(niv, f"Niveau {niv}")
                tk.Label(carte_niv,
                         text=f"  Niveau {niv} ({nom_niv}) : {nb} partie(s)",
                         bg=COULEUR_ACCENT, fg=COULEUR_TEXTE, font=POLICE_NORMAL).pack(anchor="w")

        # Classement
        # classement row: (nom, score_total, victoires, defaites, nuls, total_parties)
        CL_NOM           = 0
        CL_SCORE         = 1
        CL_VICTOIRES     = 2
        CL_DEFAITES      = 3
        CL_NULS          = 4
        CL_TOTAL_PARTIES = 5

        carte_class = frame_carte(f, padx=25, pady=12)
        carte_class.pack(padx=30, pady=5, fill="x")

        tk.Label(carte_class, text="🏅 Classement des joueurs",
                 bg=COULEUR_ACCENT, fg=COULEUR_TEXTE, font=POLICE_SOUS).pack(anchor="w", pady=(0, 8))

        if classement_lst:
            medailles = [COULEUR_OR, COULEUR_ARGENT, COULEUR_BRONZE]
            entete = "  Rang   Joueur              Score    V    D   Taux"
            tk.Label(carte_class, text=entete, bg=COULEUR_ACCENT,
                     fg=COULEUR_TEXTE_ALT, font=POLICE_MONO).pack(anchor="w")

            for i, j in enumerate(classement_lst):
                couleur = medailles[i] if i < 3 else COULEUR_TEXTE
                total = j[CL_TOTAL_PARTIES] or 1
                taux = round(j[CL_VICTOIRES] / total * 100, 1)
                ligne = (f"  {'🥇🥈🥉'[i] if i < 3 else f'{i+1:2}.'}"
                         f"  {j[CL_NOM]:<18}  {j[CL_SCORE]:>5}  "
                         f"{j[CL_VICTOIRES]:>3}  {j[CL_DEFAITES]:>3}   {taux}%")
                tk.Label(carte_class, text=ligne, bg=COULEUR_ACCENT,
                         fg=couleur, font=POLICE_MONO).pack(anchor="w")
        else:
            tk.Label(carte_class, text="Aucune partie enregistrée.",
                     bg=COULEUR_ACCENT, fg=COULEUR_TEXTE_ALT,
                     font=POLICE_NORMAL).pack()

        # Bouton retour
        btn_retour = tk.Button(f, text="← Retour",
                               command=self.app.afficher_menu_principal
                               if self.app.joueur_actif else self.app.afficher_accueil)
        bouton_style(btn_retour, couleur=COULEUR_ACCENT)
        btn_retour.pack(pady=15)

    def afficher(self):
        self._construire()
        self.frame.pack(fill="both", expand=True)

    def cacher(self):
        self.frame.pack_forget()


# ================================================
#  APPLICATION PRINCIPALE
# ================================================

class Application:
    def __init__(self):
        db.initialiser_bd()

        self.root = tk.Tk()
        self.root.title(TITRE)
        self.root.geometry(f"{LARGEUR_FENETRE}x{HAUTEUR_FENETRE}")
        self.root.configure(bg=COULEUR_FOND)
        self.root.resizable(True, True)

        self.joueur_actif = None
        self.ecran_courant = None

        self.ecran_accueil = EcranAccueil(self)
        self.ecran_menu = MenuPrincipal(self)
        self.ecran_profil = EcranProfil(self)
        self.ecran_stats = EcranStats(self)

        self.afficher_accueil()

    def _changer_ecran(self, nouvel_ecran):
        if self.ecran_courant:
            self.ecran_courant.cacher()
        self.ecran_courant = nouvel_ecran
        nouvel_ecran.afficher()

    def afficher_accueil(self):
        self._changer_ecran(self.ecran_accueil)

    def afficher_menu_principal(self):
        if not self.joueur_actif:
            self.afficher_accueil()
            return
        self._changer_ecran(self.ecran_menu)

    def afficher_profil(self):
        self._changer_ecran(self.ecran_profil)

    def afficher_stats_globales(self):
        self._changer_ecran(self.ecran_stats)

    def deconnecter(self):
        self.joueur_actif = None
        self.ecran_accueil = EcranAccueil(self)
        self.afficher_accueil()

    def lancer_jcj(self):
        ecran_config = EcranConfig(self, "JcJ")
        self._changer_ecran(ecran_config)

    def lancer_jcia(self):
        ecran_config = EcranConfig(self, "JcIA")
        self._changer_ecran(ecran_config)

    def lancer_partie(self, piles, mode, joueur2, niveau_ia):
        ecran_jeu = EcranJeu(self, piles, mode, joueur2, niveau_ia)
        self._changer_ecran(ecran_jeu)

    def run(self):
        self.root.mainloop()


# ================================================
#  POINT D'ENTREE
# ================================================

if __name__=="__main__":
    app=Application()
    app.run()
