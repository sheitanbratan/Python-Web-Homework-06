SELECT lecturers.name, lecturers.subject, students.name AS student_name
FROM lecturers, students
WHERE students.id = 1
AND lecturers.name = (SELECT name FROM lecturers WHERE id = 2)