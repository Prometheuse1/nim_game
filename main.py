#!/usr/bin/env python3
"""Jeu de Nim simple avec interface Tkinter procédurale."""
import random
import tkinter as tk
from tkinter import messagebox

players = {}
history = []
piles = [5, 4, 3]
current_player = None
mode_var = None
player1_var = None
player2_var = None
pile_var = None
remove_var = None
player_listbox = None
stats_label = None
history_text = None
piles_label = None
winner_label = None
start_button = None
remove_button = None
player2_menu = None
piles_canvas = None


def ajouter_joueur():
    name = player_name_entry.get().strip()
    if not name:
        messagebox.showwarning("Erreur", "Entrez un nom de joueur valide.")
        return
    if name in players:
        messagebox.showwarning("Erreur", "Ce joueur existe déjà.")
        return
    players[name] = {"wins": 0, "losses": 0, "games": 0}
    player_name_entry.delete(0, tk.END)
    mettre_a_jour_players()
    messagebox.showinfo("Succès", f"Joueur '{name}' ajouté.")


def mettre_a_jour_players():
    player_listbox.delete(0, tk.END)
    noms = list(players.keys())
    for nom in noms:
        player_listbox.insert(tk.END, f"{nom} - V:{players[nom]['wins']} D:{players[nom]['losses']} G:{players[nom]['games']}")
    if noms:
        player1_var.set(noms[0])
        player2_var.set(noms[0] if len(noms) > 1 else noms[0])
    else:
        player1_var.set("")
        player2_var.set("")
    mettre_a_jour_option_menu()
    mettre_a_jour_stats()


def mettre_a_jour_option_menu():
    noms = list(players.keys())
    menu1 = player1_menu["menu"]
    menu2 = player2_menu["menu"]
    menu1.delete(0, tk.END)
    menu2.delete(0, tk.END)
    for nom in noms:
        menu1.add_command(label=nom, command=lambda value=nom: player1_var.set(value))
        menu2.add_command(label=nom, command=lambda value=nom: player2_var.set(value))
    player2_menu.config(state="normal" if mode_var.get() == 1 else "disabled")


def new_game():
    global piles, current_player
    if mode_var.get() == 1:
        if player1_var.get() == player2_var.get() or not player1_var.get() or not player2_var.get():
            messagebox.showwarning("Erreur", "Choisissez deux joueurs différents.")
            return
    else:
        if not player1_var.get():
            messagebox.showwarning("Erreur", "Choisissez un joueur.")
            return
    piles = [5, 4, 3]
    current_player = 1
    pile_var.set(1)
    remove_var.set(1)
    mettre_a_jour_piles()
    mettre_a_jour_status(f"Partie lancée : {mode_label()} - Tour du joueur 1")
    start_button.config(state="disabled")
    remove_button.config(state="normal")
    if mode_var.get() == 2 and current_player == 2:
        root.after(300, ia_turn)


def mode_label():
    return "Joueur vs Joueur" if mode_var.get() == 1 else "Joueur vs IA"


def dessiner_piles():
    """Affiche les piles sous forme de blocs"""
    piles_canvas.delete("all")
    couleurs = ["#FF6B6B", "#4ECDC4", "#FFE66D"]  # Rouge, Turquoise, Jaune
    x_start = 40
    spacing = 120
    block_width = 30
    block_height = 25
    
    for pile_idx, (pile_count, couleur) in enumerate(zip(piles, couleurs)):
        x = x_start + pile_idx * spacing
        y_start = 180
        
        # Titre de la pile
        piles_canvas.create_text(x + block_width // 2, y_start - 30, 
                                text=f"Pile {pile_idx + 1}\n({pile_count})", 
                                font=("Helvetica", 12, "bold"), fill="#333333")
        
        # Dessiner les blocs
        for i in range(pile_count):
            y = y_start - (i * (block_height + 5))
            piles_canvas.create_rectangle(x, y, x + block_width, y + block_height,
                                        fill=couleur, outline="#000000", width=2)
            piles_canvas.create_text(x + block_width // 2, y + block_height // 2,
                                    text=str(i + 1), font=("Helvetica", 10, "bold"), 
                                    fill="white")


def mettre_a_jour_piles():
    piles_label.config(text=" | ".join(f"Pile {i+1} = {valeur}" for i, valeur in enumerate(piles)))
    dessiner_piles()
    pile = pile_var.get() - 1
    if 0 <= pile < len(piles):
        max_remove = max(1, piles[pile])
        remove_spinbox.config(to=max_remove)
        if remove_var.get() > max_remove:
            remove_var.set(max_remove)
    else:
        remove_spinbox.config(to=1)
        remove_var.set(1)


