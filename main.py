from settings import *
import tkinter as tk
import time
import os
import database as BD
import player as player_service
from enemy import jouer_ia

ICONS_DIR=os.path.join(os.path.dirname(os.path.abspath(__file__)),"assets","icons")
_icones_cache={}

def get_icon(nom):
    if nom not in _icones_cache:
        chemin=os.path.join(ICONS_DIR,f"{nom}.png")
        _icones_cache[nom]=tk.PhotoImage(file=chemin)
    return _icones_cache[nom]

COULEURS_NIVEAU={1:C_NIV1,2:C_NIV2,3:C_NIV3,4:C_NIV4}

etat={
    "page_courante":"accueil"  ,"joueur1":None  ,"joueur2":None,
    "mode_jeu":"JcIA"          ,"niveau_ia":2   ,"piles": [3,5,7],
    "piles_initiales":[3,5,7]  ,"tour":1        ,"partie_en_cours":False,
    "debut_partie":None        ,"nb_coups":0    ,"pile_selectionnee":None,
    "frame_principale":None    ,"root":None,
}

def partie_terminee():
    return all(p==0 for p in etat["piles"])

def effacer_frame():
    for w in etat["frame_principale"].winfo_children():
        w.destroy()

def _hover_btn(btn,couleur,survol):
    btn.bind("<Enter>",lambda _: btn.config(bg=survol))
    btn.bind("<Leave>",lambda _: btn.config(bg=couleur))

def creer_btn(parent,texte,commande,couleur=C_BOUTON,fg=None,padx=22,pady=10,taille=11,icone=None,survol=None,**kwargs):
    survol=survol if survol else (C_BTN_HOVER if couleur==C_BOUTON else C_SURVOL)
    fg=fg if fg else (C_BOUTON_TEXTE if couleur==C_BOUTON else C_TEXTE)
    if icone is not None:
        img=get_icon(icone)
        btn=tk.Button(parent,text=texte,image=img,compound="left",command=commande,bg=couleur,fg=fg,font=("Helvetica",taille,"bold"),relief="flat",cursor="hand2",padx=padx,pady=pady,activebackground=survol,activeforeground=fg,bd=0,highlightthickness=0,**kwargs)
        btn.image=img
    else:
        btn=tk.Button(parent,text=texte,command=commande,bg=couleur,fg=fg,font=("Helvetica",taille,"bold"),relief="flat",cursor="hand2",padx=padx,pady=pady,activebackground=survol,activeforeground=fg,bd=0,highlightthickness=0,**kwargs)
    _hover_btn(btn,couleur,survol)
    return btn

def creer_label(parent,texte,taille=11,couleur=C_TEXTE,bold=False,fond=C_FOND,**kwargs):
    style="bold" if bold else "normal"
    return tk.Label(parent,text=texte,bg=fond,fg=couleur,font=("Helvetica",taille,style),**kwargs)

def creer_entry(parent,largeur=20,**kwargs):
    e=tk.Entry(parent,width=largeur,bg=C_ACCENT,fg=C_TEXTE,insertbackground=C_TEXTE,font=F_NORMAL,relief="flat",bd=0,highlightthickness=1,highlightbackground=C_BORDURE,highlightcolor=C_BOUTON,disabledbackground=C_PANNEAU,disabledforeground=C_TEXTE_DIM,**kwargs)
    e.config(borderwidth=10)
    return e

def creer_carte(parent,titre=None,**kwargs):
    frame=tk.Frame(parent,bg=C_PANNEAU,bd=0,relief="flat",highlightthickness=1,highlightbackground=C_BORDURE,highlightcolor=C_BORDURE,**kwargs)
    if titre:
        tk.Label(frame,text=titre,bg=C_PANNEAU,fg=C_PILE,font=F_SOUS).pack(anchor="w",padx=ESP_M,pady=(ESP_M,ESP_XS))
        sep=tk.Frame(frame,bg=C_BORDURE,height=1)
        sep.pack(fill="x",padx=ESP_M,pady=(0,ESP_S))
    return frame

def creer_separateur(parent,couleur=C_BORDURE,**kwargs):
    return tk.Frame(parent,bg=couleur,height=1,**kwargs)

def page_accueil():
    effacer_frame()
    f=etat["frame_principale"]

    hero=tk.Frame(f,bg=C_FOND)
    hero.pack(fill="x",pady=(ESP_XL,ESP_L))

    tk.Label(hero,image=get_icon("diamond"),bg=C_FOND).pack()
    tk.Label(hero,text="JEU DE NIM",bg=C_FOND,fg=C_TEXTE,font=("Helvetica",34,"bold")).pack(pady=(ESP_S,0))
    regles=tk.Frame(f,bg=C_ACCENT,padx=28,pady=14,highlightthickness=1,highlightbackground=C_BORDURE)
    regles.pack(pady=ESP_L,ipadx=ESP_S)
    tk.Label(regles,text="Règle du jeu",bg=C_ACCENT,fg=C_TEXTE_DIM,font=("Helvetica",9,"bold")).pack()
    tk.Label(regles,text="Le dernier joueur à prendre un objet perd la partie.",bg=C_ACCENT,fg=C_PILE,
             font=("Helvetica",12,"italic")).pack(pady=(2,0))

    btns=tk.Frame(f,bg=C_FOND)
    btns.pack(pady=ESP_S)

    creer_btn(btns,"Nouvelle Partie",page_config_partie,taille=13,padx=40,pady=12,icone="play").grid(row=0,column=0,padx=8,pady=6,sticky="ew")
    creer_btn(btns,"Profils & Stats",page_profils,couleur=C_ACCENT,taille=13,padx=40,pady=12,icone="user").grid(row=0,column=1,padx=8,pady=6,sticky="ew")
    creer_btn(btns,"Classement",page_classement,couleur=C_ACCENT,taille=13,padx=40,pady=12,icone="trophy").grid(row=1,column=0,padx=8,pady=6,sticky="ew")
    creer_btn(btns,"Statistiques",page_stats,couleur=C_ACCENT,taille=13,padx=40,pady=12,icone="bar_chart").grid(row=1,column=1,padx=8,pady=6,sticky="ew")

    btns.grid_columnconfigure(0,weight=1,uniform="btncol")
    btns.grid_columnconfigure(1,weight=1,uniform="btncol")

    niveaux_frame=creer_carte(f,titre="Niveaux de l'IA disponibles")
    niveaux_frame.pack(pady=ESP_L,padx=60,fill="x")
    niveaux=[("1","Débutant",C_NIV1),("2","Intermédiaire",C_NIV2),("3","Avancé (Minimax)",C_NIV3),("4","Expert (NimSum)",C_NIV4)]

    grid=tk.Frame(niveaux_frame,bg=C_PANNEAU)
    grid.pack(padx=ESP_S,pady=(2,ESP_M))
    for i,(num,nom,col) in enumerate(niveaux):
        card=tk.Frame(grid,bg=C_ACCENT,padx=16,pady=10,highlightthickness=1,highlightbackground=col)
        card.grid(row=0,column=i,padx=6)
        tk.Label(card,text=f"NIVEAU {num}",bg=C_ACCENT,fg=col,font=("Helvetica",9,"bold")).pack()
        tk.Label(card,text=nom,bg=C_ACCENT,fg=C_TEXTE,font=("Helvetica",10)).pack(pady=(2,0))

