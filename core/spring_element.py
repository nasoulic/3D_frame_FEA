import numpy as np

class SpringElement3D:
    def __init__(self, node1, node2, stiffness_vector):
        """
        stiffness_vector: array-like of 12 stiffness values (N/mm or Nm/rad)
                          [UX1, UY1, UZ1, RX1, RY1, RZ1, UX2, UY2, UZ2, RX2, RY2, RZ2]
                          Only the first 6 matter — you only need to define one side.
        """
        self.node1 = node1
        self.node2 = node2
        self.stiffness_vector = stiffness_vector

        # Initialize 12x12 zero matrix
        k = np.zeros((12, 12))

        # For each DOF in node1, add the pair-wise spring terms
        for i in range(6):  # 0..5 for node1
            k_value = stiffness_vector[i]
            if k_value != 0.0:
                # Coupled stiffness for this DOF
                k[i, i] =  k_value
                k[i, i+6] = -k_value
                k[i+6, i] = -k_value
                k[i+6, i+6] =  k_value

        self.k_local = k
        self.k_global = self.k_local

    def get_dof_indices(self):
        return self.node1.dofs + self.node2.dofs
