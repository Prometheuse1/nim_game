import random
from settings import MINIMAX_PROFONDEUR

def ia_debutant(piles):
    piles_non_vides=[i for i,p in enumerate(piles) if p>0]
    if not piles_non_vides:
        return None, 0

    idx_pile=random.choice(piles_non_vides)
    nb_objets=random.randint(1, piles[idx_pile])
    return idx_pile,nb_objets

def ia_intermediaire(piles):
    """
    Applique des regles simples :
    - Si une seule pile non vide : prend tout sauf 1 (ou tout)
    - Sinon : choisit la plus grande pile et reduit de moitie
    """
    piles_non_vides = [(i, p) for i, p in enumerate(piles) if p > 0]
    if not piles_non_vides:
        return None, 0

    # Si une seule pile non vide
    if len(piles_non_vides) == 1:
        idx, taille = piles_non_vides[0]
        # Prend tout pour gagner
        return idx, taille

    # Strategie : attaquer la plus grande pile
    idx_max, taille_max = max(piles_non_vides, key=lambda x: x[1])

    # Retire entre la moitie et les 2/3 des objets (mais au moins 1)
    min_retrait = max(1, taille_max // 3)
    max_retrait = max(1, taille_max * 2 // 3)
    nb_objets = random.randint(min_retrait, max_retrait)

    return idx_max, nb_objets


# ==============================================
#  Niveau 3 : Avance - Minimax
# ==============================================

def _est_terminal(piles):
    """Verifie si la partie est terminee (toutes les piles vides)."""
    return all(p == 0 for p in piles)


def _minimax(piles, est_ia, profondeur):
    """
    Algorithme Minimax pour choisir le meilleur coup.
    L'IA cherche a maximiser son score.
    Retourne un score : +1 si l'IA gagne, -1 si elle perd.
    """
    if _est_terminal(piles):
        # Le joueur qui vient de jouer a pris le dernier objet -> il a gagne
        # Si c'est au tour de l'IA de jouer et c'est terminal, l'adversaire a gagne
        return 1 if not est_ia else -1

    if profondeur == 0:
        # Heuristique : on evalue par NimSum
        nim_sum = 0
        for p in piles:
            nim_sum ^= p
        return 1 if nim_sum != 0 else -1

    if est_ia:
        meilleur = -2
        for i, taille in enumerate(piles):
            for nb in range(1, taille + 1):
                nouv_piles = list(piles)
                nouv_piles[i] -= nb
                score = _minimax(tuple(nouv_piles), False, profondeur - 1)
                meilleur = max(meilleur, score)
                if meilleur == 1:
                    return meilleur  # elagage simple
        return meilleur
    else:
        meilleur = 2
        for i, taille in enumerate(piles):
            for nb in range(1, taille + 1):
                nouv_piles = list(piles)
                nouv_piles[i] -= nb
                score = _minimax(tuple(nouv_piles), True, profondeur - 1)
                meilleur = min(meilleur, score)
                if meilleur == -1:
                    return meilleur
        return meilleur


def ia_avance(piles):
    """
    Utilise Minimax pour choisir le meilleur coup possible.
    """
    meilleur_score = -2
    meilleur_coup = None

    for i, taille in enumerate(piles):
        for nb in range(1, taille + 1):
            nouv_piles = list(piles)
            nouv_piles[i] -= nb
            score = _minimax(tuple(nouv_piles), False, MINIMAX_PROFONDEUR)
            if score > meilleur_score:
                meilleur_score = score
                meilleur_coup = (i, nb)

    if meilleur_coup:
        return meilleur_coup
    # Fallback
    return ia_debutant(piles)


# ==============================================
#  Niveau 4 : Expert - NimSum (XOR optimal)
# ==============================================

def _nim_sum(piles):
    """Calcule le NimSum (XOR de toutes les piles)."""
    resultat = 0
    for p in piles:
        resultat ^= p
    return resultat


def ia_expert(piles):
    """
    Strategie mathematique optimale basee sur le NimSum.
    Si NimSum != 0, il existe toujours un coup gagnant.
    Si NimSum == 0, joue un coup aleatoire (position perdante).
    """
    ns = _nim_sum(piles)

    if ns != 0:
        # Trouver un coup qui rend le NimSum = 0
        for i, taille in enumerate(piles):
            cible = taille ^ ns
            if cible < taille:
                nb_retrait = taille - cible
                return i, nb_retrait

    # NimSum = 0 : position perdante, jouer aleatoirement
    return ia_debutant(piles)


# ==============================================
#  Interface principale : choisir le niveau
# ==============================================

def jouer_ia(piles, niveau):
    """
    Retourne le coup de l'IA selon le niveau choisi.
    niveau : 1=Debutant, 2=Intermediaire, 3=Avance, 4=Expert
    Retourne (index_pile, nb_objets_a_retirer)
    """
    if niveau == 1:
        return ia_debutant(piles)
    elif niveau == 2:
        return ia_intermediaire(piles)
    elif niveau == 3:
        return ia_avance(piles)
    elif niveau == 4:
        return ia_expert(piles)
    else:
        return ia_debutant(piles)
