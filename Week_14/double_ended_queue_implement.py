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
        current_node = self.head
        while current_node is not None:
            print(current_node.data, end=" <-> ")
            current_node = current_node.next
        print("None")
# Double ended queue class that inherits from linked list class with push and pop methods for both left and right, uses super to call the parent class constructor and get_tail method to get the tail of the queue.
class double_ended_queue(LinkedList):
    tail: Node
    def __init__(self, head):
        super().__init__(head)
        self.tail = self.get_tail()
    # Get tail method that traverses the queue to get the tail node.
    def get_tail(self):
        current_node = self.head
        while current_node and current_node.next:
            current_node = current_node.next
        return current_node
    # Push right method that pushes the right most node to the queue, by setting the new node as the head, pointing to the old head.
    def push_right(self, new_node):
        if self.head == None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node
    # Push left method that pushes the left most node to the queue, by setting the tail node to the new node and setting the next node as the new tail.
    def push_left(self, new_node):
        if self.tail == None:
            self.tail = new_node
            self.head = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
    # Pop left method that pops the left most node from the queue, by removing the head node and setting the next node as the new head.
    def pop_left(self):
        if self.head == None:
            print("Queue is empty, please add nodes to the queue before popping.")
            return None
        popped_node = self.head
        if self.head.next == None:
            self.tail = None
        self.head = self.head.next
        return popped_node
    # Pop right method that pops the right most node from the queue, by traversing the queue from the head to the tail and removing the tail node.
    def pop_right(self):
        if self.tail == None:
            print("Queue is empty, please add nodes to the queue before popping.")
            return None
        if self.tail == self.head:
            popped_node = self.head
            self.tail = None
            self.head = None
            return popped_node
        current_node = self.head
        while current_node.next != self.tail:
            current_node = current_node.next
        
        popped_node = self.tail
        current_node.next = None
        self.tail = current_node
        return popped_node
# Main function for testing the linked, double ended list with 7 nodes.  
def main():
    # Initiate the test nodes
    node1 = Node("1")
    node2 = Node("2")
    node3 = Node("3")
    node4 = Node("4")
    node5 = Node("5")
    node6 = Node("6")
    node7 = Node("7")
    # Initiate the double ended queue with the first node
    queue = double_ended_queue(node1)
    # Push the nodes to the left and right of the queue
    queue.push_right(node2)
    queue.push_right(node3)
    queue.push_right(node4)
    queue.push_left(node5)
    queue.push_left(node6)
    queue.push_left(node7)
    # See final queue structure
    queue.print_structure()
    # Check to see if tail initialization works    
    print("Print_Tail")
    tail = queue.get_tail()
    print(tail.data)
    # Remove the 4 and the 7 nodes by popping them from the queue, both left and right
    queue.pop_left()
    queue.pop_right()
    print("After popping")
    queue.print_structure()


if __name__ == "__main__":
    main()