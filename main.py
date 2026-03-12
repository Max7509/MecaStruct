import numpy as np
import lecture_data as ld
import argparse
from fonctions_resolution import resolution
import rendu_resultats as rr


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Chemin vers le fichier .txt de données du treillis")
    args = parser.parse_args()

    noeuds, barres, parametres = ld.lecture_data(args.path)
    
    solution = resolution(noeuds, barres)
    
    rr.print_resultats(solution, noeuds, barres, parametres)


if __name__ == "__main__":
    main()