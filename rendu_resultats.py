from __future__ import annotations

from pathlib import Path
import csv

import numpy as np
import matplotlib.pyplot as plt

from classe import Noeud, Barre


def print_resultats(S: np.ndarray, noeuds: list[Noeud], barres: list[Barre], parametres: Parametres) -> None:
    """
    Imprimme les efforts maximaux dans les barres et les réactions aux supports
    Créé deux fichiers cvs pour les informations des barres et des noeuds
    Créé un png représentant le treillis avec couleur et eppaisseur selon la tension dans la barre
    Créé un png représentant les déformations du treillis amplifiée
    """

    S = np.asarray(S, dtype=float).reshape(-1)
    m = len(barres)
    N = S[:m]
    idx_max = int(np.argmax(N))
    idx_min = int(np.argmin(N))

    # Impression traction/compression maximum
    if N[idx_max] > 0:
        print(f"Traction maximale : N{barres[idx_max].id} = {N[idx_max]:.6g}")
    else:
        print("Traction maximale : aucune (toutes les barres sont en compression ou nulles)")

    if N[idx_min] < 0:
        print(f"Compression maximale : N{barres[idx_min].id} = {N[idx_min]:.6g}")
    else:
        print("Compression maximale : aucune (toutes les barres sont en traction ou nulles)")
    # Réactions
    print("Réactions aux supports:")
    reactions = []
    k = m
    for nd in noeuds:
        rx = None
        ry = None
        if nd.ux:
            rx = float(S[k])
            k += 1
        if nd.uy:
            ry = float(S[k])
            k += 1
        if rx is not None:
            print(f"R{nd.id}x = {rx:.6g}")
        if ry is not None:
            print(f"R{nd.id}y = {ry:.6g}")

        reactions.append(
            {
                "node_id": nd.id,
                "Rx": rx,
                "Ry": ry,
                "ux_fixed": bool(nd.ux),
                "uy_fixed": bool(nd.uy),
            }
        )

    # Dossier outputs
    out_path = Path(parametres.out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    # CSV
    if parametres.save_csv:
        barres_csv = out_path / "barres.csv"
        with barres_csv.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["bar_id", "x1", "y1", "x2", "y2", "length", "dlen", "N"])
            for i, b in enumerate(barres):
                p1 = b.n1.pos
                p2 = b.n2.pos
                dlen = np.linalg.norm(p1+b.n1.dpos-p2-b.n2.dpos) - b.len
                writer.writerow([b.id, p1[0], p1[1], p2[0], p2[1], b.len, dlen, float(N[i])])

        noeuds_csv = out_path / "noeuds.csv"
        with noeuds_csv.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["node_id", "x", "y", "fx", "fy", "ux_fixed", "uy_fixed", "Rx", "Ry", "dx", "dy"])
            for r in reactions:
                nd = noeuds[r["node_id"]]
                writer.writerow([
                    r["node_id"],
                    nd.pos[0], nd.pos[1],
                    nd.force[0], nd.force[1],
                    r["ux_fixed"], r["uy_fixed"],
                    r["Rx"], r["Ry"],
                    nd.dpos[0], nd.dpos[1],
                ])
        print(f"Tableurs sauvegardés dans: {parametres.out_dir}")

    # PNG
    if parametres.save_plots or parametres.show_plots:
        fig1 = plt.figure()
        max_abs = float(np.max(np.abs(N))) if m > 0 else 0.0
        max_abs = max(max_abs, 1e-12)

        xs = np.array([float(nd.pos[0]) for nd in noeuds])
        ys = np.array([float(nd.pos[1]) for nd in noeuds])
        plt.scatter(xs, ys, s=25, color="k")

        for nd in noeuds:
            x0, y0 = float(nd.pos[0]), float(nd.pos[1])
            plt.text(x0, y0, f" {nd.id}")

            # f : bloqué en x et y
            if nd.ux and nd.uy:
                plt.scatter([x0], [y0], marker="s", s=400, facecolors="none", edgecolors="k")
            # x : ux libre, uy bloqué
            elif (not nd.ux) and nd.uy:
                plt.scatter([x0], [y0], marker="^", s=400, facecolors="none", edgecolors="k")
            # y : ux bloqué, uy libre
            elif nd.ux and (not nd.uy):
                plt.scatter([x0], [y0], marker=">", s=400, facecolors="none", edgecolors="k")

        # Barres (couleur et épaisseur)
        for i, b in enumerate(barres):
            p1 = b.n1.pos
            p2 = b.n2.pos
            n_i = float(N[i])
            couleur = "C3" if n_i >= 0 else "C0"  # traction / compression
            lw = 1.0 + 4.0 * (abs(n_i) / max_abs)
            plt.plot([p1[0], p2[0]], [p1[1], p2[1]], linewidth=lw, color=couleur)

        # Échelle flèches
        diag = float(np.hypot(xs.max() - xs.min(), ys.max() - ys.min())) if len(xs) else 1.0
        fmax = max((np.linalg.norm(nd.force) for nd in noeuds), default=0.0)
        rmax = max(
            max((abs(r["Rx"] or 0.0) for r in reactions), default=0.0),
            max((abs(r["Ry"] or 0.0) for r in reactions), default=0.0),
        )
        amax = max(fmax, rmax)
        scale = (0.25 * diag / amax) if amax > 0 else 0.0
        fscale = scale
        rscale = scale

        # Forces externes
        for nd in noeuds:
            fx, fy = float(nd.force[0]), float(nd.force[1])
            if fx == 0.0 and fy == 0.0:
                continue
            plt.arrow(float(nd.pos[0]), float(nd.pos[1]),
                    fx * fscale, fy * fscale,
                    length_includes_head=True, head_width=0.04*diag, head_length=0.06*diag,
                    linewidth=1, edgecolor="k", facecolor="k")
        # Réactions
        k2 = m
        for nd in noeuds:
            rx = float(S[k2]) if nd.ux else 0.0
            k2 += 1 if nd.ux else 0
            ry = float(S[k2]) if nd.uy else 0.0
            k2 += 1 if nd.uy else 0
            if rx != 0.0 or ry != 0.0:
                plt.arrow(float(nd.pos[0]), float(nd.pos[1]),
                        rx * rscale, ry * rscale,
                        length_includes_head=True, head_width=0.04*diag, head_length=0.06*diag,
                        linewidth=1, edgecolor="k", facecolor="k")
        # Légende
        import matplotlib.lines as mlines
        traction = mlines.Line2D([], [], color="C3", label="Traction")
        compression = mlines.Line2D([], [], color="C0", label="Compression")
        force_h = mlines.Line2D([], [], color="k", label="Forces / Réactions")
        appui_f = mlines.Line2D([], [], color="k", marker="s", linestyle="None", markersize=8,
                                markerfacecolor="none", label="Appui fixe")
        appui_x = mlines.Line2D([], [], color="k", marker="^", linestyle="None", markersize=8,
                                markerfacecolor="none", label="Appui roulant x")
        appui_y = mlines.Line2D([], [], color="k", marker=">", linestyle="None", markersize=8,
                                markerfacecolor="none", label="Appui roulant y")
        plt.legend(handles=[traction, compression, force_h, appui_f, appui_x, appui_y], loc="best")


        plt.axis("equal")
        plt.title("Treillis - efforts + forces + réactions")
        plt.xlabel("x")
        plt.ylabel("y")

        if parametres.save_plots:
            f1 = out_path / "treillis_forces.png"
            plt.savefig(f1, dpi=200, bbox_inches="tight")
            print(f"Figure sauvegardé: {f1}")

        if parametres.show_plots:
            plt.show()
        else:
            plt.close(fig1)


        # Deformee
        fig2 = plt.figure()
        a = parametres.ampli
        xs = np.array([float(nd.pos[0]+a*nd.dpos[0]) for nd in noeuds])
        ys = np.array([float(nd.pos[1]+a*nd.dpos[1]) for nd in noeuds])
        plt.scatter(xs, ys, s=25, color="k")


        # Barres
        for i, b in enumerate(barres):
            p1 = b.n1.pos + a*b.n1.dpos
            p2 = b.n2.pos + a*b.n2.dpos
            n_i = float(N[i])
            couleur = "C3" if n_i >= 0 else "C0"  # traction / compression
            plt.plot([p1[0], p2[0]], [p1[1], p2[1]], color=couleur)

        plt.axis("equal")
        plt.title("Treillis - Deformée")
        plt.xlabel("x")
        plt.ylabel("y")

        if parametres.save_plots:
            f2 = out_path / "treillis_deformee.png"
            plt.savefig(f2, dpi=200, bbox_inches="tight")
            print(f"Figure sauvegardé: {f2}")

        if parametres.show_plots:
            plt.show()
        else:
            plt.close(fig2)