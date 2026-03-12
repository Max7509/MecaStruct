# Présentation
Code calculcant les forces dans les barres d'un treillis et les réactions au support.
Le code prend en entrée un fichier .txt avec les informations sur les noeuds (position, forces exterieure et type d'attache) et sur les barres (noeuds de chaque extremités).
Il rend deux .csv et un .png. Le .png montre un schema du treillis et une interpretation graphique des résultats et les .csv donne un tableau avec les informations de chaque barres et chaques noeuds.

# Entrée:
le fichier .txt doit être du format suivant:

"

Noeuds

$x_1$ $y_1$ $fx_1$ $fy_1$ $flag_1$

$x_2$ $y_2$ $fx_2$ $fy_2$ $flag_2$

$x_3$ $y_3$ $fx_3$ $fy_3$ $flag_3$


Barres

$n_0$ $n_1$

$n_1$ $n_2$

$n_2$ $n_0$

"

Avec $x_i$ et $y_i$ les coordonnées des noeuds, $fx_i$ et $fy_i$ la force appliquées sur ces noeuds et $flag_i$ le type d'attache ('f' pour fixe, 'x' pour roulant en y ($x = 0$) et 'y' pour roulant en x ($y = 0$), 'l' pour libre).
Et avec $n_i$ et $n_j$ les noeuds sur lesquelles chaques barres est accrochées. 
Chaque ligne correspond donc à un objet, un noeud dans la partie "Noeuds" et une barre dans la partie "Barre".

# Sur les systèmes
Le système doit être isostatique: 
Pour $n$ noeuds, possedant au total $r$ attaches (pour chaque noeuds $r_i = 0$ pour 'l', $r_i = 1$ pour 'x' ou 'y' et $r_i = 2$ pour 'f'; $r = \sum r_i$),
Et pour $b$ barres, le code ne peut résoudre le programmes que $r + b = 2*n$.

# Exemples
On donne trois exemples, les deux premiers sont des cas triviaux et le derniers et une simplification d'un pont en arche en treillis.
