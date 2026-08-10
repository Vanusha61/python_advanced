select ag.assisgnment_id, avg(ag.grade) avg from assignments_grades ag
where ag.assisgnment_id in (
    select ag2.assisgnment_id from assignments a
    join assignments_grades ag2 on ag2.assisgnment_id = a.assisgnment_id
    WHERE a.assignment_text LIKE '%прочит%' OR a.assignment_text LIKE '%выуч%'
)
group by ag.assisgnment_id
order by avg desc