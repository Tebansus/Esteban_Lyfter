#Node class for binary tree implementation, with left and right child nodes
class Node:
    data: str

    def __init__(self, data, left=None, right =None):
        self.data = data
        self.left = left
        self.right = right
# Binary tree class with root node that traverses the tree in left hand side, root and right hand side order for the main tree and sub trees, using recursion.
# Used this implementation as reference: https://www.geeksforgeeks.org/print-binary-tree-2-dimensions/
class BinaryTree:
    def __init__(self, root):
        self.root = root
# Class get height method that gets the height of the tree by traversing the tree in level order and incrementing the height for each level.
    def get_height(self):
        if self.root is None:
            return 0
        height = 0
        queue = [self.root]
        #uses a queue to traverse the tree in level order, but not for the tree structure itself.
        while queue:
            height += 1
            
            level_size = len(queue)
            for _ in range(level_size):
                node = queue.pop(0)
                if node.left:
                    
                    queue.append(node.left)                    
                if node.right:
                    queue.append(node.right)
                    
        return height

    def print_structure(self):
        if self.root is None:
            print("Tree is empty. Please add nodes to the tree before printing.")
            return
        # Use the height of the tree to calculate the maximum width of the tree and the current level of the tree.
        height = self.get_height()
        max_width = 2 ** height - 1
        
        current_level = [(self.root, (max_width - 1) // 2)]
        
        for level in range(height):
            next_level = []
            current_line = [' '] * max_width
            branch_line = [' '] * max_width
            
            for node, pos in current_level:
                if node is not None:
                    current_line[pos] = node.data
                    
                    offset = 2 ** (height - level - 2)
                    
                    # Calculate branch positions based on parent-child midpoint for spacing and alignment.
                    if node.left:
                        left_pos = pos - offset
                        next_level.append((node.left, left_pos))
                        branch_line[(pos + left_pos) // 2] = '/'
                        
                    if node.right:
                        right_pos = pos + offset
                        next_level.append((node.right, right_pos))
                        branch_line[(pos + right_pos) // 2] = '\\'
            
            print(''.join(current_line).rstrip())
            if level < height - 1:
                print(''.join(branch_line).rstrip())
            
            current_level = next_level

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