def mettre_a_jour_status(message):
    winner_label.config(text=message)


def remove_matches():
    global current_player
    pile_index = pile_var.get() - 1
    if pile_index < 0 or pile_index >= len(piles):
        messagebox.showwarning("Erreur", "Choisissez une pile valide.")
        return
    if piles[pile_index] == 0:
        messagebox.showwarning("Erreur", "La pile choisie est vide.")
        return
    remove_amount = remove_var.get()
    if remove_amount < 1 or remove_amount > piles[pile_index]:
        messagebox.showwarning("Erreur", "Nombre d'allumettes invalide.")
        return
    piles[pile_index] -= remove_amount
    mettre_a_jour_piles()
    if sum(piles) == 0:
        declare_winner()
        return
    if mode_var.get() == 2 and current_player == 1:
        current_player = 2
        mettre_a_jour_status("Tour de l'IA...")
        root.after(500, ia_turn)
    else:
        current_player = 1 if current_player == 2 else 2
        mettre_a_jour_status(f"Tour du joueur {current_player}")


def ia_turn():
    global current_player
    if sum(piles) == 0:
        return
    pile_index, remove_amount = calculate_ia_move()
    piles[pile_index] -= remove_amount
    mettre_a_jour_piles()
    if sum(piles) == 0:
        declare_winner()
        return
    current_player = 1
    mettre_a_jour_status("Tour du joueur 1")


def calculate_ia_move():
    xor = 0
    for valeur in piles:
        xor ^= valeur
    if xor == 0:
        for i, valeur in enumerate(piles):
            if valeur > 0:
                return i, 1
    for i, valeur in enumerate(piles):
        cible = valeur ^ xor
        if cible < valeur:
            return i, valeur - cible
    non_empty = [(i, valeur) for i, valeur in enumerate(piles) if valeur > 0]
    i, valeur = random.choice(non_empty)
    return i, random.randint(1, valeur)


def declare_winner():
    winner = "IA" if mode_var.get() == 2 and current_player == 2 else f"Joueur {current_player}"
    if mode_var.get() == 1:
        winner_name = player1_var.get() if current_player == 1 else player2_var.get()
    else:
        winner_name = "IA" if current_player == 2 else player1_var.get()
    loser_name = player2_var.get() if current_player == 1 else player1_var.get() if mode_var.get() == 1 else player1_var.get()
    if winner_name != "IA":
        players[winner_name]["wins"] += 1
        players[winner_name]["games"] += 1
    if loser_name in players:
        players[loser_name]["losses"] += 1
        players[loser_name]["games"] += 1
    history_entry = f"{winner_name} a gagné ({mode_label()}) avec piles {piles}."
    history.append(history_entry)
    mettre_a_jour_history()
    mettre_a_jour_stats()
    mettre_a_jour_status(f"Partie terminée. Vainqueur : {winner_name}")
    start_button.config(state="normal")
    remove_button.config(state="disabled")


def mettre_a_jour_stats():
    lines = ["Statistiques des joueurs:"]
    for nom, stats in players.items():
        lines.append(f"{nom} - Victoires: {stats['wins']} | Défaites: {stats['losses']} | Parties: {stats['games']}")
    stats_label.config(text="\n".join(lines))


def mettre_a_jour_history():
    history_text.config(state="normal")
    history_text.delete(1.0, tk.END)
    for ligne in history[-10:]:
        history_text.insert(tk.END, ligne + "\n")
    history_text.config(state="disabled")


def changer_mode(*args):
    if mode_var.get() == 1:
        player2_menu.config(state="normal")
    else:
        player2_menu.config(state="disabled")
    mettre_a_jour_piles()
    mettre_a_jour_status(f"Mode choisi: {mode_label()}")


