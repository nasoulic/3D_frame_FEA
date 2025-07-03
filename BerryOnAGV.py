from core.FEA_3D_code_wrapper import FEA_wrapper
import os 

i = 0
flag = True
while flag:
       if not os.path.exists("./res{0}".format(i)):
              os.mkdir("./res{0}".format(i))
              i += 1
              flag = False
       else:
              i += 1
os.chdir("./res{0}".format(i-1))

berryOnAGV = FEA_wrapper()

# Fork Cross-Section
E = 210e3  # MPa (Young's modulus)
G = 81.2e3  # MPa (Shear modulus)
b = 40 # mm
h = 40 # mm
t = 3 # mm
A = b*h - (h-2*t)*(b-2*t) # m2
Iy = b*h**3/12 # m4
Iz = b**3*h/12 # m4

berryOnAGV.defineBeamProperty(E, G, A, Iy, Iz, b, h, t = t, name = "fork")

# Fork Pivot Cross-Section
E = 210e3  # MPa (Young's modulus)
G = 81.2e3  # MPa (Shear modulus)
b = 35 # mm
h = 35 # mm
t = 2.5 # mm
A = b*h - (h-2*t)*(b-2*t) # m2
Iy = b*h**3/12 # m4
Iz = b**3*h/12 # m4

berryOnAGV.defineBeamProperty(E, G, A, Iy, Iz, b, h, t = t, name = "fork_pivot")

# Fork 2 Frame Cross-Section
E = 210e3  # MPa (Young's modulus)
G = 81.2e3  # MPa (Shear modulus)
b = 50 # mm
h = 50 # mm
t = 2.5 # mm
A = b*h - (h-2*t)*(b-2*t) # m2
Iy = b*h**3/12 # m4
Iz = b**3*h/12 # m4

berryOnAGV.defineBeamProperty(E, G, A, Iy, Iz, b, h, t = t, name = "fork_to_frame")

# Frame Beam Cross-Section
E = 210e3  # MPa (Young's modulus)
G = 81.2e3  # MPa (Shear modulus)
b = 50 # mm
h = 50 # mm
t = 2.5 # mm
A = b*h - (h-2*t)*(b-2*t) # m2
Iy = b*h**3/12 # m4
Iz = b**3*h/12 # m4

berryOnAGV.defineBeamProperty(E, G, A, Iy, Iz, b, h, t = t, name = "frame")

# Frame Traverse Beam Cross-Section
E = 210e3  # MPa (Young's modulus)
G = 81.2e3  # MPa (Shear modulus)
b = 50 # mm
h = 50 # mm
t = 3 # mm
A = b*h - (h-2*t)*(b-2*t) # m2
Iy = b*h**3/12 # m4
Iz = b**3*h/12 # m4

berryOnAGV.defineBeamProperty(E, G, A, Iy, Iz, b, h, t = t, name = "frame_traverse")

berryOnAGV.loadFrameNodes()
berryOnAGV.loadFrameBeams()
berryOnAGV.addSpringElements([0, 6, 0, 0, 0, 0])

# Flexural test SPCs
spc_nodes = [berryOnAGV.frameStructure.getNodeById(22), berryOnAGV.frameStructure.getNodeById(26), 
            berryOnAGV.frameStructure.getNodeById(49), berryOnAGV.frameStructure.getNodeById(53)]
    
constrained_dofs = [[1, 3, 4, 5], [1, 3, 4, 5],
                    [0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5]]

lc_nodes = [berryOnAGV.frameStructure.getNodeById(0), berryOnAGV.frameStructure.getNodeById(5), 
            berryOnAGV.frameStructure.getNodeById(38), berryOnAGV.frameStructure.getNodeById(42)]

lcs = [[0, 1000, 0, 0, 0, 0], [0, 1000, 0, 0, 0, 0],
       [0, 1000, 0, 0, 0, 0], [0, 1000, 0, 0, 0, 0]]

berryOnAGV.addConstraints(spc_nodes, constrained_dofs)
berryOnAGV.addLoads(lc_nodes, lcs)

berryOnAGV.solve()
berryOnAGV.exportResults("flexuralTest")

berryOnAGV.clearBCs([spc_nodes, constrained_dofs, lc_nodes, lcs])

