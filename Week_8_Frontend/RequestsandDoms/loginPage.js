import axios from "axios";

window.addEventListener("DOMContentLoaded", () => {
    const userData = localStorage.getItem("userData");
    if (userData) {
        window.location.href = "myProfile.html";
    }
});

document.getElementById("loginForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const userId = document.getElementById("userId").value;
    const password = document.getElementById("password").value;
    try {
        const response = await loginUser(userId, password);
        localStorage.setItem("userData", JSON.stringify(response));
        window.location.href = "myProfile.html";
    } catch (error) {
        if (error.response && error.response.status === 404) {
            alert("User not found. Please register first.");
        } else if (error.message.includes("password")) {
            alert("Incorrect password. Please try again.");
        } else {
            alert('login failed');
        }
        console.error('Login failed:', error);
    }
});

async function  loginUser(userId, password) {
    const response = await axios.get(`https://corsproxy.io/?https://api.restful-api.dev/objects/${userId}`);
    const userData = response.data;
    if (userData.data && userData.data.password === password) {
        return userData;
    } else {
        throw new Error("Incorrect password");
    }
    
}