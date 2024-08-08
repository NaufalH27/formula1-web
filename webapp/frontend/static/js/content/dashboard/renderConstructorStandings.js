import { fetchJsonData } from "../../helper/apiHelper.js";

export default async() => {
    let constructorRows = '';
    const jsonData = await fetchJsonData("/api/dashboardLeaderboard/constructor");
    jsonData.forEach((constructor, rank) => {
        constructorRows += `<tr class="entityRow">
                            <td class="numberCell">${rank+1}</td>
                            <td class="nameCell">${constructor["constructor_name"]}</td>
                            <td class="pointsCell">${constructor["total_points"]}</td>
                        </tr>`;
    });
    return constructorRows;
}
