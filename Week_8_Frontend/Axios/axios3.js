import axios from "axios";
async function getObject(id){
    try {
        const response = await axios.get(`https://api.restful-api.dev/objects?id=${id}`);
        const data = response.data;
        console.log(data);
    } catch (error) {
        if (error.response && error.response.status === 404) {
            throw new Error(`Object with id ${id} not found`);
        }
        throw new Error(`HTTP error! status: ${error.response?.status || 'unknown'}`);
    }
}
getObject('ff8081819782e69e019c40ed1ba82bae')