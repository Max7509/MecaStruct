# Solveur de treillis isostatiques

Code calculant les forces dans les barres d'un treillis isostatique 
et les réactions aux supports.

Le code prend en entrée un fichier `.txt` décrivant le système 
(positions des nœuds, forces extérieures, types d'attaches et 
connectivité des barres). Il produit deux fichiers `.csv` et deux 
images `.png`. Les `.png` montrent un schéma du treillis avec une 
interprétation graphique des résultats (efforts et déformée), et les 
`.csv` donnent un tableau détaillé des informations de chaque barre 
et de chaque nœud. Le dossier PdeMecaStruct contient le code en java d'une version plus simples (sans les déformations) mais avec une interface graphique. Elle est utilisables directement avec l'IDE Processing.

Le fichier `Rapport_MecaStruct.pdf` fait un rapport du projet et contient notamment des explications sur le format du fichier `.txt` d'entrée.
## Environnement virtuel

Ce projet utilise Python 3. Il utilise les librairies suivantes :
`import numpy as np`

`import lecture_data as ld`

`import argparse`

`from pathlib import Path`

`from __future__ import annotations`

`import matplotlib.pyplot as plt`

`import csv`

## Exemples

Trois exemples sont fournis :
- `exemple0.txt` : cas trivial à une barre
- `exemple1.txt` : cas trivial à plusieurs barres
- `exemple2.txt` : simplification d'un pont en arche
Le dossier `outputs` donne les résultats de l'`exemple2.txt`.
