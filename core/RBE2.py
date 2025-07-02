# --------------------------------------------
# RBE2Element class
# --------------------------------------------
class RBE2Element:
    def __init__(self, master_node, slave_nodes):
        self.master_node = master_node
        self.slave_nodes = slave_nodes

    def __repr__(self):
        slaves = ", ".join(str(node.id) for node in self.slave_nodes)
        return f"<RBE2 master={self.master_node.id} slaves=[{slaves}]>"

    def assemble_constraint_matrix(self):
        """
        Example: Returns list of tuples for enforcing same DOFs.
        [(master_dof, slave_dof), ...]
        """
        constraints = []
        for slave in self.slave_nodes:
            for i in range(6):  # assuming 6 DOFs
                constraints.append((self.master_node.dofs[i], slave.dofs[i]))
        return constraints