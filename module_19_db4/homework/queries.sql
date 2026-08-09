-- select avg(ag.grade) as avg_grade,
--        t.full_name as teacher
--     from teachers t
-- join assignments a on a.teacher_id = t.teacher_id
-- join assignments_grades ag on a.assisgnment_id = ag.assisgnment_id
-- group by t.teacher_id
-- order by avg_grade asc
-- limit 1

-- select s.student_id, s.full_name,avg(ag.grade) avg
--     from students s
-- join assignments_grades ag on ag.student_id = s.student_id
-- group by s.student_id
-- order by avg desc
-- limit 10
--
--

-- SELECT s.student_id FROM students_groups sg
-- join students s on sg.group_id = s.group_id
-- where sg.teacher_id in (
--     select t.teacher_id as teacher
--     from teachers t
--     join assignments a on a.teacher_id = t.teacher_id
--     join assignments_grades ag on a.assisgnment_id = ag.assisgnment_id
--     group by t.teacher_id
--     order by avg(ag.grade) desc
--     limit 1
--     )

-- SELECT s.student_id FROM students_groups sg
-- join (select t.teacher_id as teacher
--       from teachers t
--                join assignments a on a.teacher_id = t.teacher_id
--                join assignments_grades ag on a.assisgnment_id = ag.assisgnment_id
--       group by t.teacher_id
--       order by avg(ag.grade) desc
--       limit 1) on sg.teacher_id = teacher
-- join students s on sg.group_id = s.group_id



-- select s.group_id,
--        avg(overdue.overdue_count),
--        max(overdue.overdue_count),
--        min(overdue.overdue_count)
--        from (select ag.student_id, COUNT(ag.student_id) AS overdue_count from assignments a
--     join assignments_grades ag on a.assisgnment_id = ag.assisgnment_id
--     where ag.date > a.due_date
--     group by ag.student_id) as overdue
-- join students s on s.student_id = overdue.student_id
-- group by s.group_id


-- select count(s.student_id) from students_groups sg
-- join students s on s.group_id = sg.group_id

-- select avg(ag.grade) from assignments_grades ag

-- select count(s.student_id) from students s
-- where s.student_id not in (
--     select DISTINCT ag.student_id from assignments_grades ag
--     )

-- select DISTINCT count(ag.student_id) from assignments a
-- join assignments_grades ag on a.assisgnment_id = ag.assisgnment_id
-- where a.due_date < ag.date

-- SELECT
--     s.group_id,
--     SUM(sub.retries) AS retry_attempts
-- FROM (
--     SELECT
--         student_id,
--         assisgnment_id,
--         COUNT(*) AS retries
--     FROM assignments_grades
--     GROUP BY student_id, assisgnment_id
--     HAVING COUNT(*) > 1
-- ) AS sub
-- JOIN students s ON sub.student_id = s.student_id
-- GROUP BY s.group_id;

-- select ag.assisgnment_id, avg(ag.grade) avg from assignments_grades ag
-- where ag.assisgnment_id in (
--     select ag2.assisgnment_id from assignments a
--     join assignments_grades ag2 on ag2.assisgnment_id = a.assisgnment_id
--     WHERE a.assignment_text LIKE '%прочит%' OR a.assignment_text LIKE '%выуч%'
-- )
-- group by ag.assisgnment_id
-- order by avg desc