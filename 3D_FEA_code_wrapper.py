import os
from core.structure import Structure
from core.beamProperties import BeamProperties
from core.visualise_structure import visualize_structure
from core.evaluate_stress import calculate_stress
from core.export_nodal_diaplacements import export_nodal_displacements
from core.visualise_stress import plot_stress_distribution
from core.report_generator import EngineeringReportGenerator

class FEA_wrapper():
    def __init__(self):
        
        self.beamPropertiesList = []
        self.frameStructure = None

    def getBeamPropertyByName(self, name):
        return next((item for item in self.beamPropertiesList if item.name == name))

    def defineBeamProperty(self, E, G, A, Iy, Iz, b = None, h = None, r = None, t = None, name = None):
        
        beamProp = BeamProperties(E, G, A, Iy, Iz, b, h, r, t, name)
        self.beamPropertiesList.append(beamProp)

    def loadFrameNodes(self):

        self.frameStructure = Structure()

        # Add all frame nodes
        self.frameStructure.add_node(0, 0, 0)
        self.frameStructure.add_node(85, 57.36, 0)
        self.frameStructure.add_node(265.25, 179, 0)
        self.frameStructure.add_node(75, 307.39, 0)
        self.frameStructure.add_node(0, 358, 0)
        self.frameStructure.add_node(0, 0, 155)
        self.frameStructure.add_node(85, 57.36, 155)
        self.frameStructure.add_node(265.25, 179, 155)
        self.frameStructure.add_node(75, 307.39, 155)
        self.frameStructure.add_node(0, 358, 77.5)
        self.frameStructure.add_node(0, 358, 155)
        self.frameStructure.add_node(0, 658, 77.5)
        self.frameStructure.add_node(-250, 658, 77.5)
        self.frameStructure.add_node(-585, 658, 77.5)
        self.frameStructure.add_node(-920, 658, 77.5)
        self.frameStructure.add_node(-1170, 658, 77.5)
        self.frameStructure.add_node(-1170, 358, 77.5)
        self.frameStructure.add_node(-1170, 358, 0)
        self.frameStructure.add_node(-1170, 358, 155)
        self.frameStructure.add_node(-1245, 307.39, 0)
        self.frameStructure.add_node(-1435.25, 179, 0)
        self.frameStructure.add_node(-1255, 57.36, 0)
        self.frameStructure.add_node(-1170, 0, 0)
        self.frameStructure.add_node(-1245, 307.39, 155)
        self.frameStructure.add_node(-1435.25, 179, 155)
        self.frameStructure.add_node(-1255, 57.36, 155)
        self.frameStructure.add_node(-1170, 0, 155)
        self.frameStructure.add_node(0, 658, 1087)
        self.frameStructure.add_node(-250, 658, 1087)
        self.frameStructure.add_node(-585, 658, 1087)
        self.frameStructure.add_node(-920, 658, 1087)
        self.frameStructure.add_node(-1170, 658, 1087)
        self.frameStructure.add_node(0, 358, 1087)
        self.frameStructure.add_node(-1170, 358, 1087)
        self.frameStructure.add_node(-1170, 358, 1009.5)
        self.frameStructure.add_node(0, 358, 1164.5)
        self.frameStructure.add_node(0, 358, 1009.5)
        self.frameStructure.add_node(-1170, 358, 1164.5)
        self.frameStructure.add_node(0, 0, 1009.5)
        self.frameStructure.add_node(85, 57.36, 1009.5)
        self.frameStructure.add_node(265.25, 179, 1009.5)
        self.frameStructure.add_node(75, 307.39, 1009.5)
        self.frameStructure.add_node(0, 0, 1164.5)
        self.frameStructure.add_node(85, 57.36, 1164.5)
        self.frameStructure.add_node(265.25, 179, 1164.5)
        self.frameStructure.add_node(75, 307.39, 1164.5)
        self.frameStructure.add_node(-1245, 307.39, 1009.5)
        self.frameStructure.add_node(-1435.25, 179, 1009.5)
        self.frameStructure.add_node(-1255, 57.36, 1009.5)
        self.frameStructure.add_node(-1170, 0, 1009.5)
        self.frameStructure.add_node(-1245, 307.39, 1164.5)
        self.frameStructure.add_node(-1435.25, 179, 1164.5)
        self.frameStructure.add_node(-1255, 57.36, 1164.5)
        self.frameStructure.add_node(-1170, 0, 1164.5)

    def loadFrameBeams(self):

        fork_beams = self.getBeamPropertyByName("fork")
        fork_pivot = self.getBeamPropertyByName("fork_pivot")
        frame_traverse_beam = self.getBeamPropertyByName("frame_traverse")
        fork_to_frame = self.getBeamPropertyByName("fork_to_frame")
        frame_beam = self.getBeamPropertyByName("frame")

        # Define structural memebers
        self.frameStructure.add_beam(self.frameStructure.getNodeById(0),
                                     self.frameStructure.getNodeById(1), fork_beams)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(1), 
                                     self.frameStructure.getNodeById(2), fork_beams)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(2), 
                                     self.frameStructure.getNodeById(3), fork_beams)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(3), 
                                     self.frameStructure.getNodeById(4), fork_beams)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(5), 
                                     self.frameStructure.getNodeById(6), fork_beams)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(6), 
                                     self.frameStructure.getNodeById(7), fork_beams)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(7), 
                                     self.frameStructure.getNodeById(8), fork_beams)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(8), 
                                     self.frameStructure.getNodeById(10), fork_beams)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(2), 
                                     self.frameStructure.getNodeById(7), fork_pivot)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(4), 
                                     self.frameStructure.getNodeById(9), fork_to_frame)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(9), 
                                     self.frameStructure.getNodeById(10), fork_to_frame)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(9), 
                                     self.frameStructure.getNodeById(11), fork_to_frame)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(11), 
                                     self.frameStructure.getNodeById(12), frame_beam)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(12), 
                                     self.frameStructure.getNodeById(13), frame_beam)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(13), 
                                     self.frameStructure.getNodeById(14), frame_beam)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(14), 
                                     self.frameStructure.getNodeById(15), frame_beam)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(15), 
                                     self.frameStructure.getNodeById(16), fork_to_frame)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(16), 
                                     self.frameStructure.getNodeById(17), fork_to_frame)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(16), 
                                     self.frameStructure.getNodeById(18), fork_to_frame)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(17), 
                                     self.frameStructure.getNodeById(19), fork_beams)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(18), 
                                     self.frameStructure.getNodeById(23), fork_beams)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(19), 
                                     self.frameStructure.getNodeById(20), fork_beams)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(20), 
                                     self.frameStructure.getNodeById(21), fork_beams)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(21), 
                                     self.frameStructure.getNodeById(22), fork_beams)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(23), 
                                     self.frameStructure.getNodeById(24), fork_beams)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(24), 
                                     self.frameStructure.getNodeById(25), fork_beams)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(25), 
                                     self.frameStructure.getNodeById(26), fork_beams)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(20), 
                                     self.frameStructure.getNodeById(24), fork_beams)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(11), 
                                     self.frameStructure.getNodeById(27), frame_traverse_beam)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(12), 
                                     self.frameStructure.getNodeById(28), frame_traverse_beam)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(13), 
                                     self.frameStructure.getNodeById(29), frame_traverse_beam)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(14), 
                                     self.frameStructure.getNodeById(30), frame_traverse_beam)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(15), 
                                     self.frameStructure.getNodeById(31), frame_traverse_beam)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(27), 
                                     self.frameStructure.getNodeById(28), frame_beam)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(28), 
                                     self.frameStructure.getNodeById(29), frame_beam)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(29), 
                                     self.frameStructure.getNodeById(30), frame_beam)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(30), 
                                     self.frameStructure.getNodeById(31), frame_beam)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(27), 
                                     self.frameStructure.getNodeById(32), fork_to_frame)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(31), 
                                     self.frameStructure.getNodeById(33), fork_to_frame)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(32), 
                                     self.frameStructure.getNodeById(35), fork_to_frame)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(32), 
                                     self.frameStructure.getNodeById(36), fork_to_frame)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(33), 
                                     self.frameStructure.getNodeById(34), fork_to_frame)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(33), 
                                     self.frameStructure.getNodeById(37), fork_to_frame)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(36), 
                                     self.frameStructure.getNodeById(41), fork_beams)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(41), 
                                     self.frameStructure.getNodeById(40), fork_beams)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(40), 
                                     self.frameStructure.getNodeById(39), fork_beams)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(39), 
                                     self.frameStructure.getNodeById(38), fork_beams)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(35), 
                                     self.frameStructure.getNodeById(45), fork_beams)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(45), 
                                     self.frameStructure.getNodeById(44), fork_beams)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(44), 
                                     self.frameStructure.getNodeById(43), fork_beams)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(43), 
                                     self.frameStructure.getNodeById(42), fork_beams)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(40), 
                                     self.frameStructure.getNodeById(44), fork_pivot)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(34), 
                                     self.frameStructure.getNodeById(46), fork_beams)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(46), 
                                     self.frameStructure.getNodeById(47), fork_beams)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(47), 
                                     self.frameStructure.getNodeById(48), fork_beams)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(48), 
                                     self.frameStructure.getNodeById(49), fork_beams)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(37), 
                                     self.frameStructure.getNodeById(50), fork_beams)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(50), 
                                     self.frameStructure.getNodeById(51), fork_beams)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(51), 
                                     self.frameStructure.getNodeById(52), fork_beams)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(52), 
                                     self.frameStructure.getNodeById(53), fork_beams)
        self.frameStructure.add_beam(self.frameStructure.getNodeById(47), 
                                     self.frameStructure.getNodeById(51), fork_pivot)

    def addSpringElements(self, spring_vector = [0, 0, 0, 0, 0, 0]):
        """
        spring_vector = [0, 0, 0, 0, 0, 0]  : Spring constant on each DOF (N/mm)
        """

        self.frameStructure.add_spring(self.frameStructure.getNodeById(1), 
                                       self.frameStructure.getNodeById(3), spring_vector)
        self.frameStructure.add_spring(self.frameStructure.getNodeById(6), 
                                       self.frameStructure.getNodeById(8), spring_vector)
        self.frameStructure.add_spring(self.frameStructure.getNodeById(19), 
                                       self.frameStructure.getNodeById(21), spring_vector)
        self.frameStructure.add_spring(self.frameStructure.getNodeById(23), 
                                       self.frameStructure.getNodeById(25), spring_vector)
        self.frameStructure.add_spring(self.frameStructure.getNodeById(39), 
                                       self.frameStructure.getNodeById(41), spring_vector)
        self.frameStructure.add_spring(self.frameStructure.getNodeById(43), 
                                       self.frameStructure.getNodeById(45), spring_vector)
        self.frameStructure.add_spring(self.frameStructure.getNodeById(46), 
                                       self.frameStructure.getNodeById(48), spring_vector)
        self.frameStructure.add_spring(self.frameStructure.getNodeById(50), 
                                       self.frameStructure.getNodeById(52), spring_vector)

    def addConstraints(self, nodes, spcs):
        for node, spc in zip(nodes, spcs):
            self.frameStructure.add_support(node.id, spc)

    def addLoads(self, nodes, loads):
        for node, load in zip(nodes, loads):
            self.frameStructure.add_load(node.id, load)

    def solve(self):
        self.U = self.frameStructure.solve()

    def exportResults(self, name, scale = 2):
        export_nodal_displacements(self.frameStructure, self.U, "nodal_displacement_{0}.dat".format(name))
        calculate_stress(self.frameStructure, self.U, "stresses_output_{0}.dat".format(name))
        visualize_structure(self.frameStructure, self.U, scale = scale, name = name)
        plot_stress_distribution(self.frameStructure, self.U, stress_component = "sigma_axial", filename = "stress_{0}.png".format(name))
        plot_stress_distribution(self.frameStructure, self.U, stress_component = "sigma_bending_y", filename = "stress_{0}.png".format(name))
        plot_stress_distribution(self.frameStructure, self.U, stress_component = "sigma_bending_z", filename = "stress_{0}.png".format(name))
        plot_stress_distribution(self.frameStructure, self.U, stress_component = "tau_torsion", filename = "stress_{0}.png".format(name))
        plot_stress_distribution(self.frameStructure, self.U, stress_component = "sigma_total", filename = "stress_{0}.png".format(name))

    def createReport(self):
        gen = EngineeringReportGenerator(os.getcwd())
        gen.generate()


