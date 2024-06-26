SELECT appointment_time
FROM appointments
WHERE appointment_date = CURDATE() + INTERVAL 1 WEEK
  AND appointment_time BETWEEN '17:00:00' AND '21:00:00'
  AND NOT EXISTS(
    SELECT 1
    FROM appointments
    WHERE appointment_date = CURDATE() + INTERVAL 1 WEEK AND appointment_time = appointments.appointment_time
  );
  
  SELECT curdate() + INTERVAL 1 WEEK from appointments;
  
WITH RECURSIVE DateRange AS (
    -- Anchor member
    SELECT 
        CURDATE() AS DateValue
    UNION ALL
    -- Recursive member
    SELECT 
        DateValue + INTERVAL 1 DAY
    FROM 
        DateRange
    WHERE 
        DateValue < CURDATE() + INTERVAL 7 DAY
)
SELECT 
    DateValue
FROM 
    DateRange;
    
SELECT * FROM appointments;

WITH CTE AS
(
SELECT *, COUNT(appointment_id) OVER (PARTITION BY appointment_date) AS total_appointments
FROM appointments
)
SELECT DISTINCT(appointment_date), 9-total_appointments as AVAILABLE_APPOINTMENTS FROM CTE
WHERE 
(appointment_date BETWEEN CURDATE() AND date_add(CURDATE(), INTERVAL 7 DAY)) 
AND
(total_appointments < 9);
    
    
SELECT DISTINCT(CURDATE()) from appointments;
    
SELECT * FROM appointments;

WITH CTE1 AS
    (
    SELECT *, COUNT(appointment_id) OVER (PARTITION BY appointment_date) AS total_appointments
    FROM appointments
    )
SELECT DISTINCT(appointment_date) FROM CTE1
WHERE 
(appointment_date BETWEEN "2024-05-29" AND date_add("2024-05-29", INTERVAL 7 DAY)) 
AND
(total_appointments < 9)

UNION
(
WITH RECURSIVE CTE AS
(
	SELECT "2024-05-29" AS cur_date
    UNION ALL
    SELECT DATE_ADD(cur_date, INTERVAL 1 DAY) FROM CTE
    WHERE cur_date < DATE_ADD("2024-05-29", INTERVAL 6 DAY)
)

SELECT cur_date FROM CTE
WHERE cur_date
NOT IN
(
	SELECT DISTINCT(appointment_date) FROM appointments
)
);
    
    
    
SELECT * FROM appointments;
    