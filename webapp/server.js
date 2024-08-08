const express = require("express");
const path = require("path");
const dashboardStandings = require("./backend/queries/Dashboard/standingData.js");
const scheduleData = require("./backend/queries/dashboard/scheduleData.js")

const app = express();

app.use("/static", express.static(path.resolve(__dirname,"frontend", "static")));

app.get("/api/dashboardLeaderboard/driver", async (req, res) => {
    const awaitedJsonData = await dashboardStandings.getCurrentSeasonDriverPoints();
    res.send(awaitedJsonData);
});

app.get("/api/dashboardLeaderboard/constructor", async (req, res) => {
    const awaitedJsonData = await dashboardStandings.getCurrentSeasonConstructorPoints();
    res.send(awaitedJsonData);
});

app.get("/api/dashboardSchedule", async(req, res) => {
    const awaitedJsonData = await scheduleData.getSchedule();
    res.json(awaitedJsonData);
})

app.get("/*", (req, res) => {
    res.sendFile(path.resolve(__dirname, "frontend", "index.html"));

});


app.listen(process.env.port || 8080, () => console.log("Server Running..."));