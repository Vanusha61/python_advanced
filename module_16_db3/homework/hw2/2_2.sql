select c.full_name from customer c
left join "order" o on c.customer_id = o.customer_id
where o.customer_id is NULL
