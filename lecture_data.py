from pathlib import Path
import numpy as np
from classe import Noeud, Barre, Parametres


def lecture_data(path: str) -> tuple[list[Noeud], list[Barre]]:
    """
    Lit un fichier texte du type:
    Parametres:
    string bool bool bool

    Noeuds:
    x y fx fy flag

    Barres:
    i j

    Retourne:
    noeuds: list[Noeud]
    barres: list[Barre]
    paramtres: Parametres
    """
    text = Path(path).read_text(encoding="utf-8")
    lines = text.splitlines()

    section = None  # Ligne de "noeuds" ou "barres"
    noeuds: list[Noeud] = [] 
    barres_temp: list[int, int, float] = []

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
        if line.startswith("parametres"):
            section = "parametres"
            continue

        if section == "parametres":
            parts = line.split()
            if len(parts) != 5:
                raise ValueError(f"Ligne parametres invalide: {line!r}. Attendu: 'out_dir save_csv save_plots show_plots amplification'")
            out_dir = parts[0]
            save_csv, save_plots, show_plots = (p == "true" for p in parts[1:4])
            ampli = float(parts[4])
            parametres = Parametres(out_dir, save_csv, save_plots, show_plots, ampli)

        elif section == "noeuds": 
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
                raise ValueError(f"Ligne noeud invalide: {line!r}. Attendu: 'x y fx fy liaison'.")
            
            idx = len(noeuds) # Les indices des noeuds permettrons d'y accrocher des barres
            pos = np.array([x, y], dtype=float)
            force = np.array([fx, fy], dtype=float)
            noeuds.append(Noeud(idx, pos, force, ux, uy))

        elif section == "barres":
            parts = line.split() 
            if len(parts) != 3:
                raise ValueError(f"Ligne barre invalide: {line!r}. Attendu: 'i j EA'")
            i, j = map(int, (parts[0], parts[1]))
            EA = float(parts[2])
            barres_temp.append((i, j, EA))

        else:
            raise ValueError(f"Ligne hors section (Noeuds/Barres): {line!r}")

    if not noeuds and barres_temp:
        raise ValueError("Le fichier contient des barres mais aucun noeud.")

    n = len(noeuds)
    barres: list[Barre] = []

    # Déterminer si les indices des barres sont en base 1 ou en base 0
    if barres_temp:
        tout_idx: list[int] = []
        for i, j, k in barres_temp:
            tout_idx.append(i)
            tout_idx.append(j)
        min_idx, max_idx = min(tout_idx), max(tout_idx)

        base_1 = (min_idx >= 1) and (max_idx <= n)

        for id, (i, j, EA) in enumerate(barres_temp):
            if base_1:
                i -= 1
                j -= 1

            if not (0 <= i < n and 0 <= j < n): 
                raise ValueError(f"Mauvais indices pour la barre: ({i}, {j}) avec {n} noeuds.\n")

            barres.append(Barre(id, noeuds[i], noeuds[j], EA))
    if n == 0:
        raise ValueError("Il n'y a pas de noeuds")
    if len(barres) == 0:
        raise ValueError("Il n'y a pas de barres")

    return noeuds, barres, parametres