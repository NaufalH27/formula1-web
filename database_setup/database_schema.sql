CREATE DATABASE test;
use test;

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
    race_ref VARCHAR(255) AS (CONCAT(season_ref,"-", round_number)) STORED,
    season_id INT NOT NULL,
    season_ref INT NOT NULL,
    circuit_id INT NOT NULL,
    circuit_ref VARCHAR(255),
    race_date DATE NOT NULL,
    round_number INT NOT NULL,
	GrandPrix_name VARCHAR(255) NOT NULL,
    UNIQUE KEY unique_constraint(round_number, season_ref),
	FOREIGN KEY (season_id) REFERENCES Seasons(season_id),
	FOREIGN KEY (circuit_id) REFERENCES circuits(circuit_id)
);


CREATE TABLE raceParticipants(
	participant_id INT AUTO_INCREMENT PRIMARY KEY,
    participant_ref VARCHAR(255) AS (CONCAT(race_ref,"-", driver_id,"-", driver_number)) STORED,
    Race_id INT NOT NULL,
    race_ref VARCHAR(255) NOT NULL,
	driver_id INT NOT NULL,
	driver_ref VARCHAR(255) NOT NULL,
    constructor_id INT NOT NULL,
    constructor_ref VARCHAR(255) NOT NULL, 
    driver_number INT NOT NULL,
	UNIQUE KEY unique_constraint(race_ref, driver_id, driver_number),
	FOREIGN KEY(driver_id) REFERENCES Drivers(driver_id),
	FOREIGN KEY(race_id) REFERENCES races(race_id),
	FOREIGN KEY(constructor_id) REFERENCES Constructors(Constructor_id)
);


CREATE TABLE raceResults(
	raceresult_id INT PRIMARY KEY AUTO_INCREMENT,
    participant_id INT NOT NULL,
	participant_ref VARCHAR(255) NOT NULL,
	position INT NOT NULL,
    position_text VARCHAR(255) NOT NULL,
    status_flag VARCHAR(255) NOT NULL,
	best_lap_time TIME,
	driver_race_time VARCHAR(255),
	points INT NOT NULL,
    FOREIGN KEY (participant_id) REFERENCES raceParticipants(participant_id)
);


CREATE TABLE qualifyingResults(
	qualifyingresult_id INT PRIMARY KEY AUTO_INCREMENT,
    participant_id INT NOT NULL,
	participant_ref VARCHAR(255) NOT NULL,
    qualifying_position INT NOT NULL,
    Q1 TIME,
    Q2 TIME,
    Q3 TIME,
    FOREIGN KEY (participant_id) REFERENCES raceParticipants(participant_id)
);



CREATE TABLE DriverTotalPoints (
	season_id INT NOT NULL,
    driver_id INT NOT NULL,
    PRIMARY KEY (season_id, driver_id),
    total_points INT DEFAULT 0,
    FOREIGN KEY (driver_id) REFERENCES Drivers(driver_id)
);

CREATE TABLE ConstructorTotalPoints (
	season_id INT NOT NULL,
    constructor_id INT NOT NULL,
    PRIMARY KEY (season_id, constructor_id),
    total_points INT DEFAULT 0,

    FOREIGN KEY (constructor_id) REFERENCES Constructors(constructor_id)
);

DELIMITER $$

CREATE TRIGGER before_insert_races
BEFORE INSERT ON races
FOR EACH ROW
BEGIN
    DECLARE temp_season_id INT;
    DECLARE temp_circuit_id INT;

    SELECT season_id INTO temp_season_id FROM Seasons WHERE season_year = NEW.season_ref;
    SELECT circuit_id INTO temp_circuit_id FROM Circuits WHERE circuit_ref = NEW.circuit_ref;

    SET NEW.season_id = temp_season_id;
    SET NEW.circuit_id = temp_circuit_id;
END$$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER before_insert_raceParticipants
BEFORE INSERT ON raceParticipants
FOR EACH ROW
BEGIN
    DECLARE temp_race_id INT;
    DECLARE temp_driver_id INT;
    DECLARE temp_constructor_id INT;
    
    SELECT race_id INTO temp_race_id FROM Races WHERE race_ref = NEW.race_ref;
    SELECT driver_id INTO temp_driver_id FROM drivers WHERE driver_ref = NEW.driver_ref;
    SELECT constructor_id INTO temp_constructor_id FROM constructors WHERE constructor_ref = NEW.constructor_ref;
    
    SET NEW.race_id = temp_race_id;
    SET NEW.driver_id = temp_driver_id;
    SET NEW.constructor_id = temp_constructor_id;
END$$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER before_insert_raceResults
BEFORE INSERT ON raceResults
FOR EACH ROW
BEGIN 
	
    DECLARE temp_participant_id INT;
    SELECT participant_id INTO temp_participant_id FROM raceParticipants WHERE participant_ref = NEW.participant_ref;
    SET NEW.participant_id = temp_participant_id;

END$$

DELIMITER ;


DELIMITER $$

CREATE TRIGGER before_insert_qualifyingResults
BEFORE INSERT ON qualifyingResults
FOR EACH ROW
BEGIN 

    DECLARE temp_participant_id INT;
    SELECT participant_id INTO temp_participant_id FROM raceParticipants WHERE participant_ref = NEW.participant_ref;
    SET NEW.participant_id = temp_participant_id;

END$$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER update_total_points
AFTER INSERT ON raceResults
FOR EACH ROW
BEGIN

    DECLARE v_season_id INT;
    DECLARE v_driver_id INT;
    DECLARE v_constructor_id INT;
    
    SELECT r.season_id, rp.driver_id, rp.constructor_id
    INTO v_season_id, v_driver_id, v_constructor_id
    FROM raceParticipants rp
    JOIN races r ON rp.race_id = r.race_id
    WHERE rp.participant_id = NEW.participant_id;
    
    INSERT INTO DriverTotalPoints (season_id, driver_id, total_points)
    VALUES (v_season_id, v_driver_id, NEW.points)
    ON DUPLICATE KEY UPDATE total_points = total_points + NEW.points;

    INSERT INTO ConstructorTotalPoints (season_id, constructor_id, total_points)
    VALUES (v_season_id, v_constructor_id, NEW.points)
    ON DUPLICATE KEY UPDATE total_points = total_points + NEW.points;
END$$
DELIMITER ;
