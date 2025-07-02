from core.structure import Structure
from core.beamProperties import BeamProperties
import numpy as np
import matplotlib.pyplot as plt
from core.visualise_structure import visualize_structure
from core.evaluate_stress import calculate_stress
from core.export_nodal_diaplacements import export_nodal_displacements
from core.visualise_stress import plot_stress_distribution

# Fork Cross-Section
E = 210e3  # MPa (Young's modulus)
G = 81.2e3  # MPa (Shear modulus)
b = 35 # mm
h = 35 # mm
t = 3 # mm
A = b*h - (h-2*t)*(b-2*t) # m2
Iy = b*h**3/12 # m4
Iz = b**3*h/12 # m4

fork_beams = BeamProperties(E, G, A, Iy, Iz, b, h, t = t)

# Fork Pivot Cross-Section
E = 210e3  # MPa (Young's modulus)
G = 81.2e3  # MPa (Shear modulus)
b = 25 # mm
h = 25 # mm
t = 3 # mm
A = b*h - (h-2*t)*(b-2*t) # m2
Iy = b*h**3/12 # m4
Iz = b**3*h/12 # m4

fork_pivot = BeamProperties(E, G, A, Iy, Iz, b, h, t = t)

# Fork 2 Frame Cross-Section
E = 210e3  # MPa (Young's modulus)
G = 81.2e3  # MPa (Shear modulus)
b = 40 # mm
h = 40 # mm
t = 3 # mm
A = b*h - (h-2*t)*(b-2*t) # m2
Iy = b*h**3/12 # m4
Iz = b**3*h/12 # m4

fork_to_frame = BeamProperties(E, G, A, Iy, Iz, b, h, t = t)

# Frame Beam Cross-Section
E = 210e3  # MPa (Young's modulus)
G = 81.2e3  # MPa (Shear modulus)
b = 50 # mm
h = 50 # mm
t = 2.5 # mm
A = b*h - (h-2*t)*(b-2*t) # m2
Iy = b*h**3/12 # m4
Iz = b**3*h/12 # m4

frame_beam = BeamProperties(E, G, A, Iy, Iz, b, h, t = t)

# Frame Traverse Beam Cross-Section
E = 210e3  # MPa (Young's modulus)
G = 81.2e3  # MPa (Shear modulus)
b = 50 # mm
h = 50 # mm
t = 3 # mm
A = b*h - (h-2*t)*(b-2*t) # m2
Iy = b*h**3/12 # m4
Iz = b**3*h/12 # m4

frame_traverse_beam = BeamProperties(E, G, A, Iy, Iz, b, h, t = t)

# Create frame structure
agv_frame = Structure()

