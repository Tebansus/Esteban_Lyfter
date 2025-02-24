# This program calculates the area of a circle with radius 3
# using a class and method
class Circle:
    radius = 0
    def get_area(self):
        return 3.14 * self.radius * self.radius
# Main function
def main():
    circle_for_area = Circle()
    circle_for_area.radius = 3
    print("Area of circle with radius 3 is", circle_for_area.get_area())

if __name__ == "__main__":
    main()