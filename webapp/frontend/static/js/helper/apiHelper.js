const fetchJsonData = async(api) =>{
    const response = await fetch(api);
    if (!response.ok) {
        return {};
        }
    return await response.json()
    }


export {fetchJsonData}