def style_radio(rb,actif):
    rb.config(bg=C_PANNEAU if not actif else C_ACCENT,fg=C_BOUTON if actif else C_TEXTE_ALT,selectcolor=C_PANNEAU if not actif else C_ACCENT)

def toggle_mode_widgets():
    mode=etat["mode_var"].get()
    for w in etat["ia_inner"].winfo_children():
        w.config(state="normal" if mode == "JcIA" else "disabled")
    etat["entry_j2"].config(state="normal" if mode == "JcJ" else "disabled")

def lancer():
    try:
        piles=[int(e.get()) for e in etat["entries_piles"]]
        if any(p<=0 for p in piles):
            raise ValueError("Les piles doivent être > 0")
    except ValueError as ex:
        tk.messagebox.showerror("Erreur",f"Piles invalides : {ex}")
        return

    nom_j1=etat["entry_j1"].get().strip() or "Joueur 1"
    existe_j1,joueur1=player_service.selectionner_joueur(nom_j1)
    if not existe_j1:
        ok,joueur1=player_service.creer_profil(nom_j1)
        if not ok:
            tk.messagebox.showerror("Erreur",joueur1)
            return
    etat["joueur1"]={"id":joueur1[0],"nom":joueur1[1]}

    if etat["mode_var"].get()=="JcIA":
        etat["joueur2"]={"id": None,"nom": "IA"}
    else:
        nom_j2=etat["entry_j2"].get().strip() or "Joueur 2"
        existe_j2,joueur2=player_service.selectionner_joueur(nom_j2)
        if not existe_j2:
            ok,joueur2=player_service.creer_profil(nom_j2)
            if not ok:
                tk.messagebox.showerror("Erreur",joueur2)
                return
        etat["joueur2"]={"id": joueur2[0],"nom": joueur2[1]}

    etat["mode_jeu"]=etat["mode_var"].get()
    etat["niveau_ia"]=etat["niveau_var"].get()
    etat["piles"]=piles[:]
    etat["piles_initiales"]=piles[:]
    etat["tour"]=1
    etat["nb_coups"]=0
    etat["debut_partie"]=time.time()
    etat["pile_selectionnee"]=None
    page_jeu()

