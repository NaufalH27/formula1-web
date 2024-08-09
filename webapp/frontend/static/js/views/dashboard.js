import abstractView from "./abstractView.js";
import generateHtmlForDriverLeaderboard from "../content/dashboard/renderDriverStandings.js"
import generateHtmlForConstructorLeaderboard from "../content/dashboard/renderConstructorStandings.js"
import generateHtmlForSchedule from "../content/dashboard/renderScheduleCard.js"
import generateChart from "../content/dashboard/renderPointChart.js"
import scheduleScroll from "../ui/scheduleScroll.js";


export default class extends abstractView {
    constructor(){
        super();
        this.setTitle("Dashboard");

    }

    loadUi(){
        scheduleScroll()
    }
    
    async getHtml(){
        const driverLeaderboardHtml = await generateHtmlForDriverLeaderboard();
        const constructorLeaderboardHtml = await generateHtmlForConstructorLeaderboard();
        const scheduleHtml = await generateHtmlForSchedule();
        generateChart()

        return `
        <div class="dashboardStandingArea">
            <div class="yearTitleContainer">
                <div class="yearTitle" id="currentYearTitle">${this.getCurrentYear()}</div>
                <div class="yearTitle" id="leaderboardTitle">standings</div>
             </div>
            <div class="tableContainer">
                <div class="title">Driver</div>
                <table>
                    <thead>
                        <tr>
                            <th class="numberCell">No</th>
                            <th class="nameCell">Driver Name</th>
                            <th class="pointsCell">Points</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${driverLeaderboardHtml}
                    <tbody>
                </table>
                <a href="/results" class="detailButton"  data-link >More Detail →</a>
            </div>
            <div class="tableContainer">
            <div class="title">Constructor</div>
                <table>
                    <thead>
                        <tr>
                            <th class="numberCell">No</th>
                            <th class="nameCell">Constructor Name</th>
                            <th class="pointsCell">Points</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${constructorLeaderboardHtml}
                    <tbody>
                </table>
                <a href="/results" class="detailButton"  data-link>More Detail →</a>
            </div>
        </div>
        <div class="mainArea">
            <div class = raceScheduleAreaContainer> 
                <div class="raceScheduleArea">
                    <div class="buttonAreaAboveSchedule">
                        <div class="leftSideOfbuttonAreaAboveSchedule">
                            <a class="scheduleText">2024 Schedule</a>
                        </div>
                        <div class="rightSideOfbuttonAreaAboveSchedule">
                            <a href="/schedule" class="scheduleButton" data-link>More Schedule →</a>
                        </div>
                    </div>
                    <div id="left" class="raceScheduleButton">
                        <i class="fa-solid fa-angle-left"></i>
                    </div>
                    <div class="raceScheduleContainer"  onmousedown="event.preventDefault ? event.preventDefault() : event.returnValue = false">
                        ${scheduleHtml}
                        <div class="scheduleDeadEnd">
                            <div class="text">
                                no schedule left
                            </div>
                        </div>
                    </div>
                    <div id="right" class="raceScheduleButton">
                        <i class="fa-solid fa-angle-right"></i>
                    </div>
                </div>
            </div>
            DRIVER CHARTS
            <canvas id="driverPointChart" class="pointCharts"></canvas>
            CONSTRUCTOR CHARTS
            <canvas id="constructorPointChart" class="pointCharts"></canvas>
        </div>`
         ;
    }
   
}


