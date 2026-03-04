window.addEventListener("DOMContentLoaded", () => {
    const userData = localStorage.getItem("userData");
    if (!userData) {
        window.location.href = "loginPage.html";
        return;
    }
    displayUserProfile(JSON.parse(userData));
});

function displayUserProfile(userData) {
        const profileContent = document.getElementById("profileContent");
        profileContent.innerHTML = `
        <h2>Welcome, ${userData.name}!</h2>
        <p><strong>Email:</strong> ${userData.data.email}</p>
        <p><strong>Address:</strong> ${userData.data.address}</p>
        <p><strong>User ID:</strong> ${userData.id}</p>         
        
        `;

}
document.getElementById("changePasswordBtn").addEventListener("click", () => {
    window.location.href = "changePassword.html";
});

document.getElementById("logoutBtn").addEventListener("click", () => {
    localStorage.removeItem("userData");
    window.location.href = "loginPage.html";
});

    