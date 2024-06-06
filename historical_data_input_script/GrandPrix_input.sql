USE f1;

#mysql need to use 'secure_file_prive' path provided by the server to access some file
LOAD DATA INFILE '/path/to/secure_file_prive/GP_list.csv'
INTO TABLE GrandPrix
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(gp_name, track_country);

