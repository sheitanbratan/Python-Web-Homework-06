SELECT subjects.lecturer_name, subjects.subject, ROUND(AVG(grades.grade), 3) AS average_grade
FROM subjects
JOIN grades ON subjects.subject = grades.subject
WHERE subjects.lecturer_name = (
    SELECT lecturer_name FROM subjects WHERE id = 1
)
GROUP BY subjects.lecturer_name, subjects.subject;
