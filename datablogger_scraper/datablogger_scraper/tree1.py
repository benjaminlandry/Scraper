from treelib import Node, Tree
tree = Tree()
parent1 = "Harry"
tree.create_node("Harry", "Harry")  # root node
tree.create_node("Jane", "Jane", parent="Harry")
tree.create_node("Bill", "Bill", parent="Harry")
tree.create_node("Diane", "Diane", parent="Jane")
tree.show()


