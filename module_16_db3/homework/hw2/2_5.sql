select * from customer c1
join customer c2 on c1.city = c2.city
and c1.manager_id = c2.manager_id
and c1.customer_id < c2.customer_id