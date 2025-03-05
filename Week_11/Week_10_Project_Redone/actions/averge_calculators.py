def average_the_averages(student_registry):
    # Calculate the average of all students
    average_total = 0
    for name, student in student_registry.items():
        # Use student.average instead of student['average']
        average_total += student.average  
        
    average_total /= len(student_registry)
    print(f"The average of all students is: {average_total:.2f}")

def top3_average(student_registry):
    # Sort students by average in descending order
    sorted_students = sorted(
        student_registry.items(), 
        key=lambda item: item[1].average,  # Access .average attribute
        reverse=True
    )
    
    # Get top 3 (or fewer if there aren't enough students)
    top_students = sorted_students[:3]
    
    # Print ranking with formatted averages
    for rank, (name, student) in enumerate(top_students, start=1):  
        # Use enumerate to get the rank and attribute access for the student
        print(f"{rank}. {name} = {student.average:.2f}") 