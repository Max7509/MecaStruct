import numpy as np

def deformations(noeud: Noeud) -> None:
     


def deplacement_noeud(noeud_k, direction, barres, N_reels, E, A):
    # 1. Créer un vecteur de force virtuelle unitaire
    F_virt = force_unitaire(noeud_k, direction)
    
    # 2. Résoudre le treillis sous F_virt → obtenir n̄ᵢ
    n_virt = resoudre_treillis(F_virt)
    
    # 3. Sommer la contribution de chaque barre
    delta = sum(N[i] * n_virt[i] * L[i] / (E[i] * A[i]) for i in barres)
    
    return delta