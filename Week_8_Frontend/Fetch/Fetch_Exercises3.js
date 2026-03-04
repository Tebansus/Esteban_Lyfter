async function getObject(id){
    const response = await fetch(`https://api.restful-api.dev/objects?id=${id}`);
    if (!response.ok) {
        if (response.status === 404) {
            throw new Error(`Object with id ${id} not found`);
        } 
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    console.log(data);
    
}
getObject('ff8081819782e69e019c3182794e0683')