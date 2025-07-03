from core.node import Node
from core.beam import BeamElement3D
from core.spring_element import SpringElement3D
from core.RBE2 import RBE2Element
from core.RBE3 import RBE3Element
from core.RigidElement import RigidElement
import numpy as np

class Structure:
    def __init__(self):
        self.nodes = []
        self.elements = []
        self.spring_elements = []
        self.rbe2_elements = []
        self.rbe3_elements = []
        self.rigid_elements = []
        self.loads = {}       # node_id: [Fx, Fy, Fz, Mx, My, Mz]
        self.supports = {}    # node_id: [fixed_dofs]

    def getNodeById(self, id):
        return next((item for item in self.nodes if item.id == id))

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

    def add_rbe2(self, master_node, slave_nodes):
        rbe2 = RBE2Element(master_node, slave_nodes)
        self.rbe2_elements.append(rbe2)

    def add_rbe3(self, master_node, slave_nodes, weights = None):
        rbe3 = RBE3Element(master_node, slave_nodes, weights)
        self.rbe3_elements.append(rbe3)

    def add_rigid(self, node1, node2):
        rigid = RigidElement(node1, node2)
        self.rigid_elements.append(rigid)

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

        # Standard supports
        for nid, dofs in self.supports.items():
            constrained_dofs.extend([6 * nid + dof for dof in dofs])

        # --- Add RBE2 constraints ---
        for rbe2 in self.rbe2_elements:
            constraints = rbe2.assemble_constraint_matrix()
            for master_dof, slave_dof in constraints:
                # Constrain slave_dof equal to master_dof
                K[slave_dof, :] = 0.0
                K[:, slave_dof] = 0.0
                K[slave_dof, slave_dof] = 1.0
                F[slave_dof] = 0.0

                K[slave_dof, master_dof] = -1.0
                K[master_dof, slave_dof] = -1.0

        # --- Add RBE3 constraints ---
        for rbe3 in self.rbe3_elements:
            constraints = rbe3.assemble_constraint_matrix()
            for master_dof, slave_info in constraints:
                for slave_dof, weight in slave_info:
                    K[master_dof, slave_dof] += -weight
                    K[slave_dof, master_dof] += -weight

        # --- Add Rigid elements constraints ---
        for rigid in self.rigid_elements:
            constraints = rigid.assemble_constraint_matrix()
            for dof1, dof2 in constraints:
                K[dof1, :] = 0.0
                K[:, dof1] = 0.0
                K[dof1, dof1] = 1.0
                F[dof1] = 0.0

                K[dof1, dof2] = -1.0
                K[dof2, dof1] = -1.0

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
