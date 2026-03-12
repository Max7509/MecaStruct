from pathlib import Path
import numpy as np
from classe import Noeud, Barre


def lecture_data(path: str) -> tuple[list[Noeud], list[Barre]]:
    """
    Lit un fichier texte du type:

    Noeuds:
    x y fx fy flag

    Barres:
    i j

    Retourne:
    noeuds: list[Noeud]
    barres: list[Barre]
    """
    text = Path(path).read_text(encoding="utf-8")
    lines = text.splitlines()

    section = None  # Ligne de "noeuds" ou "barres"
    noeuds: list[Noeud] = [] 
    barres_temp: list[int, int] = []

    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue

        line = line.lower() 
        if line.startswith("noeuds"): 
            section = "noeuds"
            continue
        if line.startswith("barres"):
            section = "barres" 
            continue

        if section == "noeuds": 
            parts = line.split()
            if len(parts) == 5:
                try:
                    x, y, fx, fy = map(float, parts[:4])
                except ValueError:
                    raise ValueError(f"Ligne noeud invalide: {line!r}. Attendu: 'float float float float char'.")
                flag = parts[4]
                if flag == 'f':
                    ux = True
                    uy = True
                elif flag == 'x':
                    ux = True
                    uy = False
                elif flag == 'y':
                    ux = False
                    uy = True
                else:
                    ux = False
                    uy = False
            else: 
                raise ValueError(f"Ligne noeud invalide: {line!r}. Attendu: 'x y fx fy flag'.")
            
            idx = len(noeuds) # Les indices des noeuds permettrons d'y accrocher des barres
            pos = np.array([x, y], dtype=float)
            force = np.array([fx, fy], dtype=float)
            noeuds.append(Noeud(idx, pos, force, ux, uy))

        elif section == "barres":
            parts = line.split() 
            if len(parts) != 2:
                raise ValueError(f"Ligne barre invalide (2 indices attendus): {line!r}")
            i, j = map(int, parts)
            barres_temp.append((i, j))

        else:
            raise ValueError(f"Ligne hors section (Noeuds/Barres): {line!r}")

    if not noeuds and barres_temp:
        raise ValueError("Le fichier contient des barres mais aucun noeud.")

    n = len(noeuds)
    barres: list[Barre] = []

    # Déterminer si les indices des barres sont en base 1 ou en base 0
    if barres_temp:
        tout_idx = [k for pair in barres_temp for k in pair]
        min_idx, max_idx = min(tout_idx), max(tout_idx)

        base_1 = (min_idx >= 1) and (max_idx <= n)

        for b_id, (i, j) in enumerate(barres_temp):
            if base_1:
                i -= 1
                j -= 1

            if not (0 <= i < n and 0 <= j < n): 
                raise ValueError(f"Mauvais indices pour la barre: ({i}, {j}) avec {n} noeuds.\n")

            barres.append(Barre(b_id, noeuds[i], noeuds[j]))
    if n == 0:
        raise ValueError("Il n'y a pas de noeuds")
    if len(barres) == 0:
        raise ValueError("Il n'y a pas de barres")

    return noeuds, barres