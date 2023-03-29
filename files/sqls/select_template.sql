SELECT *
FROM TABLES
WHERE BASE_DT >= {{ data_interaval_start | ds }}
