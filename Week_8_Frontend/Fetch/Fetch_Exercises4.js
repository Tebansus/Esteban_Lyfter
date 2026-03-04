async function updateUserAdress(userId, newAddress) {
    const request = await fetch(`https://api.restful-api.dev/objects/${userId}`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            data: {
                address: newAddress
            }
        })
    });
    const response = await request.json();
    console.log(response);
}
updateUserAdress('ff8081819782e69e019c3182794e0683', 'Hatillo 13')