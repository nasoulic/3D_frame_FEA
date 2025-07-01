def calculate_stress(structure, U, filename="stresses_output.dat"):
    """
    Calculates stresses for each element and exports the results to a text file.

    Parameters:
    - structure: the structure object with elements and nodes
    - U: global displacement vector
    - h, b: cross-section dimensions (height and width)
    - filename: output text file name
    """
    with open(filename, "w") as f:
        for i, element in enumerate(structure.elements):
            index_i = element.node1.id
            index_j = element.node2.id

            # Compute internal forces (local coords)
            f_local = element.compute_internal_forces(U, index_i, index_j)

            # Cross-section params
            c_y = element.h / 2
            c_z = element.b / 2
            c_t = c_y  # approximate radius for torsion in square

            stresses = element.compute_stresses(f_local, c_y, c_z, c_t)

            f.write(f"\nStresses at element {i+1}:\n")
            for key, value in stresses.items():
                f.write(f"{key}: {value:.3e} MPa\n")
