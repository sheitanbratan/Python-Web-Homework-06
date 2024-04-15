SELECT student_name, group_name, subject, grade
FROM grades
WHERE group_name = 'group_a'
AND subject = 'Math'