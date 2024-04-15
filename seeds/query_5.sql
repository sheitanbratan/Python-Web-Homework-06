SELECT lecturer_name, subject
FROM subjects
WHERE lecturer_name = (SELECT name FROM lecturers WHERE id=1)