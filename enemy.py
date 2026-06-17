import random
from settings import MINIMAX_PROFONDEUR

def ia_debutant(piles):
    piles_non_vides=[i for i,p in enumerate(piles) if p>0]

    idx_pile=random.choice(piles_non_vides)
    nb_objets=random.randint(1,piles[idx_pile])
    return idx_pile,nb_objets

def ia_intermediaire(piles):
    piles_non_vides=[(i,p) for i,p in enumerate(piles) if p>0]

    if len(piles_non_vides)==1:
        idx,taille=piles_non_vides[0]
        return idx,taille

    idx_max,taille_max=max(piles_non_vides, key=lambda x:x[1])

    min_retrait=max(1,taille_max//3)
    max_retrait=max(1,taille_max*2//3)
    nb_objets=random.randint(min_retrait,max_retrait)

    return idx_max,nb_objets

def _est_terminal(piles):
    for p in piles:
        if p!=0:
            return False
    return True


def _minimax(piles,est_ia,profondeur):
    if _est_terminal(piles):
        return 1 if not est_ia else -1

    if profondeur==0:
        nim_sum=0
        for p in piles:
            nim_sum^=p
        return 1 if nim_sum!=0 else -1

    if est_ia:
        meilleur=-2
        for i,taille in enumerate(piles):
            for nb in range(1,taille+1):
                nouv_piles=list(piles)
                nouv_piles[i]-=nb
                score=_minimax(tuple(nouv_piles),False,profondeur-1)
                meilleur=max(meilleur,score)
                if meilleur==1:
                    return meilleur
        return meilleur
    else:
        meilleur=2
        for i,taille in enumerate(piles):
            for nb in range(1,taille+1):
                nouv_piles=list(piles)
                nouv_piles[i]-=nb
                score=_minimax(tuple(nouv_piles),True,profondeur-1)
                meilleur=min(meilleur,score)
                if meilleur==-1:
                    return meilleur
        return meilleur


def ia_avance(piles):
    meilleur_score=-2
    meilleur_coup=None

    for i,taille in enumerate(piles):
        for nb in range(1,taille+1):
            nouv_piles=list(piles)
            nouv_piles[i]-=nb
            score=_minimax(tuple(nouv_piles),False,MINIMAX_PROFONDEUR)
            if score>meilleur_score:
                meilleur_score=score
                meilleur_coup=(i,nb)

    if meilleur_coup:
        return meilleur_coup
    return ia_debutant(piles)

def _nim_sum(piles):
    resultat=0
    for p in piles:
        resultat^=p
    return resultat


def ia_expert(piles):
    ns=_nim_sum(piles)
    if ns!=0:
        for i,taille in enumerate(piles):
            cible=taille^ns
            if cible<taille:
                nb_retrait=taille-cible
                return i,nb_retrait
    return ia_debutant(piles)

def jouer_ia(piles, niveau):
    if niveau==1:
        return ia_debutant(piles)
    if niveau==2:
        return ia_intermediaire(piles)
    if niveau==3:
        return ia_avance(piles)
    if niveau==4:
        return ia_expert(piles)
    return ia_debutant(piles)
