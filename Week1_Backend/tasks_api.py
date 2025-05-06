from flask import Flask, request, jsonify
import json
import os
app = Flask(__name__)


# Allowed status values
ALLOWED_STATUS = {"to_do", "in_progress", "done"}
# Code to return the list of tasks and filter them based on status if the query parameter is provided
@app.route("/Tasks_List", methods=["GET"])
def return_tasks():
    filtered_tasks = Todo_list
    status = request.args.get("status")
    if status:
        filtered_tasks = list(
            filter(lambda task: task["status"].lower() == status.lower(), filtered_tasks)
        )
    return jsonify({"tasks": filtered_tasks}), 200

# Function to add a new task to the Todo_list. It ensures the task doesnt have a duplicate identifier and that the status is one of the allowed values.
# It also checks if the task is in the correct format and returns an error message if not.
# Also verifies all required fields are present in the request.
#Then, it appends the new task to the Todo_list and saves it to the JSON file.
@app.route("/Add_Task", methods=["POST"])
def add_task():
    new_task = request.get_json(silent=True)
    if not isinstance(new_task, dict):
        return jsonify(error = "Invalid task format, please send JSON object"), 400
    identifier = new_task.get("identifier")
    title = new_task.get("title")
    description = new_task.get("description")
    status = new_task.get("status")
    
    if not identifier or not title or not description or not status:
        return jsonify(error = "Missing required fields"), 400
    
    if any(task["identifier"] == identifier for task in Todo_list):
        return jsonify(error = "Task with this identifier already exists"), 400
    
    if status not in ALLOWED_STATUS:
        return jsonify(error="Invalid status value, allowed values are: to_do, in_progress and done."), 400
    
    Todo_list.append({
                      
        "identifier": identifier,
        "title": title,
        "description": description,
        "status": status
    })
    with open("Todo_list.json", "w") as file:
        json.dump(Todo_list, file, indent=4)
    return (jsonify(message="Task added successfully", tasks=Todo_list), 201)

# Function to delete a task from the list. It checks if the  identifier is provided and if it exists in the list.
# If the task is found, it removes it from the list and saves the updated list to the JSON file.
# If the task is not found, it returns an error message.
@app.route("/Delete_Task", methods=["POST"])
def delete_task():
    task_identifier = request.get_json(silent=True)
    if not isinstance(task_identifier, dict):
        return jsonify({"error": "Invalid task format, please send JSON object"}), 400
    identifier = task_identifier.get("identifier")
    if not identifier:
        return jsonify(error =  "Missing required fields"), 400
    for task in Todo_list:
        if task["identifier"] == identifier:
            Todo_list.remove(task)
            with open("Todo_list.json", "w") as file:
                json.dump(Todo_list, file, indent=4)
            return jsonify(message="Task deleted successfully", tasks=Todo_list), 200
           
    return jsonify(error="Task not found"), 404

# Update function to modify an existing task in the Todo_list. It checks if the identifier is provided and if it exists in the list.
# If the task is found, it updates the task with the new values provided in the request.
# Not all fields neeed to be provided, only the ones that need to be updated.
@app.route("/Update_Task", methods=["POST"])
def update_task():
    task_data = request.get_json(silent=True)
    if not isinstance(task_data, dict):
        return jsonify(error="Invalid task format, please send JSON object"), 400
    identifier = task_data.get("identifier")
    if not identifier:
        return jsonify(error="Missing required fields"), 400
    for task in Todo_list:
        if task["identifier"] == identifier:
            title = task_data.get("title")
            description = task_data.get("description")
            status = task_data.get("status")
            
            if title:
                task["title"] = title
            if description:
                task["description"] = description
            if status:
                if status not in ALLOWED_STATUS:
                    return jsonify(error="Invalid status value, allowed values are: to_do, in_progress and done."), 400
                task["status"] = status
            with open("Todo_list.json", "w") as file:
                json.dump(Todo_list, file, indent=4)
            return jsonify(message="Task updated successfully", tasks=Todo_list), 200

# Main function to run the Flask application. It checks if the Todo_list.json file exists and loads the tasks from it.
# If the file does not exist, it initializes an empty Todo_list and starts the application.
if __name__ == "__main__":
    if os.path.exists("Todo_list.json"):
        with open("Todo_list.json", "r") as file:
            Todo_list = json.load(file)
        app.run(host="localhost", port=5000, debug=True)
    else:
         Todo_list = []
         app.run(host="localhost", port=5000, debug=True)
    
    