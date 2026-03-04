import axios from "axios";

document.getElementById("changePasswordForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const newPassword = document.getElementById("newPassword").value;
    const userId = document.getElementById("userId").value;
    const oldPassword = document.getElementById("oldPassword").value;
    const confirmPassword = document.getElementById("confirmPassword").value;
    const messageDiv = document.getElementById("message");
    messageDiv.textContent = "";
    if (newPassword !== confirmPassword) {
        messageDiv.textContent = "Passwords do not match";
        return;
    }
    try {
        await changePassword(userId, oldPassword, newPassword);
        messageDiv.textContent = "Password changed correctly.";
        setTimeout(() => {
            window.location.href = "myProfile.html";}, 1500);
    } catch (error) {
        messageDiv.textContent = "Error changing password: " + error.message;
    }
});
async function changePassword(userId, oldPassword, newPassword) {
    try {
        const response = await axios.get(`https://corsproxy.io/?https://api.restful-api.dev/objects/${userId}`);
        const userData = response.data;
        if (!userData.data || userData.data.password !== oldPassword) {
            throw new Error("Incorrect old password");
        }
        
        
        await axios.patch(`https://corsproxy.io/?https://api.restful-api.dev/objects/${userId}`, {
            data: {
                password: newPassword
            }
        });
        
        const storedUserData = localStorage.getItem("userData");
        if (storedUserData) {
            const parsedUserData = JSON.parse(storedUserData);
            if (parsedUserData.id === userId) {
                parsedUserData.data.password = newPassword;
                localStorage.setItem("userData", JSON.stringify(parsedUserData));
            }
        }
    } catch (error) {
        if (error.response && error.response.status === 404) {
            throw new Error("User not found");
        } else if (error.message.includes("password")) {
            throw new Error("Incorrect old password");
        } else {
            throw new Error("Error changing password");
        }
    }

    }
    
