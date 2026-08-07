select o.order_no, m.full_name, c.full_name from "order" o
join manager m on o.manager_id = m.manager_id
join customer c on o.customer_id = c.customer_id
where m.city != c.city