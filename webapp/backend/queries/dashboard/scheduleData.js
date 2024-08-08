const db = require("../../database.js");

const getSchedule = async () => {
    const dateNow = new Date();
    const utcDateString = dateNow.toISOString().split('T')[0];
    const utcTimeString = dateNow.toISOString().split('T')[1].split('.')[0];

    const databaseQuery = await db.query(`
        SELECT season_year, round_number, race_date, race_time_in_utc, GrandPrix_name, circuit_location
        FROM races 
        JOIN circuits ON races.circuit_id = circuits.circuit_id 
        WHERE race_date > ? OR (race_date = ? AND race_time_in_utc > ?)
    `, [utcDateString, utcDateString, utcTimeString]);

    return databaseQuery;
}

module.exports = { getSchedule };