def page_config_partie():
    effacer_frame()
    f=etat["frame_principale"]

    tk.Label(f,text="  Configuration de la Partie",image=get_icon("settings"),compound="left",bg=C_FOND,fg=C_TEXTE,font=("Helvetica",20,"bold")).pack(pady=(ESP_XL,ESP_L))

    mode_frame=creer_carte(f,titre="Mode de jeu")
    mode_frame.pack(padx=60,fill="x",pady=ESP_S)
    mode_var=tk.StringVar(value="JcIA")
    etat["mode_var"]=mode_var
    modes_inner=tk.Frame(mode_frame,bg=C_PANNEAU)
    modes_inner.pack(padx=ESP_M,pady=ESP_S,anchor="w")

    rb1=tk.Radiobutton(modes_inner,text="Joueur vs IA",image=get_icon("robot"),compound="left",variable=mode_var,value="JcIA",bg=C_PANNEAU,fg=C_TEXTE,selectcolor=C_ACCENT,font=F_NORMAL,activebackground=C_PANNEAU,activeforeground=C_TEXTE,relief="flat",bd=0,highlightthickness=0,command=toggle_mode_widgets)
    rb1.pack(side="left",padx=(0,20))
    rb2=tk.Radiobutton(modes_inner,text="Joueur vs Joueur",image=get_icon("group"),compound="left",variable=mode_var,value="JcJ",bg=C_PANNEAU,fg=C_TEXTE,selectcolor=C_ACCENT,font=F_NORMAL,activebackground=C_PANNEAU,activeforeground=C_TEXTE,relief="flat",bd=0,highlightthickness=0,command=toggle_mode_widgets)
    rb2.pack(side="left")
    ia_frame=creer_carte(f,titre="Niveau de l'IA")
    ia_frame.pack(padx=60,fill="x",pady=ESP_S)
    etat["ia_frame_ref"]=ia_frame

    niveau_var=tk.IntVar(value=2)
    etat["niveau_var"]=niveau_var
    ia_inner=tk.Frame(ia_frame,bg=C_PANNEAU)
    ia_inner.pack(padx=ESP_M,pady=ESP_S,anchor="w")
    etat["ia_inner"]=ia_inner

    niveaux_defs=[(1,"Débutant"),(2,"Intermédiaire"),(3,"Avancé"),(4,"Expert")]
    for val,nom in niveaux_defs:
        col=COULEURS_NIVEAU[val]
        rb=tk.Radiobutton(ia_inner,text=f"  {val}. {nom}",variable=niveau_var,value=val,bg=C_PANNEAU,fg=col,selectcolor=C_ACCENT,font=("Helvetica",11),activebackground=C_PANNEAU,activeforeground=col,relief="flat",bd=0,highlightthickness=0)
        rb.pack(side="left",padx=8)

    joueurs_frame=creer_carte(f,titre="Joueurs")
    joueurs_frame.pack(padx=60,fill="x",pady=ESP_S)
    inner=tk.Frame(joueurs_frame,bg=C_PANNEAU)
    inner.pack(padx=ESP_M,pady=ESP_S,fill="x")

    tk.Label(inner,text="Joueur 1",bg=C_PANNEAU,fg=C_TEXTE_ALT,font=F_NORMAL).grid(row=0,column=0,sticky="w",padx=(0,12),pady=6)
    entry_j1=creer_entry(inner,largeur=22)
    entry_j1.grid(row=0,column=1,sticky="w")
    entry_j1.insert(0,etat["joueur1"]["nom"] if etat["joueur1"] else "")
    etat["entry_j1"]=entry_j1

    tk.Label(inner,text="Joueur 2",bg=C_PANNEAU,fg=C_TEXTE_ALT,font=F_NORMAL).grid(row=1,column=0,sticky="w",padx=(0,12),pady=6)
    entry_j2=creer_entry(inner,largeur=22)
    entry_j2.grid(row=1,column=1,sticky="w")
    entry_j2.insert(0,etat["joueur2"]["nom"] if etat["joueur2"] else "")
    etat["entry_j2"]=entry_j2
    etat["label_j2"]=tk.Label(inner,text="optionnel en mode JcIA",bg=C_PANNEAU,fg=C_TEXTE_DIM,font=F_SMALL)
    etat["label_j2"].grid(row=1,column=2,padx=10)
    toggle_mode_widgets()

    piles_frame=creer_carte(f,titre="Configuration des piles (3 piles)")
    piles_frame.pack(padx=60,fill="x",pady=ESP_S)
    piles_inner=tk.Frame(piles_frame,bg=C_PANNEAU)
    piles_inner.pack(padx=ESP_M,pady=ESP_S,anchor="w")

    entries_piles=[]
    for i,val in enumerate([3,5,7]):
        tk.Label(piles_inner,text=f"Pile {i+1}",bg=C_PANNEAU,fg=C_PILE,font=F_NORMAL).grid(row=0,column=i*2,padx=(0,8))
        e=creer_entry(piles_inner,largeur=5)
        e.insert(0,str(val))
        e.grid(row=0,column=i*2+1,padx=(0,24))
        entries_piles.append(e)
    etat["entries_piles"]=entries_piles

    btn_frame=tk.Frame(f,bg=C_FOND)
    btn_frame.pack(pady=ESP_L)
    creer_btn(btn_frame,"Lancer la Partie",lancer,taille=13,padx=40,pady=12,icone="play").pack(side="left",padx=16)
    creer_btn(btn_frame,"Retour",page_accueil,couleur=C_ACCENT,taille=13,padx=40,pady=12,icone="arrow_left").pack(side="left",padx=16)

piles_canvas=[]
pile_labels=[]

def page_jeu():
    effacer_frame()
    f=etat["frame_principale"]

    etat["partie_en_cours"]=True

    header=tk.Frame(f,bg=C_PANNEAU,pady=14,highlightthickness=0,highlightbackground=C_BORDURE)
    header.pack(fill="x")

    j1_nom=etat["joueur1"]["nom"]
    j2_nom=etat["joueur2"]["nom"]
    etat["lbl_j1"]=tk.Label(header,text=f" {j1_nom}",image=get_icon("dot_active"),compound="left",bg=C_PANNEAU,fg=C_BOUTON,font=("Helvetica",15,"bold"))
    etat["lbl_j1"].grid(row=0,column=0,padx=30)

    tk.Label(header,text="VS",bg=C_PANNEAU,fg=C_TEXTE_DIM,font=("Helvetica",11,"bold")).grid(row=0,column=1,padx=20)

    etat["lbl_j2"]=tk.Label(header,text=f" {j2_nom}",image=get_icon("dot_inactive"),compound="left",bg=C_PANNEAU,fg=C_TEXTE_ALT,font=("Helvetica",15,"bold"))
    etat["lbl_j2"].grid(row=0,column=2,padx=30)
    etat["lbl_tour"]=tk.Label(header,text="",bg=C_PANNEAU,fg=C_OR,font=("Helvetica",11,"italic"))
    etat["lbl_tour"].grid(row=1,column=0,columnspan=3,pady=(6,0))

    header.grid_columnconfigure(0,weight=1)
    header.grid_columnconfigure(2,weight=1)

    creer_separateur(f).pack(fill="x")

    jeu_zone=tk.Frame(f,bg=C_FOND,pady=24)
    jeu_zone.pack(fill="both",expand=True)
    etat["piles_zone"]=jeu_zone
    etat["pile_frames"]=[]

    dessiner_piles()

    ctrl=tk.Frame(f,bg=C_PANNEAU,pady=14,highlightthickness=1,highlightbackground=C_BORDURE)
    ctrl.pack(fill="x")
    tk.Label(ctrl,text="Objets à retirer",bg=C_PANNEAU,fg=C_TEXTE_ALT,font=F_NORMAL).pack(side="left",padx=(24,10))

    etat["spin_val"]=tk.IntVar(value=1)
    spin=tk.Spinbox(ctrl,from_=1,to=99,width=5,textvariable=etat["spin_val"],bg=C_ACCENT,fg=C_TEXTE,buttonbackground=C_ACCENT,font=F_NORMAL,relief="flat",bd=0,highlightthickness=1,highlightbackground=C_BORDURE,insertbackground=C_TEXTE)
    spin.pack(side="left",padx=(0,10))
    etat["spin"]=spin
    etat["lbl_max_objets"]=tk.Label(ctrl,text="",bg=C_PANNEAU,fg=C_PILE,font=F_SMALL)
    etat["lbl_max_objets"].pack(side="left",padx=(0,20))

    btns_jeu=tk.Frame(ctrl,bg=C_PANNEAU)
    btns_jeu.pack(side="left",padx=4)
    creer_btn(btns_jeu,"Jouer",jouer_coup,padx=22,pady=7,icone="check").grid(row=0,column=0,padx=4,sticky="ew")
    creer_btn(btns_jeu,"Abandonner",confirmer_abandon,couleur=C_ACCENT,padx=18,pady=7,icone="undo").grid(row=0,column=1,padx=4,sticky="ew")
    btns_jeu.grid_columnconfigure(0,weight=1,uniform="ctrlcol")
    btns_jeu.grid_columnconfigure(1,weight=1,uniform="ctrlcol")

    etat["status_bar"]=tk.Label(f,text="",bg=C_ACCENT,fg=C_TEXTE,font=F_NORMAL,pady=8)
    etat["status_bar"].pack(fill="x")

    actualiser_tour()

