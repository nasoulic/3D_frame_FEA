import numpy as np

class SpringElement3D:
    def __init__(self, node1, node2, stiffness_vector):
        """
        stiffness_vector: array-like of 12 stiffness values (N/m or Nm/rad), corresponding to DOFs
                          [UX1, UY1, UZ1, RX1, RY1, RZ1, UX2, UY2, UZ2, RX2, RY2, RZ2]
        """
        self.node1 = node1
        self.node2 = node2
        self.k_local = np.diag(stiffness_vector)  # 12x12 diagonal stiffness matrix

        # No transformation needed — local = global
        self.k_global = self.k_local

    def get_dof_indices(self):
        return self.node1.dofs + self.node2.dofs
