CREATE DATABASE F1;
USE F1;

CREATE TABLE Constructors(
	constructor_id INT AUTO_INCREMENT PRIMARY KEY,
	constructor_ref VARCHAR(255) UNIQUE NOT NULL,
	constructor_name VARCHAR(255) NOT NULL,
	constructor_nationality VARCHAR(255),
	url VARCHAR(1000)
);


CREATE TABLE Drivers(  
	driver_id INT AUTO_INCREMENT PRIMARY KEY,
	driver_ref VARCHAR(255) UNIQUE NOT NULL,
	driver_firstname VARCHAR(255) NOT NULL,
	driver_lastname VARCHAR(255),
	driver_nationality VARCHAR(255),
	driver_birthdate DATE NOT NULL,
	url VARCHAR(1000)
);


CREATE TABLE  Seasons(
	season_id INT AUTO_INCREMENT PRIMARY KEY,
	season_year INT NOT NULL
);


CREATE TABLE Circuits(
	circuit_id INT AUTO_INCREMENT PRIMARY KEY,
	circuit_ref VARCHAR(255)  UNIQUE NOT NULL,
	circuit_name VARCHAR(255) NOT NULL,
	circuit_country VARCHAR(255) NOT NULL,
	circuit_location VARCHAR(255) NOT NULL,
	url VARCHAR(1000)
);


CREATE TABLE races(
	race_id INT AUTO_INCREMENT PRIMARY KEY,
    round_number INT NOT NULL,
	season_id INT NOT NULL,
	GrandPrix_name VARCHAR(255) NOT NULL,
	circuit_id INT NOT NULL,
    race_ref INT AS (CONCAT(season_id, round_number)) STORED,
    UNIQUE KEY unique_constraint(round_number, season_id),
	FOREIGN KEY (season_id) REFERENCES Seasons(season_id),
	FOREIGN KEY (circuit_id) REFERENCES circuits(circuit_id)
);


CREATE TABLE raceParticipants(
	participant_id INT AUTO_INCREMENT PRIMARY KEY,
    Race_id INT NOT NULL,
	driver_id INT NOT NULL,
    driver_number INT NOT NULL,
	constructor_id INT NOT NULL,
    participant_ref INT AS (CONCAT(race_id, driver_id)) STORED,
	UNIQUE KEY unique_constraint(race_id, driver_id),
	FOREIGN KEY(driver_id) REFERENCES Drivers(driver_id),
	FOREIGN KEY(race_id) REFERENCES races(race_id),
	FOREIGN KEY(constructor_id) REFERENCES Constructors(Constructor_id)
);


CREATE TABLE raceResults(
	raceresult_id INT PRIMARY KEY AUTO_INCREMENT,
    participant_id INT NOT NULL,
    race_date DATE NOT NULL,
    race_time TIME,
	position INT NOT NULL,
    position_text VARCHAR(255) NOT NULL,
    status_flag VARCHAR(255) NOT NULL,
	best_lap_time TIME,
	driver_race_time TIME,
	points INT NOT NULL,
    FOREIGN KEY (participant_id) REFERENCES raceParticipants(participant_id)
);


CREATE TABLE qualifyingResults(
	qualifyingresult_id INT PRIMARY KEY AUTO_INCREMENT,
    participant_id INT NOT NULL,
    qualifying_position INT NOT NULL,
    qualifying_date DATE NOT NULL,
    qualifying_time TIME,
    Q1 TIME,
    Q2 TIME,
    Q3 TIME,
    FOREIGN KEY (participant_id) REFERENCES raceParticipants(participant_id)
);


CREATE TABLE driverConstructor(
	season_id INT NOT NULL,
	driver_id INT NOT NULL,
	constructor_id INT NOT NULL,
	FOREIGN KEY (driver_id) REFERENCES Drivers(driver_id),
	FOREIGN KEY (season_id) REFERENCES Seasons(season_id),
	FOREIGN KEY (constructor_id) REFERENCES constructors(constructor_id)
);


CREATE TABLE DriverTotalPoints (
    driver_id INT PRIMARY KEY,
    total_points INT DEFAULT 0,
    FOREIGN KEY (driver_id) REFERENCES Drivers(driver_id)
);


CREATE TABLE ConstructorTotalPoints (
    constructor_id INT PRIMARY KEY,
    total_points INT DEFAULT 0,
    FOREIGN KEY (constructor_id) REFERENCES Constructors(constructor_id)
);