def on_pile_click(idx, _=None):
    if etat["tour"]==1 or etat["mode_jeu"]=="JcJ":
        etat["pile_selectionnee"]=idx
        max_objets=etat["piles"][idx]
        if "spin" in etat and max_objets > 0:
            etat["spin"].config(to=max_objets)
            etat["spin_val"].set(1)
            etat["lbl_max_objets"].config(text=f"max {max_objets}",fg=C_SUCCES if max_objets > 0 else C_ERREUR)
        dessiner_piles()

def dessiner_piles():
    zone=etat["piles_zone"]
    for w in zone.winfo_children():
        w.destroy()

    etat["pile_frames"]=[]
    container=tk.Frame(zone,bg=C_FOND)
    container.pack(expand=True)

    for i,nb in enumerate(etat["piles"]):
        selected=(etat["pile_selectionnee"]==i)
        vide=(nb==0)
        pile_bg=C_PILE_SEL if selected else C_PANNEAU
        border_col=C_PILE_SEL if selected else (C_BORDURE if not vide else C_TEXTE_DIM)
        border_w=2 if selected else 1
        pile_card=tk.Frame(container,bg=pile_bg,padx=22,pady=18,highlightbackground=border_col,highlightthickness=border_w)
        pile_card.grid(row=0,column=i,padx=18,pady=10)
        tk.Label(pile_card,text=f"PILE {i+1}",bg=pile_bg,fg=C_TEXTE if selected else C_TEXTE_ALT,font=("Helvetica",10,"bold")).pack()
        objets_frame=tk.Frame(pile_card,bg=pile_bg)
        objets_frame.pack(pady=10)

        if vide:
            tk.Label(objets_frame,text="VIDE",bg=pile_bg,fg=C_TEXTE_DIM,font=("Helvetica",26)).pack()
        else:
            cols=4
            dot_icon=get_icon("pile_dot_sel" if selected else "pile_dot")
            for j in range(nb):
                r,c=divmod(j,cols)
                tk.Label(objets_frame,image=dot_icon,bg=pile_bg).grid(row=r,column=c,padx=3,pady=2)

        tk.Label(pile_card,text=f"{nb} objet{'s' if nb != 1 else ''}",bg=pile_bg,fg=C_TEXTE if selected else C_TEXTE_ALT,font=("Helvetica",9,"bold" if selected else "normal")).pack(pady=(2,0))

        pile_card.config(cursor="hand2" if not vide else "arrow")
        pile_card.bind("<Button-1>",lambda e,idx=i: on_pile_click(idx,e))
        for child in pile_card.winfo_children():
            child.bind("<Button-1>",lambda e,idx=i: on_pile_click(idx,e))
        etat["pile_frames"].append(pile_card)

    if etat["pile_selectionnee"] is not None and "lbl_max_objets" in etat:
        max_objets=etat["piles"][etat["pile_selectionnee"]]
        if max_objets > 0:
            etat["lbl_max_objets"].config(text=f"max {max_objets}",fg=C_SUCCES)
        else:
            etat["lbl_max_objets"].config(text="pile vide",fg=C_ERREUR)

def actualiser_tour():
    tour=etat["tour"]
    j1=etat["joueur1"]["nom"]
    j2=etat["joueur2"]["nom"]

    if tour == 1:
        etat["lbl_j1"].config(fg=C_BOUTON,image=get_icon("dot_active"))
        etat["lbl_j2"].config(fg=C_TEXTE_ALT,image=get_icon("dot_inactive"))
        etat["lbl_tour"].config(text=f" Tour de {j1}",image=get_icon("arrow_right"),compound="left")
        etat["status_bar"].config(text=f"Sélectionnez une pile puis choisissez le nombre d'objets à retirer.")
    else:
        etat["lbl_j1"].config(fg=C_TEXTE_ALT,image=get_icon("dot_inactive"))
        etat["lbl_j2"].config(fg=C_BOUTON,image=get_icon("dot_active"))
        etat["lbl_tour"].config(text=f" Tour de {j2}",image=get_icon("arrow_right"),compound="left")
        if etat["mode_jeu"]=="JcIA":
            etat["status_bar"].config(text="L'IA réfléchit...")
            etat["root"].after(700,jouer_ia_auto)

def jouer_coup():
    if not etat["partie_en_cours"]:
        return

    if etat["pile_selectionnee"] is None:
        tk.messagebox.showwarning("⚠  Sélection requise","Cliquez sur une pile pour la sélectionner d'abord.")
        return

    idx=etat["pile_selectionnee"]
    max_objets=etat["piles"][idx]

    if max_objets == 0:
        tk.messagebox.showerror("❌  Erreur",f"La pile {idx+1} est vide. Sélectionnez une autre pile.")
        return

    try:
        nb=int(etat["spin_val"].get())
    except ValueError:
        tk.messagebox.showerror("❌  Erreur","Veuillez entrer un nombre valide.")
        return

    if nb<1:
        tk.messagebox.showerror("❌  Erreur","Vous devez retirer au moins 1 objet.")
        return

    if nb>max_objets:
        tk.messagebox.showerror("❌  Erreur",f"La pile {idx+1} ne contient que {max_objets} objet{'s' if max_objets > 1 else ''}.\n"f"Vous ne pouvez retirer que {max_objets} objet(s) maximum.")
        return

    etat["piles"][idx]-=nb
    etat["nb_coups"]+=1
    etat["pile_selectionnee"]=None
    etat["spin_val"].set(1)
    etat["lbl_max_objets"].config(text="")
    dessiner_piles()

    if partie_terminee():
        finir_partie(perdant=etat["tour"])
        return

    etat["tour"]=2 if etat["tour"] == 1 else 1
    actualiser_tour()

