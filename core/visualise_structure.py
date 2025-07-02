import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def visualize_structure(structure, displacements=None, show_forces=True, show_supports=True,
                        show_internal_forces=False, scale=1.0):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # --- Beam elements ---
    for elem in structure.elements:
        if elem in structure.spring_elements:
            continue  # skip springs here, handled separately

        n1 = elem.node1
        n2 = elem.node2

        # Swap Y and Z
        x = [n1.coords[0], n2.coords[0]]
        y = [n1.coords[2], n2.coords[2]]  # original Z
        z = [n1.coords[1], n2.coords[1]]  # original Y

        ax.plot(x, y, z, color='black', linewidth=1)

        if displacements is not None:
            u1 = displacements[n1.dofs]
            u2 = displacements[n2.dofs]

            xd = [n1.coords[0] + scale * u1[0], n2.coords[0] + scale * u2[0]]
            yd = [n1.coords[2] + scale * u1[2], n2.coords[2] + scale * u2[2]]  # original Z
            zd = [n1.coords[1] + scale * u1[1], n2.coords[1] + scale * u2[1]]  # original Y

            ax.plot(xd, yd, zd, color='cyan', linestyle='--')

            if show_internal_forces:
                f_local = elem.compute_internal_forces(displacements, n1.id, n2.id)
                axial_force = f_local[0]
                fx = axial_force * elem.direction_cosines[0]
                fy = axial_force * elem.direction_cosines[2]  # original Z
                fz = axial_force * elem.direction_cosines[1]  # original Y

                midpoint = np.array([
                    (xd[0] + xd[1]) / 2,
                    (yd[0] + yd[1]) / 2,
                    (zd[0] + zd[1]) / 2
                ])

                ax.quiver(midpoint[0], midpoint[1], midpoint[2], fx, fy, fz,
                          color='yellow', length=0.1, normalize=True)

    # --- Spring elements ---
    for spring in structure.spring_elements:
        n1 = spring.node1
        n2 = spring.node2

        x = [n1.coords[0], n2.coords[0]]
        y = [n1.coords[2], n2.coords[2]]  # original Z
        z = [n1.coords[1], n2.coords[1]]  # original Y

        ax.plot(x, y, z, color='magenta', linestyle='--', linewidth=1)

        if displacements is not None:
            u1 = displacements[n1.dofs]
            u2 = displacements[n2.dofs]

            xd = [n1.coords[0] + scale * u1[0], n2.coords[0] + scale * u2[0]]
            yd = [n1.coords[2] + scale * u1[2], n2.coords[2] + scale * u2[2]]  # original Z
            zd = [n1.coords[1] + scale * u1[1], n2.coords[1] + scale * u2[1]]  # original Y

            ax.plot(xd, yd, zd, color='magenta', linestyle=':', linewidth=1)

    # --- Loads ---
    if show_forces:
        for nid, load in structure.loads.items():
            node = structure.nodes[nid]
            fx, fy, fz = load[0:3]

            fy_swapped = fz  # original Z
            fz_swapped = fy  # original Y

            if fx != 0 or fy != 0 or fz != 0:
                ax.quiver(node.coords[0], node.coords[2], node.coords[1],  # coords swapped
                          fx, fy_swapped, fz_swapped,
                          color='blue', length=10, normalize=True)

    # --- Supports ---
    if show_supports:
        for nid, fixed_dofs in structure.supports.items():
            node = structure.nodes[nid]
            ax.scatter(node.coords[0], node.coords[2], node.coords[1],
                       color='red', s=50, marker='s')

    ax.set_xlabel("X")
    ax.set_ylabel("Z")  # original Z is horizontal now
    ax.set_zlabel("Y")  # vertical axis is Y

    ax.set_title("Structure Visualization (Y vertical)")

    ax.view_init(elev=20, azim=135)

    # Equal aspect ratio
    # Get all plotted coordinates
    all_x = [node.coords[0] for node in structure.nodes]
    all_y = [node.coords[2] for node in structure.nodes]  # original Z
    all_z = [node.coords[1] for node in structure.nodes]  # original Y

    x_middle = np.mean([min(all_x), max(all_x)])
    y_middle = np.mean([min(all_y), max(all_y)])
    z_middle = np.mean([min(all_z), max(all_z)])

    x_range = max(all_x) - min(all_x)
    y_range = max(all_y) - min(all_y)
    z_range = max(all_z) - min(all_z)

    plot_radius = 0.5 * max(x_range, y_range, z_range)

    ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
    ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
    ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])

    plt.tight_layout()
