async function postToApi(name, email, password, address) {
    const data = {
        name: name,
        data: {
            email: email,
            password: password,
            address: address
        }
    };
    const response = await fetch("https://api.restful-api.dev/objects", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });
    const result = await response.json();
    console.log(result);
}
postToApi("John Doe", "john.doe@example.com", "password123", "Fuente Hispanidad");