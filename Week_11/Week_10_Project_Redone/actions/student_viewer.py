def display_students(students_dict):
    # Loop through the dictionary and print the student's information
    for name, student in students_dict.items(): 
        # Access the student's attributes with dot notation instead of dictionary keys
        print(f"\nStudent: {name}")
        print(f"Section: {student.section}")  
        print("Grades: ")       
        print(f"    Spanish: {student.spanish_grade}")
        print(f"    English: {student.english_grade}")        
        print(f"    Social Studies: {student.social_studies_grade}")        
        print(f"    Science: {student.science_grade}")
        print(f"Average: {student.average:.2f}")