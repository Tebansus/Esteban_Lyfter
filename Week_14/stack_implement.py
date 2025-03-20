# Node class for linked list implementation, with next node
class Node:
    data: str

    def __init__(self, data, next=None):
        self.data = data
        self.next = next
# Linked list class with head node that traverses the list in order
class LinkedList:
    head: Node

    def __init__(self, head):
        self.head = head
    def print_structure(self):
        curent_node = self.head
        while (curent_node is not None):
            print(curent_node.data)
            curent_node = curent_node.next
# Queue class that inherits from linked list class with enqueue and dequeue methods
class Stack(LinkedList):
    def pop(self):
        if self.head == None:
            return None
        popped_node = self.head
        self.head = self.head.next
        return popped_node
    def push(self,new_node):
        if self.head == None:
            self.head = new_node
        else:
            new_node.next = self.head
            self.head = new_node
# Main fuction for testing the linked list with 7 nodes.
def main():
    node1 = Node("1")
    node2 = Node("2")
    node3 = Node("3")
    node4 = Node("4")
    node5 = Node("5")
    node6 = Node("6")
    node7 = Node("7")
    
    stack = Stack(node1)
    stack.push(node2)
    stack.push(node3)
    stack.push(node4)
    stack.push(node5)
    stack.push(node6)
    stack.push(node7)
    
    stack.print_structure()
    
    stack.pop()
    stack.pop()
    print("After popping")
    stack.print_structure()   
if __name__ == "__main__":
    main()