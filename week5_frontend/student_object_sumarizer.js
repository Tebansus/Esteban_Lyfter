// Entrada
const student = {
	name: "John Doe",
	grades: [
		{name: "math",grade: 80},
		{name: "science",grade: 100},
		{name: "history",grade: 60},
		{name: "PE",grade: 90},
		{name: "music",grade: 98}
	]
};

function sumarize_student(student) {
    var student_name = student.name;
    var average_grade = 0;
    var highest_grade = 0;
    var highest_grade_name = "";
    var lowest_grade_name = "";
    var lowest_grade = undefined;
    for (let i = 0; i < student.grades.length; i++) {
        average_grade += student.grades[i].grade;
        if (student.grades[i].grade > highest_grade) {
            highest_grade_name = student.grades[i].name;
            highest_grade = student.grades[i].grade;
        }
        if (student.grades[i].grade < lowest_grade || lowest_grade === undefined) {
            lowest_grade_name = student.grades[i].name;
            lowest_grade = student.grades[i].grade;
        }
    }
    average_grade = average_grade / student.grades.length;
    const summary = {
        student_name: student_name,
        average_grade: average_grade,
        highest_grade: highest_grade_name,
        lowest_grade: lowest_grade_name
    }
    return summary;

}

console.log(sumarize_student(student));