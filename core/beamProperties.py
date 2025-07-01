class BeamProperties:
    def __init__(self, E, G, A, Iy, Iz, b = None, h = None, r = None, t = None):
        """
        Initializes a 3D beam element.

        Parameters:
        - E: Young's modulus (MPa)
        - G: Shear modulus (MPa)
        - A: Cross sectional Area (mm2)
        - Iy: Moment of inertia - y axis
        - Iz: Moment of inertia - z axis
        - b: Beam width (mm)
        - h: Beam height (mm)
        - r: Circle radius (mm)
        - t: Thickness (mm)
        """
        self.E = E 
        self.G = G
        self.A = A
        self.Iy = Iy
        self.Iz = Iz
        self.J = Iy + Iz
        self.b = b
        self.h = h
        self.r = r
        self.t = t