def apres_ia():
    etat["pile_selectionnee"]=None
    etat["tour"]=1
    dessiner_piles()
    actualiser_tour()

def jouer_ia_auto():
    if not etat["partie_en_cours"]:
        return
    idx,nb=jouer_ia(etat["piles"],etat["niveau_ia"])
    etat["piles"][idx]-=nb
    etat["nb_coups"]+=1
    etat["pile_selectionnee"]=idx
    dessiner_piles()
    etat["status_bar"].config(text=f"L'IA retire {nb} objet(s) de la pile {idx+1}.")

    if partie_terminee():
        etat["root"].after(400,lambda: finir_partie(perdant=2))
        return

    etat["root"].after(500,apres_ia)

def finir_partie(perdant):
    etat["partie_en_cours"]=False
    duree=int(time.time()-etat["debut_partie"]) if etat["debut_partie"] else 0
    gagnant=perdant
    nom_gagnant=etat["joueur1"]["nom"] if gagnant==1 else etat["joueur2"]["nom"]
    nom_perdant=etat["joueur1"]["nom"] if perdant==2 else etat["joueur2"]["nom"]

    joueur1_id=etat["joueur1"].get("id")
    joueur2_id=etat["joueur2"].get("id")

    if joueur1_id is not None and joueur2_id is not None:
        try:
            BD.enregistrer_partie(joueur1_id,joueur2_id,etat["mode_jeu"],etat["niveau_ia"],etat["piles_initiales"],joueur1_id if gagnant==1 else joueur2_id,joueur1_id if perdant==1 else joueur2_id,duree,etat["nb_coups"])
        except Exception:
            pass

        try:
            if gagnant==1:
                BD.mettre_a_jour_stats(joueur1_id,victoire=1,points=10)
                BD.mettre_a_jour_stats(joueur2_id,defaite=1,points=-5)
            else:
                BD.mettre_a_jour_stats(joueur2_id,victoire=1,points=10)
                BD.mettre_a_jour_stats(joueur1_id,defaite=1,points=-5)
        except Exception:
            pass
    elif joueur1_id is not None and joueur2_id is None:
        try:
            BD.enregistrer_partie(joueur1_id,joueur2_id,etat["mode_jeu"],etat["niveau_ia"],etat["piles_initiales"],joueur1_id if gagnant==1 else joueur2_id,joueur1_id if perdant==1 else joueur2_id,duree,etat["nb_coups"])
        except Exception:
            pass

        try:
            if gagnant==1:
                BD.mettre_a_jour_stats(joueur1_id,victoire=1,points=10)
            else:
                BD.mettre_a_jour_stats(joueur1_id,defaite=1,points=-5)
        except Exception:
            pass

    page_resultat(nom_gagnant,nom_perdant,duree)

def confirmer_abandon():
    if tk.messagebox.askyesno("Abandonner","Voulez-vous vraiment abandonner la partie ?"):
        etat["partie_en_cours"]=False
        page_accueil()

def page_resultat(gagnant,perdant,duree):
    effacer_frame()
    f=etat["frame_principale"]

    tk.Frame(f,bg=C_FOND,height=30).pack()
    trophy_lbl=tk.Label(f,image=get_icon("trophy_large"),bg=C_FOND)
    trophy_lbl.pack()
    tk.Label(f,text="Partie Terminée !",bg=C_FOND,fg=C_OR,font=("Helvetica",26,"bold")).pack(pady=(10,0))

    res_frame=creer_carte(f)
    res_frame.pack(pady=20,padx=100,fill="x")
    tk.Label(res_frame,text="GAGNANT",bg=C_PANNEAU,fg=C_TEXTE_DIM,font=("Helvetica",9,"bold")).pack(pady=(20,0))
    tk.Label(res_frame,text=gagnant,bg=C_PANNEAU,fg=C_SUCCES,font=("Helvetica",24,"bold")).pack(pady=(2,0))

    creer_separateur(res_frame,C_BORDURE).pack(fill="x",padx=24,pady=14)

    stats_inner=tk.Frame(res_frame,bg=C_PANNEAU)
    stats_inner.pack(pady=(0,20))
    infos=[("Nombre de coups",str(etat["nb_coups"])),("Durée",f"{duree}s"),("Piles initiales",", ".join(str(p) for p in etat["piles_initiales"])),("Mode",etat["mode_jeu"]),]
    for i,(k,v) in enumerate(infos):
        tk.Label(stats_inner,text=k,bg=C_PANNEAU,fg=C_TEXTE_ALT,font=F_NORMAL).grid(row=i,column=0,sticky="w",padx=(24,16),pady=4)
        tk.Label(stats_inner,text=v,bg=C_PANNEAU,fg=C_TEXTE,font=("Helvetica",11,"bold")).grid(row=i,column=1,sticky="w",padx=(0,24))

    btn_frame=tk.Frame(f,bg=C_FOND)
    btn_frame.pack(pady=ESP_L)

    creer_btn(btn_frame,"Rejouer",page_config_partie,taille=13,padx=30,pady=10,icone="play").grid(row=0,column=0,padx=10,sticky="ew")
    creer_btn(btn_frame,"Accueil",page_accueil,couleur=C_ACCENT,taille=13,padx=30,pady=10,icone="home").grid(row=0,column=1,padx=10,sticky="ew")
    btn_frame.grid_columnconfigure(0,weight=1,uniform="resbtn")
    btn_frame.grid_columnconfigure(1,weight=1,uniform="resbtn")

def creer_profil_form():
    nom=etat["entry_nom_profil"].get().strip()
    if not nom:
        etat["msg_creation_profil"].config(text="Nom requis.",fg=C_ERREUR)
        return
    ok,resultat=player_service.creer_profil(nom)
    if ok:
        etat["msg_creation_profil"].config(text=f"Profil '{nom}' créé !",fg=C_SUCCES)
        etat["entry_nom_profil"].delete(0,"end")
        rafraichir_liste()
    else:
        etat["msg_creation_profil"].config(text=resultat,fg=C_ERREUR)

