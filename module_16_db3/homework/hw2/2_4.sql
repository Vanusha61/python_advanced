select * from customer c
JOIN "order" o ON c.customer_id = o.customer_id
where c.manager_id is NULL
