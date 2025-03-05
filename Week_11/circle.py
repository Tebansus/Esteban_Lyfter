# This program calculates the area of a circle with radius 3
# using a class and method
import math
class Circle:
    def __init__(self, radius):
        self.radius = radius
    def get_area(self):
        return math.pi * self.radius * self.radius
# Main function
def main():
    circle_for_area = Circle(3)    
    print("Area of circle with radius 3 is", circle_for_area.get_area())

if __name__ == "__main__":
    main()