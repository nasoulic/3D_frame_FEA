# --------------------------------------------
# RigidElement class
# --------------------------------------------
class RigidElement:
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2

    def __repr__(self):
        return f"<Rigid {self.node1.id} <-> {self.node2.id}>"

    def assemble_constraint_matrix(self):
        """
        Constrains node1 DOFs equal to node2 DOFs.
        """
        return [(self.node1.dofs[i], self.node2.dofs[i]) for i in range(6)]