from actions.add_student import add_student_func
from data import load_data_registry
from actions.student_viewer import display_students
from actions.averge_calculators import top3_average
from actions.averge_calculators import average_the_averages
from data import save_student_registry
# Function to display the menu options
def display_menu():
        
        print("welcome to the student DB. Choose an operation:")
        print("1. Add N students")
        print("2. See all students")
        print("3. See top 3 students")
        print("4. See average for all students")
        print("5. Export current student registry as CSV.")
        print("6. Import existing Student Data")
        print("7. Exit")
# Function to handle the menu functionality       
def menu_functionality(choice, dict_to):
        # If the user chooses 1, call the add_student_func function and update the dictionary
        if choice == 1:
                students_to_add = add_student_func()
                dict_to.update(students_to_add)
                return dict_to
        # If the user chooses 2, call the display_students function
        elif choice == 2:
                if not dict_to:
                        print("No students to display, please enter students first.")
                else:
                        display_students(dict_to)
                        return dict_to
        # If the user chooses 3, call the top3_average function
        elif choice == 3:
                if not dict_to:
                        print("No students to display, please enter students first.")                        
                else:
                        top3_average(dict_to)
                        return dict_to
        # If the user chooses 4, call the average_the_averages function
        elif choice == 4:
                if not dict_to:
                        print("No students to display, please enter students first.")
                else:
                        average_the_averages(dict_to)
                        return dict_to
        # If the user chooses 5, call the save_student_registry function      
        elif choice == 5:
                location_to_save = input("Please enter the path to save the file: ")
                saved_status = save_student_registry(dict_to, location_to_save)
                if saved_status:
                        print("File saved successfully.")
                        return dict_to
                else:
                        print("File couldn't be saved, empty dict.")
                        return dict_to
        # If the user chooses 6, call the load_data_registry function and update the dictionary
        elif choice == 6:
                location_to_load = input("Please enter the path to load the file: ")
                dict_loaded = load_data_registry(location_to_load)
                if dict_loaded:
                        print("File loaded successfully.")
                        dict_to.update(dict_loaded)
                        return dict_to
                else:                        
                        return dict_to
        # If the user chooses 7, return "Ending" to break the loop in main.py
        elif choice == 7:
                return "Ending"
        
                       
        