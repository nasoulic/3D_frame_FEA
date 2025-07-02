class BeamProperties:

    def __init__(self, E, G, A, Iy, Iz, b = None, h = None, r = None, t = None, name = None):
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
        self.name = name

    def export_data(self):
        """
        Export beam properties to a .dat file.
        """
        with open("{0}_{1}.dat".format(self.name, "properties"), 'w') as f:
            f.write(f"t = {self.name}  # Name \n")
            f.write(f"E = {self.E}  # Young's modulus (MPa)\n")
            f.write(f"G = {self.G}  # Shear modulus (MPa)\n")
            f.write(f"A = {self.A}  # Cross sectional Area (mm2)\n")
            f.write(f"Iy = {self.Iy}  # Moment of inertia - y axis\n")
            f.write(f"Iz = {self.Iz}  # Moment of inertia - z axis\n")
            f.write(f"J = {self.J}  # Torsional constant (Iy + Iz)\n")
            f.write(f"b = {self.b}  # Beam width (mm)\n")
            f.write(f"h = {self.h}  # Beam height (mm)\n")
            f.write(f"r = {self.r}  # Circle radius (mm)\n")
            f.write(f"t = {self.t}  # Thickness (mm)\n")
        f.close()