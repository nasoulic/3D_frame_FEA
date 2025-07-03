# --------------------------------------------
# RBE3Element class
# --------------------------------------------
class RBE3Element:
    def __init__(self, master_node, slave_nodes, weights=None):
        self.master_node = master_node
        self.slave_nodes = slave_nodes
        if weights is None:
            self.weights = [1.0 / len(slave_nodes)] * len(slave_nodes)
        else:
            self.weights = weights

    def __repr__(self):
        slaves = ", ".join(str(node.id) for node in self.slave_nodes)
        return f"<RBE3 master={self.master_node.id} slaves=[{slaves}]>"

    def assemble_constraint_matrix(self):
        """
        Example: Returns list of tuples with weight
        [(master_dof, [(slave_dof, weight), ...]), ...]
        """
        constraints = []
        for i in range(6):  # 6 DOFs
            slave_info = [(slave.dofs[i], w) for slave, w in zip(self.slave_nodes, self.weights)]
            constraints.append((self.master_node.dofs[i], slave_info))
        return constraints