import database as db
from settings import *


def creer_profil(nom):
    if nom=='':
        return False,"Le nom ne peut pas être vide."
    if len(nom.strip())>20:
        return False,"Le nom ne doit pas dépasser 20 caractères."

    valide,resultat=db.creer_joueur(nom)
    if valide:
        joueur=db.get_joueur_par_id(resultat)
        return True,joueur
    else:
        return False,resultat

def selectionner_joueur(nom):
    joueur=db.get_joueur_par_nom(nom)
    if joueur!=[]:
        return True,joueur
    return False,f"Aucun joueur trouvé avec le nom '{nom}'."

def selectionner_joueur_par_id(joueur_id):
    joueur=db.get_joueur_par_id(joueur_id)
    if joueur!=[]:
        return True,joueur
    return False,"Joueur introuvable."

def liste_joueurs():
    return db.get_tous_joueurs()

def afficher_stats(joueur):
    total=joueur[J_VICTOIRES]+joueur[J_DEFAITES]
    taux=(joueur[J_VICTOIRES]/total*100) if total>0 else 0

    return{
        "nom"          :joueur[J_NOM],
        "score"        :joueur[J_SCORE_TOTAL],
        "victoires"    :joueur[J_VICTOIRES],
        "defaites"     :joueur[J_DEFAITES],
        "total_parties":total,
        "taux_victoire":round(taux,1),
        "date_creation":joueur[J_DATE_CREATION],
    }

def historique(joueur_id,limite=20):
    return db.get_historique_joueur(joueur_id,limite)

def supprimer(joueur_id):
    db.supprimer_joueur(joueur_id)

def enregistrer_resultat(joueur_id,victoire):
    if victoire==1:
        db.mettre_a_jour_stats(joueur_id,victoire=1,points=10)
    else:
        db.mettre_a_jour_stats(joueur_id,defaite=1,points=-5)