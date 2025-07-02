from core.structure import Structure
from core.beamProperties import BeamProperties
import numpy as np

L = 2000  # length in mm
E = 210e3  # MPa (Young's modulus)
G = 81.2e3  # MPa (Shear modulus)
A = 2500  # mm² (50 mm x 50 mm)
Iy = 50*50**3/12  # mm^4 
Iz = 50*50**3/12  # mm^4
J = Iy + Iz  # mm⁴ (torsion)

beamProp = BeamProperties(E, G, A, Iy, Iz)

# Create structure
structure = Structure()

# Add nodes
n1 = structure.add_node(0, 0, 0)
n2 = structure.add_node(L, 0, 0)  # beam along global X
fake_node = structure.add_node(L, 0, 0) 

# Add beam
structure.add_beam(n1, n2, beamProp)

# Add a vertical translational spring at node 2 (UZ only)
k_spring = 1  # N/mm
spring_vector = [0, 0, k_spring, 0, 0, 0]

structure.add_spring(n2, fake_node, spring_vector)  # Spring between node 2 and ground

# Fix all DOFs at node 0
structure.add_support(n1.id, [0,1,2,3,4,5])
structure.add_support(fake_node.id, [0,1,2,3,4,5])

# Apply load: downward force at node 2 in Z-direction
structure.add_load(n2.id, [0, 0, -1000, 0, 0, 0])  # -1000 N in Z

U = structure.solve()
print("Nodal Displacements:")
for i, node in enumerate(structure.nodes):
    ux, uy, uz, rx, ry, rz = U[6*i:6*i+6]
    print(f"Node {i}: Ux={ux:.6e} mm, Uy={uy:.6e} mm, Uz={uz:.6e} mm, Rx={rx:.6e} rad, Ry={ry:.6e} rad, Rz={rz:.6e} rad")

# visualize_structure(structure, U, scale=1)
# animate_deformation(structure, U, scale = 10)

# Get the single beam element
element = structure.elements[0]

# Get node indices of the element
index_i = element.node1.id
index_j = element.node2.id

# Compute internal forces (local coords)
f_local = element.compute_internal_forces(U, index_i, index_j)

# Cross-section params:
# For a 50mm x 50mm square:
c_y = 50 / 2  # 50 mm
c_z = 50 / 2  # 50 mms
c_t = c_y  # approx radius for torsion in square

stresses = element.compute_stresses(f_local, c_y, c_z, c_t)

print("\nStresses at node 1:")
for key, value in stresses.items():
    print(f"{key}: {value:.3e} MPa")