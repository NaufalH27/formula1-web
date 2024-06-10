USE f1;

#mysql need to use 'secure_file_prive' path provided by the server to access some file
LOAD DATA INFILE '/path/to/secure_file_prive/constructor_list.csv'
INTO TABLE Constructors
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(constructor_name, constructor_nationality, constructorRef);



