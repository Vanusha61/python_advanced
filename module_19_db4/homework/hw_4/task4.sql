select s.group_id,
       avg(overdue.overdue_count),
       max(overdue.overdue_count),
       min(overdue.overdue_count)
       from (select ag.student_id, COUNT(ag.student_id) AS overdue_count from assignments a
    join assignments_grades ag on a.assisgnment_id = ag.assisgnment_id
    where ag.date > a.due_date
    group by ag.student_id) as overdue
join students s on s.student_id = overdue.student_id
group by s.group_id