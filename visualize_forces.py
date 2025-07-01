import matplotlib.pyplot as plt
import numpy as np
import os

def plot_bending_shear_diagrams(structure, U, save_path="bending_moment_diagram.png"):
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_title("Bending Moment and Shear Force Diagrams")
    ax.set_xlabel("Element Midpoint X (m)")
    ax.set_ylabel("Force / Moment")

    mid_xs, shear_forces, bending_moments = [], [], []

    for i, elem in enumerate(structure.elements):
        n1, n2 = elem.node1, elem.node2
        x_mid = 0.5 * (n1.coords[0] + n2.coords[0])
        mid_xs.append(x_mid)

        f_local = elem.compute_internal_forces(U, n1.id, n2.id)

        # Local DOFs:
        # [Ux1, Uy1, Uz1, Rx1, Ry1, Rz1, Ux2, Uy2, Uz2, Rx2, Ry2, Rz2]
        shear_y = f_local[2]   # Shear in local Z (usually bending about Y)
        moment_y = f_local[4]  # Moment about local Y (bending around Z axis)

        shear_forces.append(shear_y)
        bending_moments.append(moment_y)

    ax.plot(mid_xs, shear_forces, 'b-o', label='Shear Force (Z dir)')
    ax.plot(mid_xs, bending_moments, 'r-o', label='Bending Moment (Y axis)')
    ax.legend()
    ax.grid(True)

    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
    return os.path.abspath(save_path)
