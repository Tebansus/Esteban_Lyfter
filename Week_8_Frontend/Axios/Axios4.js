import axios from "axios";

async function updateUserAdress(userId, newAddress) {
    const response = await axios.patch(`https://api.restful-api.dev/objects/${userId}`, {
        data: {
            address: newAddress
        }
    });
    console.log(response.data);
}
updateUserAdress('ff8081819782e69e019c40ed1ba82bae', 'Hatillo 13')