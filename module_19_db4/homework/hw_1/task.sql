select avg(ag.grade) as avg_grade,
       t.full_name as teacher
    from teachers t
join assignments a on a.teacher_id = t.teacher_id
join assignments_grades ag on a.assisgnment_id = ag.assisgnment_id
group by t.teacher_id
order by avg_grade asc
limit 1