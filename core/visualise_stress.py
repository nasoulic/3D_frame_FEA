import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Line3DCollection
import matplotlib.cm as cm
import matplotlib.colors as colors

def plot_stress_distribution(structure, U, stress_component='axial', scale=1.0, filename="stress.png"):
    """
    Visualizes stress distribution on the structure elements using color mapping,
    with Y as the vertical axis instead of Z.
    """

    # Collect lines and stress magnitudes for coloring
    lines = []
    stress_vals = []

    for element in structure.elements:
        i, j = element.node1.id, element.node2.id

        u_i = U[6*i:6*i+3]
        u_j = U[6*j:6*j+3]

        p1 = structure.nodes[i].coords + scale * u_i
        p2 = structure.nodes[j].coords + scale * u_j

        # Swap Y and Z: [X, Z, Y]
        p1_swapped = np.array([p1[0], p1[2], p1[1]])
        p2_swapped = np.array([p2[0], p2[2], p2[1]])

        lines.append([p1_swapped, p2_swapped])

        f_local = element.compute_internal_forces(U, i, j)

        c_y = element.h / 2
        c_z = element.b / 2
        c_t = c_y

        stresses = element.compute_stresses(f_local, c_y, c_z, c_t)

        if stress_component in stresses:
            stress_vals.append(abs(stresses[stress_component]))
        else:
            stress_vals.append(abs(stresses.get('axial', 0)))

    stress_vals = np.array(stress_vals)
    norm = colors.Normalize(vmin=stress_vals.min(), vmax=stress_vals.max())
    cmap = cm.get_cmap('jet')
    colors_mapped = cmap(norm(stress_vals))

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    lc = Line3DCollection(lines, colors=colors_mapped, linewidths=4)
    ax.add_collection3d(lc)

    # Plot undeformed nodes (swapped Y/Z)
    node_coords = np.array([node.coords for node in structure.nodes])
    node_coords_swapped = node_coords[:, [0, 2, 1]]
    ax.scatter(node_coords_swapped[:, 0], node_coords_swapped[:, 1], node_coords_swapped[:, 2],
               color='k', s=10)

    margin = 0.1 * np.ptp(node_coords, axis=0)
    ax.set_xlim([node_coords[:, 0].min()-margin[0], node_coords[:, 0].max()+margin[0]])
    ax.set_ylim([node_coords[:, 2].min()-margin[2], node_coords[:, 2].max()+margin[2]])  # Z slot
    ax.set_zlim([node_coords[:, 1].min()-margin[1], node_coords[:, 1].max()+margin[1]])  # Y slot

    ax.set_xlabel('X')
    ax.set_ylabel('Z')  # Actually the original Z
    ax.set_zlabel('Y')  # Now vertical

    ax.set_title(f'Stress distribution ({stress_component})')
    ax.view_init(elev=40, azim=130)

    mappable = cm.ScalarMappable(norm=norm, cmap=cmap)
    mappable.set_array(stress_vals)
    cbar = plt.colorbar(mappable, ax=ax, shrink=0.6, pad=0.1)
    cbar.set_label('Stress (MPa)')

    plt.tight_layout()
    plt.savefig(f"{stress_component}_{filename}")
