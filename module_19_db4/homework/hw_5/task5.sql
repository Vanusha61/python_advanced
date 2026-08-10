SELECT
    sg.group_id, -- id группы студентов
    count(s.student_id) AS total_student, -- количество студентов
    (
        SELECT
            avg(ag1.grade)
        FROM students s2
        LEFT JOIN assignments_grades ag1 ON ag1.student_id = s2.student_id
        WHERE
            s2.group_id = sg.group_id
    ) AS avg_group_grade, -- средняя оценка для группы
    (
        SELECT
            count(*)
        FROM students s3
        LEFT JOIN assignments_grades ag2 ON ag2.student_id = s3.student_id
        WHERE
            s3.group_id = sg.group_id
            AND ag2.student_id IS NULL
    ) AS total_student_wo_asgn, -- сколько студентов не сдали работы
    (
        SELECT
            count(*)
        FROM students s4
        JOIN assignments_grades ag3 ON ag3.student_id = s4.student_id
        JOIN assignments a ON a.assisgnment_id = ag3.assisgnment_id
        WHERE
            s4.group_id = sg.group_id
            AND a.due_date < ag3.date
    ) AS total_student_overdue, -- сколько студентов опоздали со задачей работы
    (
        SELECT
            sum(redue)
        FROM (
            SELECT
                count(ag4.assisgnment_id) AS redue
            FROM students s5
            JOIN assignments_grades ag4 ON ag4.student_id = s5.student_id
            WHERE
                s5.group_id = sg.group_id
            GROUP BY s5.student_id
            HAVING
                redue > 1
        )
    ) AS total_redue -- сколько в каждой группе было повторных попыток сдать работу
FROM students_groups sg
JOIN students s ON s.group_id = sg.group_id
GROUP BY sg.group_id
