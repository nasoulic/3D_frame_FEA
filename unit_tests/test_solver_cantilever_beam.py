import unittest
import numpy as np
from core.beam import BeamElement3D
from core.beamProperties import BeamProperties
from core.node import Node
from core.structure import Structure

class TestBeamElement3D(unittest.TestCase):

    def setUp(self):
        # Beam properties
        beamProp = BeamProperties(210e9, 81e9, 0.003, 5.2e-7, 5.2e-7, 1.0e-6)

        # Simple horizontal beam, 2m span
        self.node1 = Node(0, 0, 0, 0)
        self.node2 = Node(1, 0, 0, 2.0)

        self.beam = BeamElement3D(self.node1, self.node2, beamProp)

    def test_length_and_direction(self):
        self.assertAlmostEqual(self.beam.length, 2.0)
        np.testing.assert_array_almost_equal(self.beam.direction_cosines, np.array([0, 0, 1]))

    def test_local_stiffness_symmetry(self):
        k_local = self.beam.k_local
        np.testing.assert_array_almost_equal(k_local, k_local.T)

    def test_transformation_orthogonality(self):
        R = self.beam.T[:3, :3]
        I = np.eye(3)
        np.testing.assert_array_almost_equal(R.T @ R, I, decimal=6)

class TestStructureSolve(unittest.TestCase):

    def setUp(self):
        self.structure = Structure()

        # Beam properties
        beamProp = BeamProperties(210e9, 81e9, 0.003, 5.2e-7, 5.2e-7, 1.0e-6)

        # Create nodes
        n0 = self.structure.add_node(0, 0, 0)
        n1 = self.structure.add_node(2.0, 0, 0)

        self.structure.add_beam(n0, n1, beamProp)

        # Cantilever support at node 0
        self.structure.add_support(0, [0, 1, 2, 3, 4, 5])

        # Load at node 1: vertical force -1000N in Z
        self.structure.add_load(1, [0, 0, -1000, 0, 0, 0])

        self.expected_uz = -0.024381
        self.expected_ry = 0.018286

    def test_solver_results(self):
        U = self.structure.solve()
        uz = U[6 + 2]  # Node 1, displacement Z
        ry = U[6 + 4]  # Node 1, rotation Y

        self.assertAlmostEqual(uz, self.expected_uz, delta=1e-4)
        self.assertAlmostEqual(ry, self.expected_ry, delta=1e-4)