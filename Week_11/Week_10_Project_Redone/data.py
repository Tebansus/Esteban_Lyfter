import csv
import os
from students import Student
def load_data_registry(filepath):
    required_student_fields = ['full_name', 'section', 'spanish_grade', 'english_grade', 'social_studies_grade', 'science_grade', 'average']    
    students = {}
    
    try:
        with open(filepath, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            
            # Validate CSV header
            if not all(field in reader.fieldnames for field in required_student_fields):
                return {}
            
            # Process each row
            for row in reader:
                # Validate required fields exist and are non-empty
                try:
                    full_name = row['full_name'].strip()
                    section = row['section'].strip()
                    
                    # Validate grades
                    spanish = float(row['spanish_grade'])
                    english = float(row['english_grade'])
                    social_studies = float(row['social_studies_grade'])
                    science = float(row['science_grade'])
                    average = float(row['average'])
                except (KeyError, ValueError):
                    print(f"Wrong Values and keys, please provide another file. No data loaded.")
                    return {}
                
                # Check valid ranges for the grades
                if not all(0 <= grade <= 100 for grade in [spanish, english, social_studies, science]):
                    print(f"Wrong Values, please provide another file. No data loaded.")
                    return {}
                
                # Check required fields not empty or None
                if not full_name or not section:
                    print(f"Wrong Values, please provide another file. No data loaded.")
                    return {}
                
                # Add to dictionary the loaded data
                students[full_name] = Student(  # Replace dictionary with Student object
                    full_name=full_name,
                    section=section,
                    spanish_grade=spanish,
                    english_grade=english,
                    social_studies_grade=social_studies,
                    science_grade=science,
                    average=average
                )
            
            # Must have at least one valid student
            if not students:
                print(f"Wrong Values, please provide another file. No data loaded.")
                return {}
            
            return students
    
    except FileNotFoundError:
        print(f"File couldn't be found, please provide a valid file path.")
        return {}
    except Exception as e:
        print(f"An error ocurred for the information: {e}, couldn't load the file.")
        # Catch other potential errors (e.g., permission issues)
        return {}
    
    
def save_student_registry(students_dict, filepath=None):
   
    if not students_dict:
        return False

    required_fields = ['full_name', 'section','spanish_grade', 'english_grade','social_studies_grade', 'science_grade','average']

    # Define the rows based on the student object instead of the dictionary
    rows = []
    for name, student in students_dict.items():  # student is now a Student object
        rows.append({
            'full_name': name,
            'section': student.section,
            'spanish_grade': student.spanish_grade,
            'english_grade': student.english_grade,
            'social_studies_grade': student.social_studies_grade,
            'science_grade': student.science_grade,
            'average': student.average
        })

    # Define the default path and try to use the provided one. If it fails, fallback to default.
    default_path = "student_registry_saved.csv"
    target_path = None

    try:
        # Validate and format filepath
        if filepath and str(filepath).strip():
            target_path = str(filepath).strip()
            if not target_path.lower().endswith('.csv'):
                target_path += '.csv'
        else:
            target_path = default_path

        # Try saving to requested path
        with open(target_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=required_fields)
            writer.writeheader()
            writer.writerows(rows)
        return True

    except:
        # Fallback to default path if any error occurs
        try:
            with open(default_path, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=required_fields)
                writer.writeheader()
                writer.writerows(rows)
            return True
        except:
            return False
    
    