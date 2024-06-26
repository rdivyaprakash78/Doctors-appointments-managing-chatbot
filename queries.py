queries = {
    "date_fetch_query" 
    :
    """WITH CTE1 AS
    (
    SELECT *, COUNT(appointment_id) OVER (PARTITION BY appointment_date) AS total_appointments
    FROM appointments
    )
    SELECT DISTINCT(appointment_date) FROM CTE1
    WHERE 
    (appointment_date BETWEEN CURDATE() AND date_add(CURDATE(), INTERVAL 7 DAY)) 
    AND
    (total_appointments < 9)

    UNION
    (
    WITH RECURSIVE CTE AS
    (
    SELECT CURDATE() AS cur_date
    UNION ALL
    SELECT DATE_ADD(cur_date, INTERVAL 1 DAY) FROM CTE
    WHERE cur_date < DATE_ADD(CURDATE(), INTERVAL 6 DAY)
    )

    SELECT cur_date FROM CTE
    WHERE cur_date
    NOT IN
    (
    SELECT DISTINCT(appointment_date) FROM appointments
    )
    );
    """,

    "current_year" : 

    """SELECT DISTINCT(YEAR(NOW())) FROM appointments;""",

    "time_fetch_query" 
    :
    """SELECT CAST(appointment_time AS CHAR) as APPOINTMENT_TIME FROM appointment_times
    WHERE appointment_time NOT IN
    (
    SELECT appointment_time FROM appointments
    WHERE appointment_date = '{date}');""",

    "patient_id_check_query"
    :
    """SELECT 1 FROM appointments WHERE patient_id = '{id}' ;""",

    "new_user_reg_query"
    :
    """
    SELECT 
                (CONCAT('PAT',

                CONVERT(
                (CONVERT(
                        RIGHT(MAX(patient_id),3),
                        SIGNED
                        ) + 1),CHAR
                        )) )AS new_id
                        FROM appointments;
    """,

    "get_pname_query" 
    :
    """
    SELECT patient_name FROM appointments WHERE patient_id = '{id}';
    """,

    "get_new_appointmentid"
    :
    """
    SELECT 
                (CONCAT('APPT',

                CONVERT(
                (CONVERT(
                        RIGHT(MAX(appointment_id),3),
                        SIGNED
                        ) + 1),CHAR
                        )) )AS new_id
                        FROM appointments;
    """,

    "get_new_sno"
    :
    """
    SELECT MAX(sno) + 1 FROM appointments;
    """,

    "appointment_booking_query" 
    :
    """
    INSERT INTO appointments 
                        (sno, appointment_id, patient_id, patient_name, appointment_date, appointment_time, purpose_of_visit)
                        VALUES 
                        ({sno}, '{appt_id}', '{pat_id}', '{name}', '{date}', '{time}', '{pov}' );
    """
}