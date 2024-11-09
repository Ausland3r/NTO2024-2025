-- database: ../TestData/C/conders0.db
WITH factory_year as (
    SELECT capacitor_id from bans b 
    JOIN condensers c ON c.factory_id = b.factory_id and c.year = b.year
    ),
factory as (
    SELECT capacitor_id from bans b
    JOIN condensers c ON c.factory_id = b.factory_id
)
SELECT capacitor_id FROM condensers c
JOIN factories f ON c.factory_id = f.factory_id
JOIN countries co ON f.country_id = co.country_id
WHERE (co.name = 'Russia' and c.capacity >= 500 and c.voltage <= 200 and c.price <= 40
and c.capacitor_id not in factory_year) or (co.name != 'Russia' and c.capacity >= 500 and c.voltage <= 200 and c.price <= 20 and c.factory_id not in factory);


