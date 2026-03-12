import numpy as np

class Noeud:
    def __init__(self, index: int, pos: np.ndarray, force: np.ndarray, ux: bool, uy: bool):
        self.id = index
        self.pos = pos
        self.force = force
        self.ux = ux
        self.uy = uy

class Barre:
    def __init__(self, index: int, n1: Noeud, n2: Noeud):
        self.id = index
        self.n1 = n1
        self.n2 = n2
        self.len = np.linalg.norm(n2.pos - n1.pos)