def choisir_joueur(jou,slot=1):
    etat[f"joueur{slot}"]={"id": jou[0],"nom": jou[1]}
    tk.messagebox.showinfo("Sélection",f"'{jou[1]}' sélectionné comme Joueur {slot}.")

def voir_stats_joueur(jou):
    page_stats_joueur(jou)

def supprimer_joueur(jou):
    if tk.messagebox.askyesno("Supprimer",f"Supprimer le profil '{jou[1]}' ?"):
        BD.supprimer_joueur(jou[0])
        rafraichir_liste()

def rafraichir_liste():
    liste_inner=etat["liste_profils_frame"]
    for w in liste_inner.winfo_children():
        w.destroy()
    headers=["Nom","Score","Victoires","Défaites","Actions"]
    cols_w=[200,80,90,80,320]
    for j,(h,w) in enumerate(zip(headers,cols_w)):
        tk.Label(liste_inner,text=h.upper(),bg=C_PANNEAU,fg=C_PILE,font=("Helvetica",9,"bold"),width=w//10).grid(row=0,column=j,padx=8,pady=(0,8))

    joueurs=BD.get_tous_joueurs()
    for i,joueur in enumerate(joueurs):
        bg=C_PANNEAU
        nom=joueur[1]
        score=joueur[3]
        victoires=joueur[4]
        defaites=joueur[5]
        vals=[nom,score,victoires,defaites]
        for j,v in enumerate(vals):
            tk.Label(liste_inner,text=str(v),bg=bg,fg=C_TEXTE,font=F_NORMAL).grid(row=i+1,column=j,padx=8,pady=6)

        btn_frame=tk.Frame(liste_inner,bg=bg)
        btn_frame.grid(row=i+1,column=4,padx=4,pady=2,sticky="w")
        creer_btn(btn_frame,"J1",lambda jou=joueur: choisir_joueur(jou,1),couleur=C_BOUTON,padx=8,pady=3,taille=8).pack(side="left",padx=2)
        creer_btn(btn_frame,"J2",lambda jou=joueur: choisir_joueur(jou,2),couleur=C_BOUTON,padx=8,pady=3,taille=8).pack(side="left",padx=2)
        creer_btn(btn_frame,"Stats",lambda jou=joueur: voir_stats_joueur(jou),couleur=C_SURVOL,padx=8,pady=3,taille=8).pack(side="left",padx=2)
        creer_btn(btn_frame,"",lambda jou=joueur: supprimer_joueur(jou),couleur=C_SURVOL,padx=6,pady=3,taille=8,icone="close").pack(side="left",padx=2)

def page_profils():
    effacer_frame()
    f=etat["frame_principale"]

    tk.Label(f,text="Gestion des Profils",image=get_icon("user"),compound="left",bg=C_FOND,fg=C_TEXTE,font=("Helvetica",20,"bold")).pack(pady=(ESP_XL,ESP_L))

    creer_frame=creer_carte(f,titre="Créer un profil")
    creer_frame.pack(padx=60,fill="x",pady=ESP_S)
    inner=tk.Frame(creer_frame,bg=C_PANNEAU)
    inner.pack(padx=ESP_M,pady=ESP_S,anchor="w")
    tk.Label(inner,text="Nom",bg=C_PANNEAU,fg=C_TEXTE_ALT,font=F_NORMAL).pack(side="left",padx=(0,10))
    entry_nom=creer_entry(inner,largeur=22)
    entry_nom.pack(side="left",padx=(0,12))
    creer_btn(inner,"+ Créer",creer_profil_form,padx=16,pady=6).pack(side="left",padx=(0,12))
    msg_creation=tk.Label(inner,text="",bg=C_PANNEAU,fg=C_SUCCES,font=F_NORMAL)
    msg_creation.pack(side="left")
    etat["entry_nom_profil"]=entry_nom
    etat["msg_creation_profil"]=msg_creation
    liste_frame=creer_carte(f,titre="Joueurs enregistrés")
    liste_frame.pack(padx=60,fill="x",pady=ESP_S)
    liste_inner=tk.Frame(liste_frame,bg=C_PANNEAU)
    liste_inner.pack(padx=ESP_M,pady=ESP_S,fill="x")
    etat["liste_profils_frame"]=liste_inner
    rafraichir_liste()
    creer_btn(f,"← Retour",page_accueil,couleur=C_ACCENT,padx=20,pady=8).pack(pady=ESP_M)

def badge(parent,label,valeur,couleur):
    c=tk.Frame(parent,bg=C_PANNEAU,padx=26,pady=16,highlightthickness=1,highlightbackground=C_BORDURE)
    c.pack(side="left",padx=8)
    tk.Label(c,text=str(valeur),bg=C_PANNEAU,fg=couleur,font=("Helvetica",28,"bold")).pack()
    tk.Label(c,text=label.upper(),bg=C_PANNEAU,fg=C_TEXTE_DIM,font=("Helvetica",9,"bold")).pack(pady=(2,0))

def page_stats_joueur(joueur):
    effacer_frame()
    f=etat["frame_principale"]

    joueur_id=joueur[0]
    stats=player_service.afficher_stats(joueur)
    tk.Label(f,text=f"Stats de {stats['nom']}",image=get_icon("bar_chart"),compound="left",bg=C_FOND,fg=C_TEXTE,font=("Helvetica",20,"bold")).pack(pady=(ESP_XL,ESP_L))
    total=stats["total_parties"]
    taux=stats["taux_victoire"]
    badges_frame=tk.Frame(f,bg=C_FOND)
    badges_frame.pack(pady=ESP_S)
    badge(badges_frame,"Score",stats["score"],C_OR)
    badge(badges_frame,"Victoires",stats["victoires"],C_SUCCES)
    badge(badges_frame,"Défaites",stats["defaites"],C_ERREUR)
    badge(badges_frame,"Taux %",f"{taux}%",C_PILE)
    bar_frame=creer_carte(f,titre="Taux de victoire")
    bar_frame.pack(padx=60,fill="x",pady=ESP_M)
    bar_inner=tk.Frame(bar_frame,bg=C_PANNEAU)
    bar_inner.pack(padx=ESP_M,pady=ESP_S,fill="x")
    bar_bg=tk.Frame(bar_inner,bg=C_ACCENT,height=18,highlightthickness=1,highlightbackground=C_BORDURE)
    bar_bg.pack(fill="x")
    bar_bg.update_idletasks()
    w_total=bar_bg.winfo_width() or 400
    w_fill=int(w_total*taux/100)
    bar_fill=tk.Frame(bar_inner,bg=C_SUCCES,height=18,width=w_fill)
    bar_fill.place(in_=bar_bg,x=0,y=0)
    tk.Label(bar_inner,text=f"{taux}% de victoires sur {total} parties",bg=C_PANNEAU,fg=C_TEXTE_ALT,font=F_SMALL).pack(anchor="w",pady=(8,0))
    hist_frame=creer_carte(f,titre="Dernières parties")
    hist_frame.pack(padx=60,fill="x",pady=ESP_S)
    historiques=BD.get_historique_joueur(joueur_id)
    for i,p in enumerate(historiques):
        bg=C_PANNEAU if i%2==0 else C_ACCENT
        row=tk.Frame(hist_frame,bg=bg)
        row.pack(fill="x",padx=ESP_M,pady=1)
        joueur1_id=p[1]
        joueur2_id=p[2]
        gagnant_id=p[6]
        resultat="Victoire" if gagnant_id==joueur_id else "Défaite"
        col=C_SUCCES if resultat=="Victoire" else C_ERREUR
        adversaire=p[12] if joueur1_id==joueur_id else p[11]
        piles=p[5]
        coups=p[10]
        duree=p[9]
        date=p[8].strftime("%Y-%m-%d") if hasattr(p[8],'strftime') else str(p[8])

        tk.Label(row,text=resultat,bg=bg,fg=col,font=("Helvetica",10,"bold"),width=10).pack(side="left",padx=8,pady=6)
        tk.Label(row,text=f"vs {adversaire}",bg=bg,fg=C_TEXTE,font=F_NORMAL,width=20,anchor="w").pack(side="left")
        tk.Label(row,text=f"Piles {piles}",bg=bg,fg=C_TEXTE_ALT,font=F_SMALL,width=14).pack(side="left")
        tk.Label(row,text=f"{coups} coups · {duree}s",bg=bg,fg=C_TEXTE_ALT,font=F_SMALL).pack(side="left",padx=8)
        tk.Label(row,text=date,bg=bg,fg=C_TEXTE_DIM,font=F_SMALL).pack(side="right",padx=8)

    creer_btn(f,"← Retour",page_profils,couleur=C_ACCENT,padx=20,pady=8).pack(pady=ESP_M)

def page_classement():
    effacer_frame()
    f=etat["frame_principale"]
    tk.Label(f,text="Classement Général",image=get_icon("target"),compound="left",bg=C_FOND,fg=C_TEXTE,font=("Helvetica",20,"bold")).pack(pady=(ESP_XL,ESP_L))
    classement=BD.get_tous_joueurs()
    medailles=["medal_gold","medal_silver","medal_bronze"]
    couleurs_rang=[C_OR,C_ARGENT,C_BRONZE]
    podium_frame=tk.Frame(f,bg=C_FOND)
    podium_frame.pack(pady=ESP_S)
    for i,joueur in enumerate(classement[:3]):
        col=couleurs_rang[i] if i<3 else C_TEXTE
        pady_extra=8 if i==0 else 0
        card=tk.Frame(podium_frame,bg=C_PANNEAU,padx=26,pady=18+pady_extra,highlightthickness=2,highlightbackground=col)
        card.grid(row=0,column=i,padx=12,sticky="s")
        if i<3:
            tk.Label(card,image=get_icon(medailles[i]),bg=C_PANNEAU).pack()
        else:
            tk.Label(card,text=f"#{i+1}",bg=C_PANNEAU,fg=C_TEXTE,font=("Helvetica",28)).pack()
        tk.Label(card,text=joueur[1],bg=C_PANNEAU,fg=col,font=("Helvetica",14,"bold")).pack(pady=(4,0))
        tk.Label(card,text=f"{joueur[3]} pts",bg=C_PANNEAU,fg=C_TEXTE_ALT,font=F_NORMAL).pack()

    creer_separateur(f).pack(fill="x",padx=40,pady=ESP_L)
    table_frame=creer_carte(f,titre="Tableau complet")
    table_frame.pack(padx=60,fill="x",pady=ESP_S)
    headers=["#","Nom","Score","Victoires","Défaites","Taux %"]
    inner=tk.Frame(table_frame,bg=C_PANNEAU)
    inner.pack(padx=ESP_M,pady=ESP_S,fill="x")

    for j,h in enumerate(headers):
        tk.Label(inner,text=h.upper(),bg=C_PANNEAU,fg=C_PILE,font=("Helvetica",9,"bold"),width=10).grid(row=0,column=j,pady=(0,8))

    for i,joueur in enumerate(classement):
        bg=C_PANNEAU if i%2==0 else C_ACCENT
        total=joueur[4]+joueur[5]
        taux=f"{round(joueur[4]/total*100,1)}%" if total else "—"
        vals=[f"#{i+1}",joueur[1],joueur[3],joueur[4],joueur[5],taux]
        for j,v in enumerate(vals):
            tk.Label(inner,text=str(v),bg=bg,fg=C_TEXTE,font=F_NORMAL,width=10).grid(row=i+1,column=j,pady=6)

    creer_btn(f,"← Retour",page_accueil,couleur=C_ACCENT,padx=20,pady=8).pack(pady=ESP_M)

def stat_box(parent,label,val,col):
    c=tk.Frame(parent,bg=C_PANNEAU,padx=30,pady=18,highlightthickness=1,highlightbackground=C_BORDURE)
    c.pack(side="left",padx=10)
    tk.Label(c,text=str(val),bg=C_PANNEAU,fg=col,font=("Helvetica",30,"bold")).pack()
    tk.Label(c,text=label.upper(),bg=C_PANNEAU,fg=C_TEXTE_DIM,font=("Helvetica",9,"bold")).pack(pady=(2,0))

def page_stats():
    effacer_frame()
    f=etat["frame_principale"]

    tk.Label(f,text="Statistiques Globales",image=get_icon("bar_chart"),compound="left",bg=C_FOND,fg=C_TEXTE,font=("Helvetica",20,"bold")).pack(pady=(ESP_XL,ESP_L))
    total_parties,duree_moyenne,par_niveau,classement=BD.get_statistiques_globales()
    total_parties=total_parties[0] if isinstance(total_parties,tuple) else total_parties
    total_joueurs=len(BD.get_tous_joueurs())
    meilleur=classement[0] if classement else ("",0,0,0,0)
    chiffres=tk.Frame(f,bg=C_FOND)
    chiffres.pack(pady=ESP_S)
    stat_box(chiffres,"Parties jouées",total_parties,C_PILE)
    stat_box(chiffres,"Joueurs inscrits",total_joueurs,C_SUCCES)
    stat_box(chiffres,"Meilleur score",meilleur[1],C_OR)
    stat_box(chiffres,"Durée moyenne",f"{duree_moyenne}s",C_NIV2)
    niveaux_frame=creer_carte(f,titre="Parties par niveau IA")
    niveaux_frame.pack(padx=60,fill="x",pady=ESP_M)
    noms_niveau={1:"Débutant",2:"Intermédiaire",3:"Avancé",4:"Expert"}
    niveaux_data=[]
    for niveau,nb in par_niveau:
        nom=noms_niveau.get(niveau,f"Niveau {niveau}")
        col=COULEURS_NIVEAU.get(niveau,C_TEXTE)
        niveaux_data.append((nom,nb,col))
    if not niveaux_data:
        niveaux_data=[(noms_niveau[n],0,COULEURS_NIVEAU[n]) for n in (1,2,3,4)]
    max_val=max(n[1] for n in niveaux_data) or 1
    chart_inner=tk.Frame(niveaux_frame,bg=C_PANNEAU)
    chart_inner.pack(padx=ESP_M,pady=ESP_S,fill="x")
    for nom,val,col in niveaux_data:
        row=tk.Frame(chart_inner,bg=C_PANNEAU)
        row.pack(fill="x",pady=5)
        tk.Label(row,text=nom,bg=C_PANNEAU,fg=C_TEXTE_ALT,font=F_NORMAL,width=16,anchor="w").pack(side="left")
        bar_bg=tk.Frame(row,bg=C_ACCENT,height=18,width=300,highlightthickness=1,highlightbackground=C_BORDURE)
        bar_bg.pack(side="left")
        bar_w=max(int(300*val/max_val),3) if val else 0
        bar=tk.Frame(bar_bg,bg=col,height=18,width=bar_w)
        bar.place(x=0,y=0)
        tk.Label(row,text=str(val),bg=C_PANNEAU,fg=col,font=("Helvetica",10,"bold"),width=4).pack(side="left",padx=8)

    creer_btn(f,"← Retour",page_accueil,couleur=C_ACCENT,padx=20,pady=8).pack(pady=ESP_M)

def on_nav_enter(_,b):
    if b is not etat.get("nav_actif"):
        b.config(bg=C_ACCENT,fg=C_TEXTE)

def on_nav_leave(_,b):
    if b is not etat.get("nav_actif"):
        b.config(bg=C_PANNEAU,fg=C_TEXTE_ALT)

def marquer_nav_actif(cle):
    for btn in etat.get("nav_btns",{}).values():
        btn.config(bg=C_PANNEAU,fg=C_TEXTE_ALT)
    actif=etat.get("nav_btns",{}).get(cle)
    if actif:
        actif.config(bg=C_ACCENT,fg=C_BOUTON)
        etat["nav_actif"]=actif

def creer_sidebar(root):
    sidebar=tk.Frame(root,bg=C_PANNEAU,width=190)
    sidebar.pack(side="left",fill="y")
    sidebar.pack_propagate(False)
    tk.Label(sidebar,text="NAVBAR",bg=C_PANNEAU,fg=C_BOUTON,font=("Helvetica",24,"bold")).pack(pady=(28,20))
    creer_separateur(sidebar).pack(fill="x",padx=16,pady=0)
    nav_items=[("accueil","  Accueil","home",page_accueil),("jouer","  Jouer","play",page_config_partie),("profils","  Profils","user",page_profils),("classement","  Classement","trophy",page_classement),("stats","  Statistiques","bar_chart",page_stats),]

    etat["nav_btns"]={}
    for cle,label,icone,commande_page in nav_items:
        def commande(cmd=commande_page,c=cle):
            marquer_nav_actif(c)
            cmd()
        img=get_icon(icone)
        btn=tk.Button(sidebar,text=label,image=img,compound="left",command=commande,bg=C_PANNEAU,fg=C_TEXTE_ALT,font=("Helvetica",11),relief="flat",anchor="w",padx=18,pady=10,cursor="hand2",activebackground=C_ACCENT,activeforeground=C_BOUTON,bd=0,highlightthickness=0)
        btn.image=img
        btn.pack(fill="x",pady=1)
        btn.bind("<Enter>",lambda e,b=btn: on_nav_enter(e,b))
        btn.bind("<Leave>",lambda e,b=btn: on_nav_leave(e,b))
        etat["nav_btns"][cle]=btn

    marquer_nav_actif("accueil")
    tk.Label(sidebar,text="NimGame",bg=C_PANNEAU,fg=C_TEXTE_DIM,font=("Helvetica",8)).pack(side="bottom",pady=14)
    return sidebar

def main():
    try:
        BD.initialiser_bd()
    except Exception:
        tk.messagebox.showerror("Erreur de base de données","Impossible de se connecter à la base de données.")

    root=tk.Tk()
    root.title("Jeu de Nim")
    root.geometry("1000x680")
    root.configure(bg=C_FOND)
    root.resizable(True,True)
    root.minsize(800,720)
    etat["root"]=root
    creer_sidebar(root)
    main_container=tk.Frame(root,bg=C_FOND)
    main_container.pack(side="right",fill="both",expand=True)
    etat["frame_principale"]=main_container
    page_accueil()
    root.mainloop()

if __name__=="__main__":
    main()