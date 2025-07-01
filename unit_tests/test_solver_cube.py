import unittest
import numpy as np
from structure import Structure  

class TestCubeStructure(unittest.TestCase):

    def setUp(self):
        self.structure = Structure()

        # Material and cross-section
        E = 210e9  # Pa
        G = 80e9   # Pa
        A = 5e-4   # m^2
        Iy = 1e-6  # m^4
        Iz = 1e-6  # m^4
        J = 2e-6   # m^4

        # Create cube nodes (8 corners)
        coords = [
            (0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0),
            (0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1),
        ]
        self.nodes = [self.structure.add_node(*c) for c in coords]

        # Define beam connections for cube edges
        edges = [
            (0,1), (1,2), (2,3), (3,0),  # bottom face
            (4,5), (5,6), (6,7), (7,4),  # top face
            (0,4), (1,5), (2,6), (3,7),  # vertical edges
        ]

        for i, j in edges:
            self.structure.add_beam(self.nodes[i], self.nodes[j], E, G, A, Iy, Iz, J)

        # Supports: fix all 6 DOFs of bottom nodes
        for nid in [0, 1, 2, 3]:
            self.structure.add_support(nid, [0, 1, 2, 3, 4, 5])

        # Apply vertical load on top center node (between nodes 4–7)
        center_z_node = self.structure.add_node(0.5, 0.5, 1.0)
        for i in [4, 5, 6, 7]:
            self.structure.add_beam(self.nodes[i], center_z_node, E, G, A, Iy, Iz, J)
        self.structure.add_load(center_z_node.id, [0, 0, -1000.0, 0, 0, 0])

        self.center_node = center_z_node

    def test_cube_deflection(self):
        U = self.structure.solve()

        uz = U[6 * self.center_node.id + 2]  # UZ
        print(f"Vertical displacement of top center node: {uz:.6e} m")

        # Based on manual estimation or prior known good result
        self.assertTrue(uz < 0, "Node should move downward under load.")
        self.assertAlmostEqual(uz, -6.62e-6, delta=5e-6)

if __name__ == '__main__':
    unittest.main()
