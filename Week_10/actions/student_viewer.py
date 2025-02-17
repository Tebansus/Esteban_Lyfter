def display_students(students_dict):
    # Iterate over each student in the dictionary
    for name, info in students_dict.items():
        # Print the student's name
        print(f"\nStudent: {name}")
        # Print the student's section
        print(f"Section: {info['section']}")
        # Print the student's grades
        print("Grades: ")       
        print(f"    Spanish: {info['spanish_grade']}")
        print(f"    English: {info['english_grade']}")        
        print(f"    Social Studies: {info['social_studies_grade']}")        
        print(f"    Science: {info['science_grade']}")
        # Print the student's average grade, formatted to 2 decimal places
        print(f"Average: {info['average']:.2f}")