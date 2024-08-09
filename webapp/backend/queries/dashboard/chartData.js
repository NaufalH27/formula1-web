const db = require("../../database.js");

const getFullPointsForCurrentSeason = async () => {
    const dateNow = new Date();
    year = dateNow.getFullYear()

    const databaseQuery = await db.query(`
        SELECT d.driver_id,c.constructor_id, round_number, driver_firstName, driver_lastname, constructor_name,  COALESCE(rr.points, 0) + COALESCE(sr.points, 0) AS total_points
        FROM races r
        JOIN raceParticipants rp  ON r.race_id = rp.race_id
        JOIN raceResults rr ON rr.participant_id = rp.participant_id
        LEFT JOIN sprintResults sr ON sr.participant_id = rp.participant_id
        JOIN drivers d ON d.driver_id = rp.driver_id
        JOIN constructors c ON c.constructor_id = rp.constructor_id
        WHERE season_year = ? order by round_number
    `, [year]);

    return databaseQuery;
}

module.exports = { getFullPointsForCurrentSeason };