if __name__ == "__main__":

    agv = FEA_wrapper()

    # Fork Cross-Section
    E = 210e3  # MPa (Young's modulus)
    G = 81.2e3  # MPa (Shear modulus)
    b = 40 # mm
    h = 40 # mm
    t = 3 # mm
    A = b*h - (h-2*t)*(b-2*t) # m2
    Iy = b*h**3/12 # m4
    Iz = b**3*h/12 # m4

    agv.defineBeamProperty(E, G, A, Iy, Iz, b, h, t = t, name = "fork")

    # Fork Pivot Cross-Section
    E = 210e3  # MPa (Young's modulus)
    G = 81.2e3  # MPa (Shear modulus)
    b = 35 # mm
    h = 35 # mm
    t = 2.5 # mm
    A = b*h - (h-2*t)*(b-2*t) # m2
    Iy = b*h**3/12 # m4
    Iz = b**3*h/12 # m4

    agv.defineBeamProperty(E, G, A, Iy, Iz, b, h, t = t, name = "fork_pivot")

    # Fork 2 Frame Cross-Section
    E = 210e3  # MPa (Young's modulus)
    G = 81.2e3  # MPa (Shear modulus)
    b = 50 # mm
    h = 50 # mm
    t = 2.5 # mm
    A = b*h - (h-2*t)*(b-2*t) # m2
    Iy = b*h**3/12 # m4
    Iz = b**3*h/12 # m4

    agv.defineBeamProperty(E, G, A, Iy, Iz, b, h, t = t, name = "fork_to_frame")

    # Frame Beam Cross-Section
    E = 210e3  # MPa (Young's modulus)
    G = 81.2e3  # MPa (Shear modulus)
    b = 50 # mm
    h = 50 # mm
    t = 2.5 # mm
    A = b*h - (h-2*t)*(b-2*t) # m2
    Iy = b*h**3/12 # m4
    Iz = b**3*h/12 # m4

    agv.defineBeamProperty(E, G, A, Iy, Iz, b, h, t = t, name = "frame")

    # Frame Traverse Beam Cross-Section
    E = 210e3  # MPa (Young's modulus)
    G = 81.2e3  # MPa (Shear modulus)
    b = 50 # mm
    h = 50 # mm
    t = 3 # mm
    A = b*h - (h-2*t)*(b-2*t) # m2
    Iy = b*h**3/12 # m4
    Iz = b**3*h/12 # m4

    agv.defineBeamProperty(E, G, A, Iy, Iz, b, h, t = t, name = "frame_traverse")

    agv.loadFrameNodes()
    agv.loadFrameBeams()
    agv.addSpringElements([0, 6, 0, 0, 0, 0])

    spc_nodes = [agv.frameStructure.getNodeById(22), agv.frameStructure.getNodeById(26), 
                 agv.frameStructure.getNodeById(49), agv.frameStructure.getNodeById(53)]
    
    constrained_dofs = [[1, 3, 4, 5], [1, 3, 4, 5],
                        [0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5]]

    lc_nodes = [agv.frameStructure.getNodeById(0), agv.frameStructure.getNodeById(5), 
                 agv.frameStructure.getNodeById(38), agv.frameStructure.getNodeById(42)]
    
    lcs = [[0, 1000, 0, 0, 0, 0], [0, 1000, 0, 0, 0, 0],
           [0, 1000, 0, 0, 0, 0], [0, 1000, 0, 0, 0, 0]]
    
    agv.addConstraints(spc_nodes, constrained_dofs)
    agv.addLoads(lc_nodes, lcs)

    agv.solve()
    agv.exportResults("flexuralTest")
    agv.createReport()