select s.student_id, s.full_name,avg(ag.grade) avg
    from students s
join assignments_grades ag on ag.student_id = s.student_id
group by s.student_id
order by avg desc
limit 10