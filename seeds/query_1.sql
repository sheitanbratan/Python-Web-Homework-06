SELECT student_name, ROUND(AVG(grade), 2) as avg_grade
FROM grades
GROUP BY student_name
ORDER BY avg_grade DESC
LIMIT 5;