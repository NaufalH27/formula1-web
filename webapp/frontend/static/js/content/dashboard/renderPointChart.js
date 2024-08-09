import { fetchJsonData } from "../../helper/apiHelper.js";


function getRandomColor() {
  var letters = '0123456789ABCDEF';
  var color = '#';
  for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}

export default async() =>{
  const driverMap = new Map()
  const constructorMap = new Map()

  const appendData = (result,maxRound) => {
    let driver = driverMap.get(result.driver_id);
    let constructor = constructorMap.get(result.constructor_id)
    if (!driver){
      driverMap.set(result.driver_id, {
          label: result.driver_firstName + result.driver_lastname,
          data: new Array(maxRound+1).fill(0)
      })
      driver = driverMap.get(result.driver_id);
    }

    if (!constructor){
      constructorMap.set(result.constructor_id, {
        label: result.constructor_name,
        data: new Array(maxRound+1).fill(0)
    })
    constructor = constructorMap.get(result.constructor_id)
    }

    driver.data[result.round_number] += result.total_points;
    constructor.data[result.round_number] += result.total_points;
  }
 
    
    const resultList = await fetchJsonData('/api/fullPointResultForCurrentSeason');
    const maxRound =  resultList[resultList.length - 1].round_number;
    resultList.forEach((result)=> {
      appendData(result,maxRound)
    });

    const driverList = Array.from(driverMap.values())
    const constructorList = Array.from(constructorMap.values())

    function transformArray(arr) {
      return arr.reduce((acc, currentValue, index) => {
          if (index === 0) {
              acc.push(currentValue);
          } else {
              acc.push(currentValue + acc[index - 1]);
          }
          return acc;
      }, []);
  }

  driverList.forEach(driver => {
    driver.data = transformArray(driver.data)
  })

  constructorList.forEach(constructor => {
    constructor.data = transformArray(constructor.data)
  })

    const driverChart = document.getElementById('driverPointChart');
    const constructorChart = document.getElementById('constructorPointChart');
    new Chart(driverChart, {
      type: 'line',
      data: {
        labels: Array.from({ length: maxRound+1}, (_, i) => i),
        datasets: driverList
      },
      options: {
        plugins: {
          legend: {
              display: false
          },
          tooltip: {
              enabled: true
          }
      },
      }
    });

    new Chart(constructorChart, {
      type: 'line',
      data: {
        labels: Array.from({ length: maxRound+1}, (_, i) => i),
        datasets: constructorList
      },
      options: {
        plugins: {
          legend: {
              display: false
          },
          tooltip: {
              enabled: true
          }
      }
      }
    });
    console.log(driverMap.values())
    console.log(constructorMap.values())

}
