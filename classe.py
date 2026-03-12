import numpy as np

class Noeud:
    def __init__(self, index: int, pos: np.ndarray, force: np.ndarray, ux: bool, uy: bool):
        self.id = index
        self.pos = pos
        self.dpos = np.array([0.0, 0.0])
        self.force = force
        self.ux = ux
        self.uy = uy

class Barre:
    def __init__(self, index: int, n1: Noeud, n2: Noeud, EA: float):
        self.id = index
        self.n1 = n1
        self.n2 = n2
        self.len = np.linalg.norm(n2.pos - n1.pos)
        self.dl = 0
        self.EA = EA

class Parametres:
    def __init__(self, out_dir: str | Path, save_csv: bool, save_plots: bool, show_plots: bool, ampli: float):
        self.out_dir = out_dir
        self.save_csv = save_csv
        self.save_plots = save_plots
        self.show_plots = show_plots
        self.ampli = ampli
    