# Add frame nodes
n1 = agv_frame.add_node(0, 0 , 0)
n2 = agv_frame.add_node(85, 57.36, 0)
n3 = agv_frame.add_node(265.25, 179, 0)
n4 = agv_frame.add_node(75, 307.39, 0)
n5 = agv_frame.add_node(0, 358, 0)
n6 = agv_frame.add_node(0, 0 , 155)
n7 = agv_frame.add_node(85, 57.36, 155)
n8 = agv_frame.add_node(265.25, 179, 155)
n9 = agv_frame.add_node(75, 307.39, 155)
n10 = agv_frame.add_node(0, 358, 77.5)
n11 = agv_frame.add_node(0, 358, 155)
n12 = agv_frame.add_node(0, 658, 77.5)
n13 = agv_frame.add_node(-250, 658, 77.5)
n14 = agv_frame.add_node(-585, 658, 77.5)
n15 = agv_frame.add_node(-920, 658, 77.5)
n16 = agv_frame.add_node(-1170, 658, 77.5)
n17 = agv_frame.add_node(-1170, 358, 77.5)
n18 = agv_frame.add_node(-1170, 358, 0)
n19 = agv_frame.add_node(-1170, 358, 155)
n20 = agv_frame.add_node(-1245, 307.39, 0)
n21 = agv_frame.add_node(-1435.25, 179, 0)
n22 = agv_frame.add_node(-1255, 57.36, 0)
n23 = agv_frame.add_node(-1170, 0, 0)
n24 = agv_frame.add_node(-1245, 307.39, 155)
n25 = agv_frame.add_node(-1435.25, 179, 155)
n26 = agv_frame.add_node(-1255, 57.36, 155)
n27 = agv_frame.add_node(-1170, 0, 155)
n28 = agv_frame.add_node(0, 658, 1087)
n29 = agv_frame.add_node(-250, 658, 1087)
n30 = agv_frame.add_node(-585, 658, 1087)
n31 = agv_frame.add_node(-920, 658, 1087)
n32 = agv_frame.add_node(-1170, 658, 1087)
n33 = agv_frame.add_node(0, 358, 1087)
n34 = agv_frame.add_node(-1170, 358, 1087)
n35 = agv_frame.add_node(-1170, 358, 1009.5)
n36 = agv_frame.add_node(0, 358, 1164.5)
n37 = agv_frame.add_node(0, 358, 1009.5)
n38 = agv_frame.add_node(-1170, 358, 1164.5)
n39 = agv_frame.add_node(0, 0 , 1009.5)
n40 = agv_frame.add_node(85, 57.36, 1009.5)
n41 = agv_frame.add_node(265.25, 179, 1009.5)
n42 = agv_frame.add_node(75, 307.39, 1009.5)
n43 = agv_frame.add_node(0, 0 , 1164.5)
n44 = agv_frame.add_node(85, 57.36, 1164.5)
n45 = agv_frame.add_node(265.25, 179, 1164.5)
n46 = agv_frame.add_node(75, 307.39, 1164.5)
n47 = agv_frame.add_node(-1245, 307.39, 1009.5)
n48 = agv_frame.add_node(-1435.25, 179, 1009.5)
n49 = agv_frame.add_node(-1255, 57.36, 1009.5)
n50 = agv_frame.add_node(-1170, 0, 1009.5)
n51 = agv_frame.add_node(-1245, 307.39, 1164.5)
n52 = agv_frame.add_node(-1435.25, 179, 1164.5)
n53 = agv_frame.add_node(-1255, 57.36, 1164.5)
n54 = agv_frame.add_node(-1170, 0, 1164.5)


# Define structural memebers
agv_frame.add_beam(n1, n2, fork_beams)
agv_frame.add_beam(n2, n3, fork_beams)
agv_frame.add_beam(n3, n4, fork_beams)
agv_frame.add_beam(n4, n5, fork_beams)
agv_frame.add_beam(n6, n7, fork_beams)
agv_frame.add_beam(n7, n8, fork_beams)
agv_frame.add_beam(n8, n9, fork_beams)
agv_frame.add_beam(n9, n11, fork_beams)
agv_frame.add_beam(n3, n8, fork_pivot)
agv_frame.add_beam(n5, n10, fork_to_frame)
agv_frame.add_beam(n10, n11, fork_to_frame)
agv_frame.add_beam(n10, n12, fork_to_frame)
agv_frame.add_beam(n12, n13, frame_beam)
agv_frame.add_beam(n13, n14, frame_beam)
agv_frame.add_beam(n14, n15, frame_beam)
agv_frame.add_beam(n15, n16, frame_beam)
agv_frame.add_beam(n16, n17, fork_to_frame)
agv_frame.add_beam(n17, n18, fork_to_frame)
agv_frame.add_beam(n17, n19, fork_to_frame)
agv_frame.add_beam(n18, n20, fork_beams)
agv_frame.add_beam(n19, n24, fork_beams)
agv_frame.add_beam(n20, n21, fork_beams)
agv_frame.add_beam(n21, n22, fork_beams)
agv_frame.add_beam(n22, n23, fork_beams)
agv_frame.add_beam(n24, n25, fork_beams)
agv_frame.add_beam(n25, n26, fork_beams)
agv_frame.add_beam(n26, n27, fork_beams)
agv_frame.add_beam(n21, n25, fork_beams)
agv_frame.add_beam(n12, n28, frame_traverse_beam)
agv_frame.add_beam(n13, n29, frame_traverse_beam)
agv_frame.add_beam(n14, n30, frame_traverse_beam)
agv_frame.add_beam(n15, n31, frame_traverse_beam)
agv_frame.add_beam(n16, n32, frame_traverse_beam)
agv_frame.add_beam(n28, n29, frame_beam)
agv_frame.add_beam(n29, n30, frame_beam)
agv_frame.add_beam(n30, n31, frame_beam)
agv_frame.add_beam(n31, n32, frame_beam)
agv_frame.add_beam(n28, n33, fork_to_frame)
agv_frame.add_beam(n32, n34, fork_to_frame)
agv_frame.add_beam(n33, n36, fork_to_frame)
agv_frame.add_beam(n33, n37, fork_to_frame)
agv_frame.add_beam(n34, n35, fork_to_frame)
agv_frame.add_beam(n34, n38, fork_to_frame)
agv_frame.add_beam(n37, n42, fork_beams)
agv_frame.add_beam(n42, n41, fork_beams)
agv_frame.add_beam(n41, n40, fork_beams)
agv_frame.add_beam(n40, n39, fork_beams)
agv_frame.add_beam(n36, n46, fork_beams)
agv_frame.add_beam(n46, n45, fork_beams)
agv_frame.add_beam(n45, n44, fork_beams)
agv_frame.add_beam(n44, n43, fork_beams)
agv_frame.add_beam(n41, n45, fork_pivot)
agv_frame.add_beam(n35, n47, fork_beams)
agv_frame.add_beam(n47, n48, fork_beams)
agv_frame.add_beam(n48, n49, fork_beams)
agv_frame.add_beam(n49, n50, fork_beams)
agv_frame.add_beam(n38, n51, fork_beams)
agv_frame.add_beam(n51, n52, fork_beams)
agv_frame.add_beam(n52, n53, fork_beams)
agv_frame.add_beam(n53, n54, fork_beams)
agv_frame.add_beam(n48, n52, fork_pivot)

