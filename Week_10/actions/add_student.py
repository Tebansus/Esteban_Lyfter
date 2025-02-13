def add_student_func():
    # Ask the user for the number of students to add and define an empty dictionary to store the students
    while True:
        try:
            n = int(input("Enter the number of students: "))
            break
        except ValueError:
            print("Invalid input. Please enter an integer value.")
    students_dict = {}
    
    for i in range(n):
        # Define the student's name, section, grades and subjects
        full_name = input("\nEnter student's name: ").strip()
        section = input("Enter section (for example, 11B): ").strip()
        # Define the dictionary to sore the student's grades
        grades = {}
        subjects = ['Spanish', 'English', 'Social Studies', 'Science']
        # Loop through the subjects and ask for the student's grade
        for subject in subjects:
            while True:
                # Ask for the student's grade and validate it with a try-except block to make sure it's a number.
                grade_input = input(f"Enter {subject} grade (0-100): ")
                try:
                    grade = float(grade_input)
                    if 0 <= grade <= 100:
                        # Streamline the key by removing spaces and converting to lowercase, and add the grade title.
                        key = f"{subject.lower().replace(' ', '_')}_grade"
                        grades[key] = grade
                        break
                    else:
                        print("Grade must be between 0 and 100. Please keep trying until it's a valid number.")
                except ValueError:
                    print("Invalid input. Please enter a numeric value.")
        
        average = sum(grades.values()) / 4
        # Use the unpacking operator ** to merge the student's name with the grades and average
        student_entry = {'section': section, **grades,'average': average}
        # Add the student's entry to the dictionary
        students_dict[full_name] = student_entry
    # Return the merged dictionary
    return students_dict