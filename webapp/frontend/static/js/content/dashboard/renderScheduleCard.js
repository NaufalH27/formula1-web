import { fetchJsonData } from "../../helper/apiHelper.js";

export default async () => {
    // Array of month names for formatting dates
    const monthNames = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];

    let scheduleCardsHTML = '';
    
    const scheduleData = await fetchJsonData("/api/dashboardSchedule");
    
    // Process each schedule item
    scheduleData.forEach((race) => {
        // Parse the race date
        const raceDate = new Date(race["race_date"]);
        
        // Compute the next day's date for displaying range
        const nextDayDate = new Date(raceDate);
        nextDayDate.setUTCDate(raceDate.getUTCDate() + 1);
        
        // Extract day, month, and year
        const day = raceDate.getUTCDate();
        const month = monthNames[raceDate.getUTCMonth()];
        const monthAbbreviation = month.slice(0, 3);
        const year = raceDate.getUTCFullYear();
        
        // Extract and format time
        const [hours, minutes] = race["race_time_in_utc"].split(":");
        const formattedTime = `${hours}:${minutes}`;
        
        // Determine if month should be updated
        const nextDay = nextDayDate.getUTCDate();
        const monthSuffix = (nextDay < day) ? `-${monthNames[nextDayDate.getUTCMonth()].slice(0, 3)}` : "";

        // Construct the HTML for this schedule card
        scheduleCardsHTML += `
            <div class="raceSchedule">
                <div class="topScheduleArea">
                    <div class="dateAndMonthScheduleContainer">
                        <div class="dateScheduleText">${day}-${nextDay}</div>
                        <div class="monthScheduleText">${monthAbbreviation}${monthSuffix}</div>
                    </div>  
                </div>
                <div class="bottomScheduleArea">
                    <a href="/" class="GPName">
                        ${race["GrandPrix_name"]} ${year}
                    </a>
                    <div class="roundAndRaceTimeScheduleContainer">   
                        <div class="roundText">Round ${race["round_number"]}</div>
                        <div class="raceTimeSchedule">${formattedTime} UTC</div>
                    </div>   
                </div>
            </div>
        `;
    });
   
    
    return scheduleCardsHTML;
};