# Add spring elements
k_spring = 6 # N/mm
spring_vector = [0, k_spring, 0, 0, 0, 0]

agv_frame.add_spring(n2, n4, spring_vector)
agv_frame.add_spring(n7, n9, spring_vector)
agv_frame.add_spring(n20, n22, spring_vector)
agv_frame.add_spring(n24, n26, spring_vector)
agv_frame.add_spring(n40, n42, spring_vector)
agv_frame.add_spring(n44, n46, spring_vector)
agv_frame.add_spring(n47, n49, spring_vector)
agv_frame.add_spring(n51, n53, spring_vector)

# Apply constraints for skid steering
agv_frame.add_support(n1.id, [0, 1]) # Constrain xy
agv_frame.add_support(n6.id, [0, 1]) # Constrain xy
agv_frame.add_support(n23.id, [0, 1, 2]) # Constrain xyz
agv_frame.add_support(n27.id, [0, 1, 2]) # Constrain xyz
agv_frame.add_support(n39.id, [1, 2]) # Constrain yz
agv_frame.add_support(n43.id, [1, 2]) # Constrain yz
agv_frame.add_support(n50.id, [1]) # Constrain y
agv_frame.add_support(n54.id, [1]) # Constrain y


# Apply loadcases
agv_frame.add_load(n1.id, [230, 0, 644, 0, 0, 0]) # Front Left Wheel
agv_frame.add_load(n6.id, [230, 0, 644, 0, 0, 0]) # Front Left Wheel
agv_frame.add_load(n39.id, [-230, 0, 243, 0, 0, 0]) # Front Right Wheel
agv_frame.add_load(n43.id, [-230, 0, 243, 0, 0, 0]) # Front Right Wheel
agv_frame.add_load(n23.id, [230, 0, -861, 0, 0, 0]) # Rear Left Wheel
agv_frame.add_load(n27.id, [230, 0, -861, 0, 0, 0]) # Rear Left Wheel
agv_frame.add_load(n50.id, [-230, 0, -460, 0, 0, 0]) # Rear Right Wheel
agv_frame.add_load(n54.id, [-230, 0, -460, 0, 0, 0]) # Rear Right Wheel

# Visualise frame
# visualize_structure(agv_frame)

# Resolve frame
U = agv_frame.solve()

# Write result files
export_nodal_displacements(agv_frame, U, "nodal_displacement_skid_steering.dat")
calculate_stress(agv_frame, U, "stresses_output_skid_steering.dat")

# Visualise results
visualize_structure(agv_frame, U, scale = 10)

plot_stress_distribution(agv_frame, U, stress_component = "sigma_axial", filename = "stress_skid_steering.png")
plot_stress_distribution(agv_frame, U, stress_component = "sigma_bending_y", filename = "stress_skid_steering.png")
plot_stress_distribution(agv_frame, U, stress_component = "sigma_bending_z", filename = "stress_skid_steering.png")
plot_stress_distribution(agv_frame, U, stress_component = "tau_torsion", filename = "stress_skid_steering.png")
plot_stress_distribution(agv_frame, U, stress_component = "sigma_total", filename = "stress_skid_steering.png")

plt.show()