SELECT s.student_id FROM students_groups sg
join students s on sg.group_id = s.group_id
where sg.teacher_id in (
    select t.teacher_id as teacher
    from teachers t
    join assignments a on a.teacher_id = t.teacher_id
    join assignments_grades ag on a.assisgnment_id = ag.assisgnment_id
    group by t.teacher_id
    order by avg(ag.grade) desc
    limit 1
    )

SELECT s.student_id FROM students_groups sg
join (select t.teacher_id as teacher
      from teachers t
               join assignments a on a.teacher_id = t.teacher_id
               join assignments_grades ag on a.assisgnment_id = ag.assisgnment_id
      group by t.teacher_id
      order by avg(ag.grade) desc
      limit 1) on sg.teacher_id = teacher
join students s on sg.group_id = s.group_id