def export_nodal_displacements(structure, U, filename="nodal_displacements.dat"):
    with open(filename, "w") as f:
        f.write("Nodal Displacements:\n")
        for i, node in enumerate(structure.nodes):
            ux, uy, uz, rx, ry, rz = U[6*i:6*i+6]
            f.write(f"Node {i}: Ux={ux:.6e} mm, Uy={uy:.6e} mm, Uz={uz:.6e} mm, "
                    f"Rx={rx:.6e} rad, Ry={ry:.6e} rad, Rz={rz:.6e} rad\n")
    f.close()