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
            print(current_node.data, end=" -> ")
            current_node = current_node.next
        print("None")
# Queue class that inherits from linked list class with enqueue and dequeue methods
class Queue(LinkedList):
    def enqueue(self, new_node):
        
        if self.head == None:
            self.head = new_node
        else:
            current_node = self.head
            while (current_node.next is not None):
                current_node = current_node.next
                
            current_node.next = new_node
        new_node.next = None    
    def dequeue(self):
        if self.head == None:
            print("Queue is empty, please fill the queue first before dequeing.")
            return None
        dequeed_node = self.head
        self.head = self.head.next
        return dequeed_node

def main():
    node1 = Node("1")
    node2 = Node("2")
    node3 = Node("3")
    node4 = Node("4")
    node5 = Node("5")
    node6 = Node("6")
    node7 = Node("7")
    
    queue = Queue(node1)
    queue.enqueue(node2)
    queue.enqueue(node3)
    queue.enqueue(node4)
    queue.enqueue(node5)
    queue.enqueue(node6)
    queue.enqueue(node7)
    queue.print_structure()
    print("Dequeing")
    print(queue.dequeue().data)
    print(queue.dequeue().data)
    print("after dequeing")
    queue.print_structure()
    
if __name__ == "__main__":
   main()
     
        