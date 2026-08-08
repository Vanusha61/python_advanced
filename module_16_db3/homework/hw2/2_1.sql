select
    c.full_name AS customer_name,
    m.full_name AS manager_name,
    o.purchase_amount,
    o.date
from "order" o
join customer c on c.customer_id = o.customer_id
join manager m on c.manager_id = m.manager_id