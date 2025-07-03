import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from matplotlib.animation import FFMpegWriter
import os

def animate_deformation(structure, U, scale=1.0, save_path="deformation_animation.mp4"):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Compute undeformed geometry
    original_lines = []
    for elem in structure.elements:
        i, j = elem.node1.id, elem.node2.id
        p1 = structure.nodes[i].coords
        p2 = structure.nodes[j].coords
        original_lines.append([p1, p2])

    original_lc = Line3DCollection(original_lines, colors='gray', linewidths=1.5, linestyles='dashed')

    # Determine auto-scaling limits
    all_coords = np.array([node.coords for node in structure.nodes])
    x_min, y_min, z_min = all_coords.min(axis=0) - 1
    x_max, y_max, z_max = all_coords.max(axis=0) + 1

    def get_lines(u_factor):
        lines = []
        for elem in structure.elements:
            i, j = elem.node1.id, elem.node2.id
            u_i = U[6*i:6*i+3] * u_factor
            u_j = U[6*j:6*j+3] * u_factor

            p1 = structure.nodes[i].coords + u_i
            p2 = structure.nodes[j].coords + u_j
            lines.append([p1, p2])
        return lines

    def update(frame):
        ax.cla()
        ax.set_xlim([x_min, x_max])
        ax.set_ylim([y_min, y_max])
        ax.set_zlim([z_min, z_max])
        ax.set_title("Animated Deformation")
        ax.set_box_aspect([x_max - x_min, y_max - y_min, z_max - z_min])

        # Set fixed isometric view (elevation and azimuth)
        ax.view_init(elev=30, azim=45)

        # Undeformed structure
        ax.add_collection3d(original_lc)

        # Deformed structure
        lines = get_lines(frame)
        lc = Line3DCollection(lines, colors='blue', linewidths=2)
        ax.add_collection3d(lc)


    ani = animation.FuncAnimation(
        fig, update, frames=np.linspace(0, scale, 30), interval=100
    )

    writer = FFMpegWriter(fps=15, bitrate=1800)
    ani.save(save_path, writer=writer)
    plt.close()
    return os.path.abspath(save_path)
