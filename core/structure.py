from core.node import Node
from core.beam import BeamElement3D
from core.spring_element import SpringElement3D
import numpy as np

class Structure:
    def __init__(self):
        self.nodes = []
        self.elements = []
        self.spring_elements = []
        self.loads = {}       # node_id: [Fx, Fy, Fz, Mx, My, Mz]
        self.supports = {}    # node_id: [fixed_dofs]

    def add_node(self, x, y, z):
        node_id = len(self.nodes)
        node = Node(node_id, x, y, z)
        self.nodes.append(node)
        return node

    def add_beam(self, node1, node2, beamProperties):
        element = BeamElement3D(node1, node2, beamProperties)
        self.elements.append(element)

    def add_spring(self, node1, node2, stiffness_vector):
        spring = SpringElement3D(node1, node2, stiffness_vector)
        self.spring_elements.append(spring)

    def add_support(self, node_id, fixed_dofs):
        self.supports[node_id] = fixed_dofs

    def add_load(self, node_id, load_vector):
        self.loads[node_id] = np.array(load_vector)

    def assemble_global_stiffness(self):
        ndof = 6 * len(self.nodes)
        K = np.zeros((ndof, ndof))
        for elem in self.elements:
            dofs = elem.node1.dofs + elem.node2.dofs
            for i in range(12):
                for j in range(12):
                    K[dofs[i], dofs[j]] += elem.k_global[i, j]

        # Add spring element stiffness
        for spring in self.spring_elements:
            dofs = spring.get_dof_indices()
            for i in range(12):
                for j in range(12):
                    K[dofs[i], dofs[j]] += spring.k_global[i, j]

        return K

    def assemble_load_vector(self):
        ndof = 6 * len(self.nodes)
        F = np.zeros(ndof)
        for nid, load in self.loads.items():
            for i in range(6):
                F[6 * nid + i] = load[i]
        return F

    def apply_boundary_conditions(self, K, F):
        constrained_dofs = []
        for nid, dofs in self.supports.items():
            constrained_dofs.extend([6 * nid + dof for dof in dofs])

        free_dofs = list(set(range(K.shape[0])) - set(constrained_dofs))

        K_reduced = K[np.ix_(free_dofs, free_dofs)]
        F_reduced = F[free_dofs]
        return K_reduced, F_reduced, free_dofs

    def solve(self):
        K = self.assemble_global_stiffness()
        F = self.assemble_load_vector()
        K_red, F_red, free_dofs = self.apply_boundary_conditions(K, F)

        U = np.zeros(K.shape[0])
        U_free = np.linalg.solve(K_red, F_red)
        U[free_dofs] = U_free
        return U
