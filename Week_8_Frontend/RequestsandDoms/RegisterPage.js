import axios from "axios";
window.addEventListener("DOMContentLoaded", () => {
    const userData = localStorage.getItem("userData");
    if (userData) {
        window.location.href = "myProfile.html";
    }
});

document.getElementById("registerForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const address = document.getElementById("address").value;
    try {
        const response = await registerUser(name, email, password, address);
        localStorage.setItem("userData", JSON.stringify(response));
        alert(`User created successfully! Your user ID is: ${response.id}`);
        window.location.href = "myProfile.html";
    } catch (error) {
        alert(`Error: ${error.message}`);
        console.error('Registration failed:', error);
    }
});

async function registerUser(name, email, password, address) {
    const data = {
        name: name,
        data: {
            email: email,
            password: password,
            address: address
        }
    };
    const response = await axios.post("https://corsproxy.io/?https://api.restful-api.dev/objects", data);
    
    const result = response.data;
    console.log(result);
    return result;
}