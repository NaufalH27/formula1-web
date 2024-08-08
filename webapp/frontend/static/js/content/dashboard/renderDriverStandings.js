import { fetchJsonData } from "../../helper/apiHelper.js";


export default async() => {
    let driverStandingHtml = '';

    const jsonData = await fetchJsonData("/api/dashboardLeaderboard/driver");
    jsonData.forEach((driver, rank) => {
        driverStandingHtml += `<tr class="entityRow">
                            <td class="numberCell">${rank+1}</td>
                            <td class="nameCell">${driver["driver_firstName"] +" " + driver["driver_lastName"]}</td>
                            <td class="pointsCell">${driver["total_points"]}</td>
                        </tr>`;
    });
    return driverStandingHtml;
}

