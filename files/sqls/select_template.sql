SELECT *
FROM TABLES
WHERE BASE_DT >= {{ data_interval_start | ds }}
