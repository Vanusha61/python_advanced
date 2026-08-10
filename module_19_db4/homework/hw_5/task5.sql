select count(s.student_id) from students_groups sg
join students s on s.group_id = sg.group_id

select avg(ag.grade) from assignments_grades ag

select count(s.student_id) from students s
where s.student_id not in (
    select DISTINCT ag.student_id from assignments_grades ag
    )

select DISTINCT count(ag.student_id) from assignments a
join assignments_grades ag on a.assisgnment_id = ag.assisgnment_id
where a.due_date < ag.date

SELECT
    s.group_id,
    SUM(sub.retries) AS retry_attempts
FROM (
    SELECT
        student_id,
        assisgnment_id,
        COUNT(*) AS retries
    FROM assignments_grades
    GROUP BY student_id, assisgnment_id
    HAVING COUNT(*) > 1
) AS sub
JOIN students s ON sub.student_id = s.student_id
GROUP BY s.group_id;