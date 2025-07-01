from structure import Structure
from beamProperties import BeamProperties
import numpy as np
from visualise_structure import visualize_structure
from evaluate_stress import calculate_stress
from export_nodal_diaplacements import export_nodal_displacements
from visualise_stress import plot_stress_distribution
from visualize_forces import plot_bending_shear_diagrams
from animate_deformation import animate_deformation

# Fork Cross-Section
E = 210e3  # MPa (Young's modulus)
G = 81.2e3  # MPa (Shear modulus)
b = 50 # mm
h = 50 # mm
t = 3 # mm
A = b*h - (h-2*t)*(b-2*t) # m2
Iy = b*h**3/12 # m4
Iz = b**3*h/12 # m4

fork_beam = BeamProperties(E, G, A, Iy, Iz)

# Create structure
agv_fork_structure = Structure()

# Add nodes
n1 = agv_fork_structure.add_node(0, 0, 0)
n2 = agv_fork_structure.add_node(-70, 70, 0)
n3 = agv_fork_structure.add_node(-282.84, 282.84, 0)
n4 = agv_fork_structure.add_node(-55, 510.69, 0)
n5 = agv_fork_structure.add_node(0, 565.69, 0)
n6 = agv_fork_structure.add_node(0, 0, 143)
n7 = agv_fork_structure.add_node(-70, 70, 143)
n8 = agv_fork_structure.add_node(-282.84, 282.84, 143)
n9 = agv_fork_structure.add_node(-55, 510.69, 143)
n10 = agv_fork_structure.add_node(0, 565.69, 143)

# Add beam
agv_fork_structure.add_beam(n1, n2, fork_beam.E, fork_beam.G, fork_beam.A, fork_beam.Iy, fork_beam.Iz, fork_beam.J)
agv_fork_structure.add_beam(n2, n3, fork_beam.E, fork_beam.G, fork_beam.A, fork_beam.Iy, fork_beam.Iz, fork_beam.J)
agv_fork_structure.add_beam(n3, n4, fork_beam.E, fork_beam.G, fork_beam.A, fork_beam.Iy, fork_beam.Iz, fork_beam.J)
agv_fork_structure.add_beam(n4, n5, fork_beam.E, fork_beam.G, fork_beam.A, fork_beam.Iy, fork_beam.Iz, fork_beam.J)
agv_fork_structure.add_beam(n6, n7, fork_beam.E, fork_beam.G, fork_beam.A, fork_beam.Iy, fork_beam.Iz, fork_beam.J)
agv_fork_structure.add_beam(n7, n8, fork_beam.E, fork_beam.G, fork_beam.A, fork_beam.Iy, fork_beam.Iz, fork_beam.J)
agv_fork_structure.add_beam(n8, n9, fork_beam.E, fork_beam.G, fork_beam.A, fork_beam.Iy, fork_beam.Iz, fork_beam.J)
agv_fork_structure.add_beam(n9, n10, fork_beam.E, fork_beam.G, fork_beam.A, fork_beam.Iy, fork_beam.Iz, fork_beam.J)
# agv_fork_structure.add_beam(n8, n3, fork_beam.E, fork_beam.G, fork_beam.A, fork_beam.Iy, fork_beam.Iz, fork_beam.J)
agv_fork_structure.add_beam(n5, n10, fork_beam.E, fork_beam.G, fork_beam.A, fork_beam.Iy, fork_beam.Iz, fork_beam.J)

# Add spring
k_spring = 6 # N/mm
spring_vector = np.zeros(12)
spring_vector[2] = k_spring  # UZ of node1 (index 2 of first 6 DOFs)

agv_fork_structure.add_spring(n2, n4, spring_vector)
agv_fork_structure.add_spring(n7, n9, spring_vector)

# Fix all DOFs at node 5 and node 10
agv_fork_structure.add_support(n5.id, [0,1,2,3,4,5])
agv_fork_structure.add_support(n10.id, [0,1,2,3,4,5])

# Apply load
agv_fork_structure.add_load(n1.id, [0, 1800, 0, 0, 0, 0])
agv_fork_structure.add_load(n6.id, [0, 1800, 0, 0, 0, 0])

visualize_structure(agv_fork_structure, scale = 10)

U = agv_fork_structure.solve()

export_nodal_displacements(agv_fork_structure, U)

visualize_structure(agv_fork_structure, U, scale = 10)
# # plot_bending_shear_diagrams(agv_fork_structure, U)
# animate_deformation(agv_fork_structure, U, scale = 10)

calculate_stress(agv_fork_structure, U, h, b)

plot_stress_distribution(agv_fork_structure, U, h, b, stress_component = "sigma_axial")
plot_stress_distribution(agv_fork_structure, U, h, b, stress_component = "sigma_bending_y")
plot_stress_distribution(agv_fork_structure, U, h, b, stress_component = "sigma_bending_z")
plot_stress_distribution(agv_fork_structure, U, h, b, stress_component = "tau_torsion")
plot_stress_distribution(agv_fork_structure, U, h, b, stress_component = "sigma_total")