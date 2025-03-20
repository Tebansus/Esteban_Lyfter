#Node class for binary tree implementation, with left and right child nodes
class Node:
    data: str

    def __init__(self, data, left=None, right =None):
        self.data = data
        self.left = left
        self.right = right
# Binary tree class with root node that traverses the tree in left hand side, root and right hand side order for the main tree and sub trees, using recursion.
class BinaryTree:
    # Root node of the binary tree
    root: Node
    def __init__(self, root):
        self.root = root
    def print_structure(self):
        def in_order_traversal(node):
            if node:                
                in_order_traversal(node.left)
                print(node.data)                
                in_order_traversal(node.right)
        
        in_order_traversal(self.root)

# Main fuction for testing the binary tree with 7 nodes.
def main():
    node1 = Node("1")
    node2 = Node("2")
    node3 = Node("3")
    node4 = Node("4")
    node5 = Node("5")
    node6 = Node("6")
    node7 = Node("7")
    
    node1.left = node2
    node1.right = node3
    node2.left = node4
    node2.right = node5
    node3.left = node6
    node3.right = node7
    
    binary_tree = BinaryTree(node1)
    binary_tree.print_structure()
    
if __name__ == "__main__":
   main()