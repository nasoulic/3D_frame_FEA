import numpy as np
import matplotlib.pyplot as plt
from core.visualise_structure import visualize_structure
from core.structure import Structure
from core.beamProperties import BeamProperties

# Beam section properties
E = 210e3   # MPa
G = 81.2e3  # MPa
b = 10      # mm
h = 10      # mm
t = 2       # mm

beam_props = BeamProperties(E, G, b*h, b*h**3/12, h*b**3/12, b, h, t = t)

# --------------------------
# Build the structure
s = Structure()

# Add nodes
n1 = s.add_node(0, 0, 0)
n2 = s.add_node(1000, 0, 0)
n3 = s.add_node(1000, 1000, 0)
n4 = s.add_node(0, 1000, 0)

# Add a beam
s.add_beam(n1, n2, beam_props)
s.add_beam(n2, n3, beam_props)
s.add_beam(n3, n4, beam_props)
s.add_beam(n4, n1, beam_props)

# Add spring
k_spring = 1e6 # N/mm
spring_vector = np.zeros(12)
spring_vector[2] = k_spring  # UZ of node1 (index 2 of first 6 DOFs)
s.add_spring(n1, n3, spring_vector)

# Supports: fix node 1 in all DOFs
s.add_support(n1.id, [0, 1, 2, 3, 4, 5])

# Loads: apply force at node 3
s.add_load(n3.id, [100, 0, 0, 0, 0, 0])  # Fx = 1000 N

# --------------------------
# Solve
U = s.solve()

visualize_structure(s, U)

# --------------------------
# Print nodal displacements
print("\nNodal displacements:")
for i, node in enumerate(s.nodes):
    ux, uy, uz, rx, ry, rz = U[6*i:6*i+6]
    print(f"Node {i}: Ux={ux:.6e} mm, Uy={uy:.6e} mm, Uz={uz:.6e} mm, Rx={rx:.6e} rad, Ry={ry:.6e} rad, Rz={rz:.6e} rad")

plt.show()