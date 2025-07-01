import numpy as np

class BeamElement3D:

    def __init__(self, node1, node2, beam_properties):
        self.node1 = node1
        self.node2 = node2
        self.E = beam_properties.E      # Young's modulus
        self.G = beam_properties.G      # Shear modulus
        self.A = beam_properties.A      # Cross-sectional area
        self.Iy = beam_properties.Iy    # Moment of inertia about y
        self.Iz = beam_properties.Iz    # Moment of inertia about z
        self.J = beam_properties.J      # Torsional constant
        self.b = beam_properties.b      # Beam width
        self.h = beam_properties.h      # Beam height
        self.r = beam_properties.r      # Beam radius
        self.t = beam_properties.t      # Beam thickness

        self.length, self.direction_cosines = self._compute_geometry()
        self.k_local = self._compute_local_stiffness()
        self.T = self._compute_transformation_matrix()
        self.k_global = self.T.T @ self.k_local @ self.T

    def _compute_geometry(self):
        delta = self.node2.coords - self.node1.coords
        L = np.linalg.norm(delta)
        l = delta / L
        return L, l

    def _compute_local_stiffness(self):
        E, G = self.E, self.G
        A, Iy, Iz, J = self.A, self.Iy, self.Iz, self.J
        L = self.length

        L2 = L ** 2
        L3 = L ** 3

        k = np.zeros((12, 12))

        # Axial stiffness
        k[0, 0] = k[6, 6] = E * A / L
        k[0, 6] = k[6, 0] = -E * A / L

        # Torsional stiffness
        k[3, 3] = k[9, 9] = G * J / L
        k[3, 9] = k[9, 3] = -G * J / L

        # Bending about Z-axis (Y-direction displacement)
        k[1, 1] = k[7, 7] = 12 * E * Iz / L3
        k[1, 7] = k[7, 1] = -12 * E * Iz / L3
        k[1, 5] = k[5, 1] = 6 * E * Iz / L2
        k[1,11] = k[11,1] = 6 * E * Iz / L2
        k[5, 7] = k[7, 5] = -6 * E * Iz / L2
        k[5,11] = k[11,5] = 2 * E * Iz / L
        k[11,7] = k[7,11] = -6 * E * Iz / L2
        k[11,11] = 4 * E * Iz / L
        k[5, 5] = 4 * E * Iz / L  # Added diagonal term for rotation θz

        # Bending about Y-axis (Z-direction displacement)
        k[2, 2] = k[8, 8] = 12 * E * Iy / L3
        k[2, 8] = k[8, 2] = -12 * E * Iy / L3
        k[2, 4] = k[4, 2] = -6 * E * Iy / L2
        k[2,10] = k[10,2] = -6 * E * Iy / L2
        k[4, 8] = k[8, 4] = 6 * E * Iy / L2
        k[4,10] = k[10,4] = 2 * E * Iy / L
        k[10,8] = k[8,10] = 6 * E * Iy / L2
        k[10,10] = 4 * E * Iy / L
        k[4, 4] = 4 * E * Iy / L  # Added diagonal term for rotation θy

        return k

    def _compute_transformation_matrix(self):
        x_local = self.direction_cosines  # already unit vector from node1 to node2

        # Choose a global reference for local y axis (try global Z)
        global_z = np.array([0, 0, 1])
        if np.allclose(x_local, global_z) or np.allclose(x_local, -global_z):
            # If beam is vertical, use global Y to avoid zero cross product
            global_z = np.array([0, 1, 0])

        z_local = np.cross(x_local, global_z)
        z_local /= np.linalg.norm(z_local)

        y_local = np.cross(z_local, x_local)
        y_local /= np.linalg.norm(y_local)

        # 3x3 rotation matrix from local to global coords
        R = np.vstack((x_local, y_local, z_local)).T  # shape (3,3)

        # Build 12x12 transformation matrix
        T = np.zeros((12, 12))
        for i in range(4):  # 4 blocks: [disp_node1, rot_node1, disp_node2, rot_node2]
            T[i*3:(i+1)*3, i*3:(i+1)*3] = R

        return T

    def get_dof_indices(self, index_i, index_j):
        return [index_i*6 + i for i in range(6)] + [index_j*6 + i for i in range(6)]
    
    def compute_internal_forces(self, u_global, index_i, index_j):
        """
        Compute internal local forces and moments in the element.
        u_global: full global displacement vector
        index_i, index_j: global node indices of the element
        Returns: local internal force vector (12x1)
        """
        dofs = self.get_dof_indices(index_i, index_j)
        u_e_global = u_global[dofs]  # element displacement in global coords (12,)
        u_e_local = self.T @ u_e_global  # transform to local coords

        # internal force in local coords: f_local = k_local * u_local
        f_local = self.k_local @ u_e_local

        return f_local  # 12x1 vector: axial, shear, moments, torsion in local DOFs
    
    def compute_stresses(self, f_local, c_y, c_z, c_t):
        # Axial force
        N = f_local[0]
        sigma_axial = N / self.A
        
        # Bending moments at node1
        M_y = f_local[4]
        M_z = f_local[5]
        
        sigma_b_y = - M_z * c_y / self.Iz
        sigma_b_z = M_y * c_z / self.Iy
        
        # Torsional moment
        T = f_local[3]
        tau = T * c_t / self.J
        
        # Total normal stress (axial + bending)
        sigma_total = np.sqrt(sigma_b_y**2 + sigma_b_z**2)
        
        return {
            'sigma_axial': sigma_axial,
            'sigma_bending_y': sigma_b_y,
            'sigma_bending_z': sigma_b_z,
            'tau_torsion': tau,
            'sigma_total': sigma_total
        }