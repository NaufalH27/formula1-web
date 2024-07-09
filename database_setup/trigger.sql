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
