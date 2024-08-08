const db = require("../../database.js")

const date = new Date();
const current_year = date.getFullYear()


const getCurrentSeasonDriverPoints = async() => {
    const databaseQuery = await db.query(`SELECT driver_firstName, driver_lastName, total_points
                FROM DriverTotalPoints JOIN drivers ON DriverTotalPoints.driver_id = drivers.driver_id 
                WHERE season_year = ? ORDER BY total_points DESC;`, [current_year])
    return databaseQuery;
}

const getCurrentSeasonConstructorPoints = async() => {
    const databaseQuery = await db.query(`SELECT constructor_name, total_points
                FROM ConstructorTotalPoints JOIN Constructors ON ConstructorTotalPoints.constructor_id = constructors.constructor_id 
                WHERE season_year = ? ORDER BY total_points DESC;`, [current_year]);
        return databaseQuery;
}

module.exports = {getCurrentSeasonDriverPoints, getCurrentSeasonConstructorPoints}