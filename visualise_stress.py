import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Line3DCollection
import matplotlib.cm as cm
import matplotlib.colors as colors

def plot_stress_distribution(structure, U, stress_component='axial', scale=1.0):
    """
    Visualizes stress distribution on the structure elements using color mapping.

    Parameters:
    - structure: structure object with nodes and elements
    - U: global displacement vector
    - h, b: cross-section dimensions
    - stress_component: which stress to visualize, e.g. 'axial', 'bending_y', 'bending_z', 'torsion'
    - scale: scale factor for deformation visualization (optional)
    """

    # Collect lines and stress magnitudes for coloring
    lines = []
    stress_vals = []

    # For each element, compute stresses and create line segments for plotting
    for element in structure.elements:
        i, j = element.node1.id, element.node2.id

        # Get element nodal displacements (only translations here for deformation)
        u_i = U[6*i:6*i+3]
        u_j = U[6*j:6*j+3]

        # Coordinates deformed by scale factor
        p1 = structure.nodes[i].coords + scale * u_i
        p2 = structure.nodes[j].coords + scale * u_j
        lines.append([p1, p2])

        # Compute internal forces in local coordinates
        f_local = element.compute_internal_forces(U, i, j)

        # Cross-section params
        c_y = element.h / 2
        c_z = element.b / 2
        c_t = c_y

        stresses = element.compute_stresses(f_local, c_y, c_z, c_t)

        # Extract the stress component for colormapping
        if stress_component in stresses:
            stress_vals.append(abs(stresses[stress_component]))
        else:
            # If requested stress_component not found, fallback to axial
            stress_vals.append(abs(stresses.get('axial', 0)))

    # Normalize stresses for colormap
    stress_vals = np.array(stress_vals)
    norm = colors.Normalize(vmin=stress_vals.min(), vmax=stress_vals.max())

    # Choose colormap
    cmap = cm.get_cmap('jet')

    # Map normalized stress to colors
    colors_mapped = cmap(norm(stress_vals))

    # Plotting
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Create a Line3DCollection with colors according to stress
    lc = Line3DCollection(lines, colors=colors_mapped, linewidths=4)
    ax.add_collection3d(lc)

    # Plot undeformed nodes for reference
    node_coords = np.array([node.coords for node in structure.nodes])
    ax.scatter(node_coords[:,0], node_coords[:,1], node_coords[:,2], color='k', s=10)

    # Set axis limits with some margin
    margin = 0.1 * np.ptp(node_coords, axis=0)
    ax.set_xlim([node_coords[:,0].min()-margin[0], node_coords[:,0].max()+margin[0]])
    ax.set_ylim([node_coords[:,1].min()-margin[1], node_coords[:,1].max()+margin[1]])
    ax.set_zlim([node_coords[:,2].min()-margin[2], node_coords[:,2].max()+margin[2]])

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f'Stress distribution ({stress_component})')

    # Add colorbar
    mappable = cm.ScalarMappable(norm=norm, cmap=cmap)
    mappable.set_array(stress_vals)
    cbar = plt.colorbar(mappable, ax=ax, shrink=0.6, pad=0.1)
    cbar.set_label('Stress (MPa)')

    plt.tight_layout()
    plt.show()
