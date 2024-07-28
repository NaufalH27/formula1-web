CREATE DATABASE f1db;
USE f1db;

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
    season_year INT NOT NULL,
    round_number INT NOT NULL,
    circuit_id INT NOT NULL,
    race_date DATE NOT NULL,
    GrandPrix_name VARCHAR(255) NOT NULL,
    UNIQUE KEY unique_constraint(round_number, season_year),
    FOREIGN KEY (circuit_id) REFERENCES Circuits(circuit_id)
);

CREATE TABLE raceParticipants(
    participant_id INT AUTO_INCREMENT PRIMARY KEY,
    race_id INT NOT NULL,
    driver_id INT NOT NULL,
    constructor_id INT NOT NULL,
    driver_number INT NOT NULL,
    UNIQUE KEY unique_constraint(race_id,driver_id, constructor_id, driver_number),
    FOREIGN KEY(driver_id) REFERENCES Drivers(driver_id),
    FOREIGN KEY(race_id) REFERENCES races(race_id),
    FOREIGN KEY(constructor_id) REFERENCES Constructors(constructor_id)
);

CREATE TABLE raceResults(
    raceresult_id INT AUTO_INCREMENT PRIMARY KEY,
    participant_id INT NOT NULL,
    position INT NOT NULL,
    position_text VARCHAR(255) NOT NULL,
    status_flag VARCHAR(255) NOT NULL,
    best_lap_time TIME,
    driver_race_time VARCHAR(255),
    points INT NOT NULL,
    FOREIGN KEY (participant_id) REFERENCES raceParticipants(participant_id)
);

CREATE TABLE qualifyingResults(
    qualifyingresult_id INT AUTO_INCREMENT PRIMARY KEY,
    participant_id INT NOT NULL,
    qualifying_position INT NOT NULL,
    Q1 TIME,
    Q2 TIME,
    Q3 TIME,
    FOREIGN KEY (participant_id) REFERENCES raceParticipants(participant_id)
);

CREATE TABLE DriverTotalPoints (
    season_year INT NOT NULL,
    driver_id INT NOT NULL,
    PRIMARY KEY (season_year, driver_id),
    total_points INT DEFAULT 0,
    FOREIGN KEY (driver_id) REFERENCES Drivers(driver_id)
);

CREATE TABLE ConstructorTotalPoints (
    season_year INT NOT NULL,
    constructor_id INT NOT NULL,
    PRIMARY KEY (season_year, constructor_id),
    total_points INT DEFAULT 0,
    FOREIGN KEY (constructor_id) REFERENCES Constructors(constructor_id)
);

DELIMITER $$

CREATE TRIGGER update_total_points
AFTER INSERT ON raceResults
FOR EACH ROW
BEGIN
    DECLARE v_season_year INT;
    DECLARE v_driver_id INT;
    DECLARE v_constructor_id INT;
    
    SELECT races.season_year, raceParticipants.driver_id, raceParticipants.constructor_id
    INTO v_season_year, v_driver_id, v_constructor_id
    FROM raceParticipants 
    JOIN races ON raceParticipants.race_id = races.race_id
    WHERE raceParticipants.participant_id = NEW.participant_id;
    
    INSERT INTO DriverTotalPoints (season_year, driver_id, total_points)
    VALUES (v_season_year, v_driver_id, NEW.points)
    ON DUPLICATE KEY UPDATE total_points = total_points + NEW.points;

    INSERT INTO ConstructorTotalPoints (season_year, constructor_id, total_points)
    VALUES (v_season_year, v_constructor_id, NEW.points)
    ON DUPLICATE KEY UPDATE total_points = total_points + NEW.points;
END$$
DELIMITER ;
