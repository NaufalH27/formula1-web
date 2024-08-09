import { fetchJsonData } from "../../helper/apiHelper.js";

export default async() => {
    let constructorStandingHtml = '';
    const constructorData = await fetchJsonData("/api/dashboardLeaderboard/constructor");
    constructorData.forEach((constructor, rank) => {
        constructorStandingHtml += `<tr class="entityRow">
                            <td class="numberCell">${rank+1}</td>
                            <td class="nameCell">${constructor["constructor_name"]}</td>
                            <td class="pointsCell">${constructor["total_points"]}</td>
                        </tr>`;
    });
    return constructorStandingHtml;
}
