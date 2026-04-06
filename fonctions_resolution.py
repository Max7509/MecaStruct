import numpy as np
from classe import Noeud, Barre

def resolution(noeuds: list[Noeud], barres: list[Barre]) -> np.ndarray:
    """
    Resout le système:
    Construit la matrice d'equations du systeme
    L'inverse avec l'algorithme de Gauss-Jordan
    Renvoie l'inverse multiplié par les parametres d'entrée (forces exterieurs)
    Calcule les deplacements nodaux
    """
    nbrEqua = 2*len(noeuds)
    nbrInco = len(barres)
    for noeud in noeuds:
        if noeud.ux and noeud.uy:
            nbrInco += 2
        elif noeud.ux or noeud.uy:
            nbrInco += 1
    if nbrEqua > nbrInco:
        raise ValueError("Le système est hyperstatique")
    elif nbrEqua < nbrInco:
        raise ValueError("Le système est hypostatique")
    
    K = _constru_matrice(noeuds, barres)
    
    K_inv = _inversion_matrice(K)
    
    forces = np.zeros(len(K), dtype=float)
    for i in range(0, len(forces), 2):
        forces[i  ] = noeuds[int(i/2)].force[0]
        forces[i+1] = noeuds[int(i/2)].force[1]
    
    S = - K_inv @ forces

    """On calcule aussi le résidu, devrait être petit devant les forces"""
    norme = np.linalg.norm(forces)
    residu = np.linalg.norm(K @ S - forces) / (norme if norme != 0 else 1.0)
    print(f"Le résidu de la solution est {residu}")

    _deformation(noeuds, barres, K_inv, S)

    return S


def _constru_matrice(noeuds: list[Noeud], barres: list[Barre]) -> np.ndarray:
    """Construit et renvoie la matrice de rigidité du système."""
    
    ndof = 2*len(noeuds)
    K = np.zeros((ndof, ndof), dtype=float)

    index = len(barres)
    for j in range(0, ndof, 2):
        n = int(j/2)
        for i in range(len(barres)):
            if barres[i].n1 == noeuds[n]:
                K[j  ][i] = (barres[i].n2.pos[0] - noeuds[n].pos[0])/barres[i].len
                K[j+1][i] = (barres[i].n2.pos[1] - noeuds[n].pos[1])/barres[i].len
            elif barres[i].n2 == noeuds[n]:
                K[j  ][i] = (barres[i].n1.pos[0] - noeuds[n].pos[0])/barres[i].len
                K[j+1][i] = (barres[i].n1.pos[1] - noeuds[n].pos[1])/barres[i].len
    
        if noeuds[n].ux and not noeuds[n].uy:
            K[j][index] = 1
            index += 1
        elif not noeuds[n].ux and noeuds[n].uy:
            K[j+1][index] = 1
            index += 1
        elif noeuds[n].ux and  noeuds[n].uy:
            K[j  ][index  ] = 1
            K[j+1][index+1] = 1
            index += 2
        
    return K




def _inversion_matrice(A: np.ndarray) -> np.ndarray:
    """Calcule l'inverse de la matrice de rigidité du système."""
    n = len(A)
    matriceAug = np.zeros((n, 2*n), dtype=float)
    for i in range(n):
        for j in range(n): matriceAug[i][j] = A[i][j]
        matriceAug[i][n+i] = 1.0

    # Seuil en dessous duquel on considère le pivot = 0
    seuil = 1e-7

    for col in range(n):
        colPivot = col
        max = abs(matriceAug[col][col])
        for row in range(col + 1, n):
            v = abs(matriceAug[row][col])
            if v > max:
                max = v
                colPivot = row
        if max < seuil:
            raise ValueError("Système irrésoluble, peut être un mécanisme?")
        
        if not colPivot == col:
            temp = matriceAug[colPivot].copy()
            matriceAug[colPivot] = matriceAug[col]
            matriceAug[col] = temp
        
        pivot = matriceAug[col][col]
        for j in range(2*n):
            matriceAug[col][j] /= pivot
        
        for row in range(n):
            if row == col: continue
            facteur = matriceAug[row][col]
            if abs(facteur) < seuil: continue
            for  j in range(2*n):
                matriceAug[row][j] -= facteur * matriceAug[col][j]
            
    inverse = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(n): 
            inverse[i][j] = matriceAug[i][n + j]
    
    return inverse


    
def _deformation(noeuds: list[Noeud], barres: list[Barre], K_inv: np.ndarray, S: np.ndarray) -> None:
    """Calcule le déplacement de chaque noeud avec la méthode de Mohr"""
    n = len(noeuds)
    b = len(barres)
    for i in range(n):
        if not noeuds[i].ux:
            f = np.zeros(2*n)
            f[2*i] = 1
            s = K_inv @ f
            for j in range(b):
                noeuds[i].dpos[0] -= s[j]*S[j]*barres[j].len / barres[j].EA
        if not noeuds[i].uy:
            f = np.zeros(2*n)
            f[2*i+1] = 1
            s = K_inv @ f
            for j in range(b):
                noeuds[i].dpos[1] -= s[j]*S[j]*barres[j].len / barres[j].EA