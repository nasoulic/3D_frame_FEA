import numpy as np

class Node:
    def __init__(self, node_id, x, y, z):
        self.id = node_id
        self.coords = np.array([x, y, z], dtype=float)
        self.dofs = [6 * node_id + i for i in range(6)]  # [UX, UY, UZ, RX, RY, RZ]