def construire_interface():
    global root, mode_var, player1_var, player2_var, pile_var, remove_var
    global player_name_entry, player_listbox, stats_label, history_text, piles_label, winner_label, start_button, remove_button, player1_menu, player2_menu, remove_spinbox, piles_canvas
    
    root = tk.Tk()
    root.title("🎮 Jeu de Nim - Interface Graphique")
    root.geometry("1000x700")
    root.resizable(False, False)
    root.config(bg="#0F3460")
    
    # ===== HEADER =====
    header_frame = tk.Frame(root, bg="#E94560", height=60)
    header_frame.pack(fill="x", padx=0, pady=0)
    header_frame.pack_propagate(False)
    
    header = tk.Label(header_frame, text="🎮 JEU DE NIM 🎮", font=("Helvetica", 28, "bold"), 
                     bg="#E94560", fg="white")
    header.pack(pady=10)
    
    # ===== MAIN CONTENT =====
    main_frame = tk.Frame(root, bg="#0F3460")
    main_frame.pack(fill="both", expand=True, padx=15, pady=15)
    
    # ===== LEFT PANEL =====
    left_frame = tk.LabelFrame(main_frame, text="⚙️  CONFIGURATION", padx=15, pady=15, 
                               bg="#1A4D7A", fg="white", font=("Helvetica", 11, "bold"))
    left_frame.pack(side="left", fill="y", padx=(0, 10))
    
    # Ajouter joueur
    tk.Label(left_frame, text="Nom joueur :", bg="#1A4D7A", fg="white", 
            font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(10, 5))
    player_name_entry = tk.Entry(left_frame, width=24, font=("Helvetica", 10), 
                                bg="#E8F4F8", fg="#333333")
    player_name_entry.pack(anchor="w", pady=(0, 8))
    tk.Button(left_frame, text="➕ Ajouter joueur", command=ajouter_joueur, width=20,
             bg="#16C784", fg="white", font=("Helvetica", 10, "bold"),
             activebackground="#12A970", relief="flat", padx=10, pady=5).pack(anchor="w", pady=(0, 15))
    
    # Liste des joueurs
    tk.Label(left_frame, text="Joueurs existants :", bg="#1A4D7A", fg="white",
            font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(10, 5))
    player_listbox = tk.Listbox(left_frame, width=28, height=8, font=("Helvetica", 9),
                               bg="#E8F4F8", fg="#333333", highlightthickness=0)
    player_listbox.pack(anchor="w", pady=(0, 15))
    
    # Mode de jeu
    mode_var = tk.IntVar(value=1)
    tk.Label(left_frame, text="Mode de jeu :", bg="#1A4D7A", fg="white",
            font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(10, 8))
    tk.Radiobutton(left_frame, text="👥 Joueur vs Joueur", variable=mode_var, value=1, 
                  command=changer_mode, bg="#1A4D7A", fg="white", 
                  font=("Helvetica", 10), activebackground="#1A4D7A", activeforeground="white",
                  selectcolor="#16C784").pack(anchor="w", pady=4)
    tk.Radiobutton(left_frame, text="🤖 Joueur vs IA", variable=mode_var, value=2, 
                  command=changer_mode, bg="#1A4D7A", fg="white",
                  font=("Helvetica", 10), activebackground="#1A4D7A", activeforeground="white",
                  selectcolor="#16C784").pack(anchor="w", pady=4)
    
    # Sélection des joueurs
    player1_var = tk.StringVar(value="")
    player2_var = tk.StringVar(value="")
    
    tk.Label(left_frame, text="Joueur 1 :", bg="#1A4D7A", fg="white",
            font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(15, 5))
    player1_menu = tk.OptionMenu(left_frame, player1_var, "")
    player1_menu.config(width=20, bg="#E8F4F8", fg="#333333", font=("Helvetica", 10),
                       activebackground="#16C784", activeforeground="white")
    player1_menu.pack(anchor="w", pady=(0, 10))
    
    tk.Label(left_frame, text="Joueur 2 / IA :", bg="#1A4D7A", fg="white",
            font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(0, 5))
    player2_menu = tk.OptionMenu(left_frame, player2_var, "")
    player2_menu.config(width=20, bg="#E8F4F8", fg="#333333", font=("Helvetica", 10),
                       activebackground="#16C784", activeforeground="white")
    player2_menu.pack(anchor="w", pady=(0, 15))
    
    # Bouton Démarrer - SUPER MAGNIFIQUE
    start_button = tk.Button(left_frame, text="🚀 DÉMARRER LA PARTIE 🚀", command=new_game, 
                            width=26, bg="#E94560", fg="white", font=("Helvetica", 14, "bold"),
                            activebackground="#D6344A", activeforeground="#FFE66D",
                            relief="raised", bd=4, padx=20, pady=20,
                            cursor="hand2", highlightthickness=2, highlightbackground="#FFE66D")
    start_button.pack(pady=(15, 0), fill="x", padx=10)
    
    # ===== CENTER PANEL =====
    center_frame = tk.LabelFrame(main_frame, text="🎯 PILES DE JEU", padx=15, pady=15,
                                bg="#1A4D7A", fg="white", font=("Helvetica", 11, "bold"))
    center_frame.pack(side="left", fill="both", expand=True, padx=10)
    
    # Canvas pour afficher les piles
    piles_canvas = tk.Canvas(center_frame, width=380, height=250, bg="#E8F4F8",
                            highlightthickness=0, relief="flat")
    piles_canvas.pack(pady=(0, 15))
    
    # Texte informatif
    piles_label = tk.Label(center_frame, text="Pile 1 = 5 | Pile 2 = 4 | Pile 3 = 3",
                          font=("Helvetica", 11, "bold"), bg="#1A4D7A", fg="#FFE66D")
    piles_label.pack(pady=(0, 15))
    
    # Contrôles
    control_frame = tk.Frame(center_frame, bg="#1A4D7A")
    control_frame.pack(pady=(0, 15))
    
    tk.Label(control_frame, text="Pile :", bg="#1A4D7A", fg="white",
            font=("Helvetica", 10, "bold")).grid(row=0, column=0, padx=8, pady=5)
    pile_var = tk.IntVar(value=1)
    pile_menu = tk.Spinbox(control_frame, from_=1, to=3, width=6, textvariable=pile_var,
                          command=mettre_a_jour_piles, font=("Helvetica", 10),
                          bg="#E8F4F8", fg="#333333", highlightthickness=0)
    pile_menu.grid(row=0, column=1, padx=8, pady=5)
    
    tk.Label(control_frame, text="Retirer :", bg="#1A4D7A", fg="white",
            font=("Helvetica", 10, "bold")).grid(row=0, column=2, padx=8, pady=5)
    remove_var = tk.IntVar(value=1)
    remove_spinbox = tk.Spinbox(control_frame, from_=1, to=5, width=6, textvariable=remove_var,
                               font=("Helvetica", 10), bg="#E8F4F8", fg="#333333",
                               highlightthickness=0)
    remove_spinbox.grid(row=0, column=3, padx=8, pady=5)
    
    # Bouton Retirer
    remove_button = tk.Button(center_frame, text="✂️  Retirer les allumettes", command=remove_matches,
                             width=28, bg="#16C784", fg="white", font=("Helvetica", 10, "bold"),
                             activebackground="#12A970", state="disabled", relief="flat", padx=10, pady=8)
    remove_button.pack(pady=(0, 15))
    
    # Status
    winner_label = tk.Label(center_frame, text="Cliquez sur DÉMARRER pour commencer la partie.",
                           font=("Helvetica", 11, "bold"), bg="#1A4D7A", fg="#FFE66D", wraplength=350)
    winner_label.pack(pady=(10, 0))
    
    # ===== RIGHT PANEL =====
    right_frame = tk.LabelFrame(main_frame, text="📊 STATISTIQUES & HISTORIQUE", padx=10, pady=10,
                               bg="#1A4D7A", fg="white", font=("Helvetica", 11, "bold"))
    right_frame.pack(side="left", fill="both", expand=True, padx=(10, 0))
    
    stats_label = tk.Label(right_frame, text="Statistiques des joueurs:", justify="left",
                          anchor="nw", bg="#1A4D7A", fg="white", font=("Helvetica", 9))
    stats_label.pack(fill="both", expand=True, pady=(0, 10))
    
    history_text = tk.Text(right_frame, height=14, width=35, state="disabled",
                          font=("Helvetica", 9), bg="#E8F4F8", fg="#333333",
                          highlightthickness=0)
    history_text.pack(pady=(0, 10))
    
    # ===== FOOTER =====
    bottom_frame = tk.Frame(root, bg="#0F3460")
    bottom_frame.pack(fill="x", padx=15, pady=10)
    
    tk.Button(bottom_frame, text="🔄 Réinitialiser les scores", command=reset_stats,
             width=25, bg="#FF6B6B", fg="white", font=("Helvetica", 10, "bold"),
             activebackground="#E05555", relief="flat", padx=10, pady=8).pack(side="left", padx=5)
    
    tk.Button(bottom_frame, text="❌ Quitter", command=root.destroy,
             width=25, bg="#666666", fg="white", font=("Helvetica", 10, "bold"),
             activebackground="#555555", relief="flat", padx=10, pady=8).pack(side="right", padx=5)
    
    # Initialisation
    pile_var.trace_add("write", lambda *args: mettre_a_jour_piles())
    mettre_a_jour_players()
    mettre_a_jour_stats()
    mettre_a_jour_history()
    dessiner_piles()


def reset_stats():
    for stats in players.values():
        stats["wins"] = 0
        stats["losses"] = 0
        stats["games"] = 0
    history.clear()
    mettre_a_jour_stats()
    mettre_a_jour_history()
    mettre_a_jour_status("Statistiques et historique réinitialisés.")


def main():
    construire_interface()
    root.mainloop()


if __name__ == '__main__':
    main()