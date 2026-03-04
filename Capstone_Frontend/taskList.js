import axios from "axios";
const API_LINK = "https://corsproxy.io/?https://api.restful-api.dev/objects";
let currentUser = null;
let selectedTaskId = null;
let currentFilter = "all";
window.addEventListener("DOMContentLoaded", async () => {
    const userData = localStorage.getItem("userData");
    if (!userData) {
        window.location.href = "loginPage.html";
        return;
    }
    
    currentUser = JSON.parse(userData); 

    document.querySelector(".add-btn").addEventListener("click", handleAddTask);
    document.querySelector(".add-task-input").addEventListener("keydown", (e) => {
        if (e.key === "Enter") handleAddTask();
    });
    document.querySelector(".btn-save").addEventListener("click", handleSaveEdit);
    document.querySelector(".btn-discard").addEventListener("click", handleDiscardEdit);
    document.querySelector(".logout").addEventListener("click", (e) => {
        e.preventDefault();
        localStorage.removeItem("userData");
        window.location.href = "loginPage.html";
    });
    document.querySelectorAll(".filter-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            currentFilter = btn.dataset.filter;
            document.querySelectorAll(".filter-btn").forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            renderTasks();
        });
    });
    await syncUserFromAPI();
});
async function syncUserFromAPI() {
    try {
        const response = await axios.get(`${API_LINK}/${currentUser.id}`);
        const apiUser = response.data;

        if (!apiUser.data) apiUser.data = {};
        if (!apiUser.data.tasks) apiUser.data.tasks = [];

        
        if (apiUser.data.tasks.length > 0) {
            currentUser = apiUser;
            localStorage.setItem("userData", JSON.stringify(currentUser));
        } else if (currentUser.data?.tasks?.length > 0) {           
            console.warn("API has no tasks, restoring from localStorage...");
            await saveUserToAPI();
        } else {            
            currentUser = apiUser;
            localStorage.setItem("userData", JSON.stringify(currentUser));
        }

        renderTasks();
    } catch (error) {
        console.error("Failed to sync user data from API:", error);
        // API failed entirely — just use whatever is in localStorage
        if (!currentUser.data) currentUser.data = {};
        if (!currentUser.data.tasks) currentUser.data.tasks = [];
        renderTasks();
    }
}

async function saveUserToAPI() {
    const response = await axios.put(`${API_LINK}/${currentUser.id}`, {
        name: currentUser.name,
        data: currentUser.data
    });
    currentUser = response.data;
    if (!currentUser.data.tasks) currentUser.data.tasks = [];
    localStorage.setItem("userData", JSON.stringify(currentUser));
}
async function handleAddTask() {
    const input = document.querySelector(".add-task-input");
    const name = input.value.trim();
    if (!name) return;
    const newTask = {
        id: Date.now(),
        name: name,
        description: "",
        completed: false
    };
    currentUser.data.tasks.push(newTask);
    try {
        await saveUserToAPI();
        input.value = "";
        renderTasks();
    } catch (error) {
        currentUser.data.tasks.pop();
        alert("Failed to add task. Please try again.");
        console.error("Error adding task:", error);
    }

}
function openEditPanel(taskId) {
    const task = currentUser.data.tasks.find(t => t.id === taskId);
    if (!task) return;
    selectedTaskId = taskId;
    document.getElementById("edit-name").value = task.name || "";
    document.getElementById("edit-desc").value = task.description || "";
    document.body.classList.add("details-open");
    document.querySelectorAll(".task-item").forEach(el => el.classList.remove("active-task"));
    const activeItem = document.querySelector(`.task-item[data-id="${taskId}"]`);
    if (activeItem) activeItem.classList.add("active-task");
}

