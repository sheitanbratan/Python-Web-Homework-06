SELECT subject, group_name, student_name, ROUND(AVG(grade), 2) as avg_grade
FROM grades
WHERE subject = 'English'
GROUP BY group_name
ORDER BY avg_grade