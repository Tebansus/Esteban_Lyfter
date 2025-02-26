#Temporar person class to test the bus class
class Person:
    pass
# Define the Bus class with the following attributes:
# max_passengers: maximum number of passengers the bus can carry
# current_passengers: current number of passengers on the bus
# Define the following methods for the Bus class:
# add_passenger(self, passenger): adds a passenger to the bus. If the bus is full, print "Cannot add passengers. Bus is full."
# remove_passenger(self): removes a passenger from the bus. If the bus is empty, print "Cannot remove passengers. Bus is empty."
# Note: The add_passenger method should only accept Person objects as passengers. If the passenger is not a Person object, print "Invalid passenger. Please add a Person object."
class Bus:
    def __init__(self, max_passengers):
        self.max_passengers = max_passengers
    
    current_passengers = 0
    def add_passenger(self, passenger):
        if isinstance(passenger, Person):            
            if self.current_passengers >= self.max_passengers:
                print("Cannot add passengers. Bus is full.")
            else:
                self.current_passengers += 1
                print("new passanger has boarded the bus")
        else:
            print("Invalid passenger. Please add a Person object.")
    def remove_passenger(self):
     
        if self.current_passengers == 0:
            print("Cannot remove passengers. Bus is empty.")
        else:
            self.current_passengers -= 1
            print("A Passenger has been removed from the bus.")
# Main function: Create a Bus object and add and remove passengers to test the Bus class.
def main():
    bus_test = Bus(10)
    for i in range(11):
        person = Person()        
        bus_test.add_passenger(person)
    for i in range(11):
        bus_test.remove_passenger()


if __name__ == "__main__":
    main()