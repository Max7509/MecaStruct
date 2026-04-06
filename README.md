# Solveur de treillis isostatiques

Code calculant les forces dans les barres d'un treillis isostatique 
et les réactions aux supports.

Le code prend en entrée un fichier `.txt` décrivant le système 
(positions des nœuds, forces extérieures, types d'attaches et 
connectivité des barres). Il produit deux fichiers `.csv` et deux 
images `.png`. Les `.png` montrent un schéma du treillis avec une 
interprétation graphique des résultats (efforts et déformée), et les 
`.csv` donnent un tableau détaillé des informations de chaque barre 
et de chaque nœud.

Le fichier `Rapport_MecaStruct.pdf` fait un rapport du projet et contient notamment des explications sur le format du fichier `.txt` d'entrée.
## Environnement virtuel

Ce projet utilise Python 3. Il est recommandé d'utiliser un 
environnement virtuel pour isoler les dépendances du projet de 
votre installation Python globale.

Pour créer et activer l'environnement virtuel :
```bash
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement (Linux / macOS)
source venv/bin/activate

# Activer l'environnement (Windows)
venv\Scripts\activate
```

Puis installer les dépendances :
```bash
pip install -r requirements.txt
```

Pour désactiver l'environnement virtuel une fois le travail terminé :
```bash
deactivate
```

## Utilisation
```bash
python main.py exemple.txt
```


## Exemples

Trois exemples sont fournis dans le dossier `exemples/` :
- `exemple0.txt` : cas trivial à une barre
- `exemple1.txt` : cas trivial à plusieurs barres
- `exemple2.txt` : simplification d'un pont en arche
