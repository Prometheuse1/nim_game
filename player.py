import database as db

J_ID            =0
J_NOM           =1
J_DATE_CREATION =2
J_SCORE_TOTAL   =3
J_VICTOIRES     =4
J_DEFAITES      =5
J_NULS          =6

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

def creer_profil(nom):
    """
    Cree un nouveau profil joueur dans la BDD.
    Retourne (True, joueur_tuple) ou (False, message_erreur).
    """
    if not nom or not nom.strip():
        return False, "Le nom ne peut pas être vide."
    if len(nom.strip()) > 20:
        return False, "Le nom ne doit pas dépasser 20 caractères."

    ok, resultat = db.creer_joueur(nom)
    if ok:
        joueur = db.get_joueur_par_id(resultat)
        return True, joueur
    else:
        return False, resultat


def selectionner_joueur(nom):
    """
    Selectionne un joueur existant par son nom.
    Retourne (True, joueur_tuple) ou (False, message_erreur).
    """
    joueur = db.get_joueur_par_nom(nom)
    if joueur:
        return True, joueur
    return False, f"Aucun joueur trouvé avec le nom '{nom}'."


def selectionner_joueur_par_id(joueur_id):
    """Selectionne un joueur par son id."""
    joueur = db.get_joueur_par_id(joueur_id)
    if joueur:
        return True, joueur
    return False, "Joueur introuvable."


def liste_joueurs():
    """Retourne la liste de tous les joueurs enregistres."""
    return db.get_tous_joueurs()


def afficher_stats(joueur):
    """
    Retourne un dictionnaire lisible des statistiques d'un joueur.
    joueur : tuple issu de la BDD.
    """
    total = joueur[J_VICTOIRES] + joueur[J_DEFAITES] + joueur[J_NULS]
    taux = (joueur[J_VICTOIRES] / total * 100) if total > 0 else 0

    return {
        "nom"          : joueur[J_NOM],
        "score"        : joueur[J_SCORE_TOTAL],
        "victoires"    : joueur[J_VICTOIRES],
        "defaites"     : joueur[J_DEFAITES],
        "nuls"         : joueur[J_NULS],
        "total_parties": total,
        "taux_victoire": round(taux, 1),
        "date_creation": joueur[J_DATE_CREATION],
    }


def historique(joueur_id, limite=20):
    """Retourne l'historique des parties d'un joueur."""
    return db.get_historique_joueur(joueur_id, limite)


def supprimer(joueur_id):
    """Supprime un joueur et son historique."""
    db.supprimer_joueur(joueur_id)


def enregistrer_resultat(joueur_id, victoire, nul=False):
    """
    Met a jour les stats du joueur apres une partie.
    victoire=True -> +10 pts, defaite -> -5 pts, nul -> 0 pt
    """
    if nul:
        db.mettre_a_jour_stats(joueur_id, nul=True, points=0)
    elif victoire:
        db.mettre_a_jour_stats(joueur_id, victoire=True, points=10)
    else:
        db.mettre_a_jour_stats(joueur_id, defaite=True, points=-5)
