import axios from "axios";

async function postToApi(name, email, password, address) {
    const data = {
        name: name,
        data: {
            email: email,
            password: password,
            address: address
        }
    };
    const response = await axios.post("https://api.restful-api.dev/objects", data);
    
    const result = response.data;
    console.log(result);
}
postToApi("John Doe", "john.doe@example.com", "password123", "Fuente Hispanidad");