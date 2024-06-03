CREATE DATABASE F1;
USE F1;

CREATE TABLE Constructors(
constructor_id INT AUTO_INCREMENT PRIMARY KEY,
constructor_name VARCHAR(255) unique NOT NULL,
constructor_nationality VARCHAR(255)
);

CREATE TABLE Drivers(
driver_id INT AUTO_INCREMENT PRIMARY KEY,
driver_firstname VARCHAR(255) NOT NULL,
driver_lastname VARCHAR(255),
driver_nationality VARCHAR(255),
abbrevation VARCHAR(255)
);

create table  Seasons(
season_year INT PRIMARY KEY
);


CREATE TABLE GrandPrix(
gp_id INT AUTO_INCREMENT PRIMARY KEY,
gp_name VARCHAR(255) NOT NULL,
track_country VARCHAR(255)
);



create table race(
race_id INT AUTO_INCREMENT PRIMARY KEY,
season_id INT NOT NULL,
gp_id INT NOT NULL,
race_date date NOT NULL,
FOREIGN KEY (season_id) REFERENCES Seasons(season_id),
FOREIGN KEY (gp_id) REFERENCES GrandPrix(gp_id)
);



create table RaceResults(
result_id INT AUTO_INCREMENT PRIMARY KEY,
driver_id INT,
position INT ,
poINTs INT NOT NULL,
Race_id INT NOT NULL,
FOREIGN KEY(driver_id) REFERENCES Drivers(driver_id),
FOREIGN KEY(race_id) REFERENCES race(race_id)
);



CREATE TABLE DriverNumber (
    driver_id INT,
    season_id INT,
    PRIMARY KEY (driver_id, season_id),
    FOREIGN KEY (driver_id) REFERENCES Drivers(driver_id),
    FOREIGN KEY (season_id) REFERENCES Seasons(season_id)
);

CREATE TABLE driverConstructor(
    driver_id INT,
    season_id INT,
    constructor_id INT,
    PRIMARY KEY (driver_id, season_id, constructor_id),
    FOREIGN KEY (driver_id) REFERENCES Drivers(driver_id),
    FOREIGN KEY (season_id) REFERENCES Seasons(season_id),
    FOREIGN KEY (constructor_id) REFERENCES constructors(constructor_id)
);




