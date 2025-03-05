from abc import ABC, abstractmethod
import math
# Create an abstract class Shape with abstract methods calculate_area and calculate_perimeter.
class Shape(ABC):
    @abstractmethod
    def calculate_area(self):
        pass
    @abstractmethod
    def calculate_perimeter(self):
        pass
# Create classes Circle, Rectangle, and Square that extend the Shape class and add their own perimeter and area calculation methods.
class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    def calculate_area(self):
        return math.pi * self.radius * self.radius
    def calculate_perimeter(self):
        return 2 * math.pi * self.radius 
class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    def calculate_area(self):
        return self.width * self.height
    def calculate_perimeter(self):
        return 2 * (self.width + self.height)
class Square(Shape):
    def __init__(self, side):
        self.side = side
    def calculate_area(self):
        return self.side * self.side
    def calculate_perimeter(self):
        return 4 * self.side
# Test the classes by creating instances of Circle, Rectangle, and Square and calling the methods on them.
def main():
    circle = Circle(5)
    print(circle.calculate_area())
    print(circle.calculate_perimeter())
    rectangle = Rectangle(4, 5)
    print(rectangle.calculate_area())
    print(rectangle.calculate_perimeter())
    square = Square(5)
    print(square.calculate_area())
    print(square.calculate_perimeter())

if __name__ == "__main__":
    main()