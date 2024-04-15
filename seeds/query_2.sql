SELECT subject, student_name, ROUND(AVG(grade), 2) as avg_grade
FROM grades
WHERE subject = 'English'
GROUP BY student_name
ORDER BY avg_grade DESC
LIMIT 1;