async function handleSaveEdit() {
    if (!selectedTaskId) return;
    const taskIndex = currentUser.data.tasks.findIndex(t => t.id === selectedTaskId);
    if (taskIndex === -1) return;
    const newName = document.getElementById("edit-name").value.trim();
    const newDesc = document.getElementById("edit-desc").value.trim();
    if (!newName) {
        alert("Task name cannot be empty.");
        return;
    }
    const oldTask = { ...currentUser.data.tasks[taskIndex] };
    currentUser.data.tasks[taskIndex] = {
        ...currentUser.data.tasks[taskIndex],
        name: newName,
        description: newDesc
    };
    try {
        await saveUserToAPI();
        closeEditPanel();
        renderTasks();
    } catch (error) {
        currentUser.data.tasks[taskIndex] = oldTask;
        alert("Failed to save changes. Please try again.");
        console.error("Error saving task:", error);
    }
}
function handleDiscardEdit() {
    closeEditPanel();
}
function closeEditPanel() {
    selectedTaskId = null;
    document.body.classList.remove("details-open");
    document.querySelectorAll(".task-item").forEach(el => el.classList.remove("active-task"));
}
async function handleToggleComplete(taskId) {
    const taskIndex = currentUser.data.tasks.findIndex(t => t.id === taskId);
    if (taskIndex === -1) return;
    const oldCompleted = currentUser.data.tasks[taskIndex].completed;
    currentUser.data.tasks[taskIndex].completed = !oldCompleted;
    try {
        await saveUserToAPI();
        renderTasks();
    } catch (error) {
        currentUser.data.tasks[taskIndex].completed = oldCompleted;
        alert("Failed to update task. Please try again.");
        console.error("Error updating task:", error);
    }

    
}
async function handleDeleteTask(taskId){
    if (!confirm("Are you sure you want to delete this task?")) return;
    const oldTasks = [...currentUser.data.tasks];
    currentUser.data.tasks = currentUser.data.tasks.filter(t => t.id !== taskId);
    try {
        await saveUserToAPI();
        if (selectedTaskId === taskId) closeEditPanel();
        renderTasks();
    } catch (error) {
        currentUser.data.tasks = oldTasks;
        alert("Failed to delete task. Please try again.");
        console.error("Error deleting task:", error);
    }
}
function renderTasks() {
    const taskList = document.querySelector(".task-list");
    const countEl = document.querySelector(".count");
    const allTasks = currentUser.data.tasks;

    
    const tasks = allTasks.filter(task => {
        if (currentFilter === "completed") return task.completed;
        if (currentFilter === "pending") return !task.completed;
        return true; 
    });

    countEl.textContent = allTasks.length;
    taskList.innerHTML = "";

    if (tasks.length === 0) {
        taskList.innerHTML = `<p style="color: var(--text-light); text-align:center; margin-top:20px;">No ${currentFilter === "all" ? "" : currentFilter} tasks found.</p>`;
        return;
    }

    tasks.forEach(task => {
        const item = document.createElement("div");
        item.classList.add("task-item");
        item.dataset.id = task.id;
        if (task.id === selectedTaskId) item.classList.add("active-task");

        item.innerHTML = `
            <div class="task-left">
                <input type="checkbox" class="custom-checkbox" ${task.completed ? "checked" : ""}>
                <span class="task-name" style="${task.completed ? 'text-decoration: line-through; color: var(--text-light);' : ''}">
                    ${task.name}
                </span>
            </div>
            <div style="display:flex; align-items:center; gap:8px;">
                <button class="arrow-btn edit-btn" title="Edit">›</button>
                <button class="arrow-btn delete-btn" title="Delete" style="color:#e74c3c;">✕</button>
            </div>
        `;

        item.querySelector(".custom-checkbox").addEventListener("change", (e) => {
            // Prevent checkbox click from triggering edit panel
            e.stopPropagation();
            handleToggleComplete(task.id);
        });

        item.querySelector(".edit-btn").addEventListener("click", (e) => {            
            e.stopPropagation();
            openEditPanel(task.id);
        });

        item.querySelector(".delete-btn").addEventListener("click", (e) => {
            // Prevent delete button click from triggering another edit panel
            e.stopPropagation();
            handleDeleteTask(task.id);
        });

        item.addEventListener("click", () => openEditPanel(task.id));

        taskList.appendChild(item);
    });
}