# Skid Steering SPCs
spc_nodes = [berryOnAGV.frameStructure.getNodeById(0), berryOnAGV.frameStructure.getNodeById(5), 
            berryOnAGV.frameStructure.getNodeById(22), berryOnAGV.frameStructure.getNodeById(26),
            berryOnAGV.frameStructure.getNodeById(38), berryOnAGV.frameStructure.getNodeById(42), 
            berryOnAGV.frameStructure.getNodeById(49), berryOnAGV.frameStructure.getNodeById(53)]
    
constrained_dofs = [[0, 1], [0, 1],
                    [0, 1, 2], [0, 1, 2],
                    [1, 2], [1, 2],
                    [1], [1]]

lc_nodes = [berryOnAGV.frameStructure.getNodeById(0), berryOnAGV.frameStructure.getNodeById(5), 
            berryOnAGV.frameStructure.getNodeById(38), berryOnAGV.frameStructure.getNodeById(42),
            berryOnAGV.frameStructure.getNodeById(22), berryOnAGV.frameStructure.getNodeById(26), 
            berryOnAGV.frameStructure.getNodeById(49), berryOnAGV.frameStructure.getNodeById(53)]

lcs = [[230, 0, 644, 0, 0, 0], [230, 0, 644, 0, 0, 0],
       [-230, 0, 243, 0, 0, 0], [-230, 0, 243, 0, 0, 0],
       [230, 0, -861, 0, 0, 0], [230, 0, -861, 0, 0, 0], 
       [-230, 0, -460, 0, 0, 0], [-230, 0, -460, 0, 0, 0]]

berryOnAGV.addConstraints(spc_nodes, constrained_dofs)
berryOnAGV.addLoads(lc_nodes, lcs)

berryOnAGV.solve()
berryOnAGV.exportResults("skidSteering")

berryOnAGV.clearBCs([spc_nodes, constrained_dofs, lc_nodes, lcs])

# Vertical Bump SPCs
spc_nodes = [berryOnAGV.frameStructure.getNodeById(22), berryOnAGV.frameStructure.getNodeById(26),
            berryOnAGV.frameStructure.getNodeById(38), berryOnAGV.frameStructure.getNodeById(42), 
            berryOnAGV.frameStructure.getNodeById(49), berryOnAGV.frameStructure.getNodeById(53)]
    
constrained_dofs = [[1], [1],
                    [1, 2], [1, 2],
                    [0, 1, 2], [0, 1, 2]]

lc_nodes = [berryOnAGV.frameStructure.getNodeById(0), berryOnAGV.frameStructure.getNodeById(5)]

lcs = [[0, 2000, 0, 0, 0, 0], [0, 2000, 0, 0, 0, 0]]

berryOnAGV.addConstraints(spc_nodes, constrained_dofs)
berryOnAGV.addLoads(lc_nodes, lcs)

berryOnAGV.solve()
berryOnAGV.exportResults("verticalBump")

berryOnAGV.clearBCs([spc_nodes, constrained_dofs, lc_nodes, lcs])

# Torsional Twist SPCs
berryOnAGV.frameStructure.spring_elements.clear()
berryOnAGV.addSpringElements([0, 1e12, 0, 0, 0, 0])

spc_nodes = [berryOnAGV.frameStructure.getNodeById(22), berryOnAGV.frameStructure.getNodeById(26), 
            berryOnAGV.frameStructure.getNodeById(49), berryOnAGV.frameStructure.getNodeById(53)]
    
constrained_dofs = [[1, 3, 4, 5], [1, 3, 4, 5],
                    [0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5]]

lc_nodes = [berryOnAGV.frameStructure.getNodeById(0), berryOnAGV.frameStructure.getNodeById(5), 
            berryOnAGV.frameStructure.getNodeById(38), berryOnAGV.frameStructure.getNodeById(42)]

lcs = [[0, -500, 0, 0, 0, 0], [0, -500, 0, 0, 0, 0],
       [0, 500, 0, 0, 0, 0], [0, 500, 0, 0, 0, 0]]

berryOnAGV.addConstraints(spc_nodes, constrained_dofs)
berryOnAGV.addLoads(lc_nodes, lcs)

berryOnAGV.solve()
berryOnAGV.exportResults("torsionalTest")

berryOnAGV.clearBCs([spc_nodes, constrained_dofs, lc_nodes, lcs])

berryOnAGV.createReport()