class BeamElement:
    def __init__(self, E, G, A, Iy, Iz):
        """
        Initializes a 3D beam element.

        Parameters:
        - E: Young's modulus (MPa)
        - G: Shear modulus (MPa)
        - A: Cross sectional Area (mm2)
        - Iy: Moment of inertia - y axis
        - Iz: Moment of inertia - z axis
        """
        self.E = E 
        self.G = G
        self.A = A
        self.Iy = Iy
        self.Iz = Iz
        self.J = Iy + Iz