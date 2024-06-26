CREATE DATABASE doctors_appointments;

USE doctors_appointments;

SHOW TABLES;

CREATE TABLE appointments (
    sno int,
    appointment_id VARCHAR(50),
    patient_id VARCHAR(50),
    patient_name VARCHAR(50),
    appointment_date DATE,
    appointment_time TIME,
    purpose_of_visit VARCHAR(50)
);

SELECT * FROM appointments;

LOAD DATA INFILE 'C:\Projects\Langchain\Doctors appointment chatbot\Data.csv'
INTO TABLE appointments
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

SELECT * FROM data;

SELECT * from appointments;