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



CREATE TABLE race(
race_id INT AUTO_INCREMENT PRIMARY KEY,
season_id INT NOT NULL,
round_number INT NOT NULL
GrandPrix_name VARCHAR(255) NOT NULL,
circuit_id INT NOT NULL,
race_datetime datetime NOT NULL,
FOREIGN KEY (season_id) REFERENCES Seasons(season_id),
FOREIGN KEY (circuit_id) REFERENCES circuits(circuit_id)
);



CREATE TABLE RaceResults(
result_id INT AUTO_INCREMENT PRIMARY KEY,
position INT NOT NULL,
driver_id INT NOT NULL,
constructor_id INT NOT NULL,
status_flag VARCHAR(255),
best_lap_time TIME,
race_time TIME,
points INT NOT NULL,
Race_id INT NOT NULL,
FOREIGN KEY(driver_id) REFERENCES Drivers(driver_id),
FOREIGN KEY(race_id) REFERENCES race(race_id),
FOREIGN KEY(constructor_id) REFERENCES Constructors(Constructor_id)
);


CREATE TABLE driverConstructor(
season_id INT NOT NULL,
driver_id INT NOT NULL,
constructor_id INT,
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

