USE f1;

#mysql need to use 'secure_file_prive' path provided by the server to access some file
LOAD DATA INFILE '/path/to/secure_file_prive/f1driver_list.csv' 
INTO TABLE drivers
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(driver_firstname, driver_lastname, driver_nationality, abbreviation);

SELECT * FROM drivers;
