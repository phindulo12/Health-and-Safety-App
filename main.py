import os
import json
import tkinter as tk
from tkinter import messagebox, simpledialog

# Data directory
DATA_DIR = "data"
INCIDENTS_FILE = os.path.join(DATA_DIR, "incidents.json")
MESSAGES_FILE = os.path.join(DATA_DIR, "messages.json")
SUPERVISORS_FILE = os.path.join(DATA_DIR, "supervisors.json")
WORKERS_FILE = os.path.join(DATA_DIR, "workers.json")


# Function to ensure data directory exists
def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


# Function to load data from a file
def load_data(filename):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return json.load(file)
    return []


# Function to save data to a file
def save_data(data, filename):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


# Function to register a new worker
def register_worker():
    name = simpledialog.askstring("Registration", "Enter your name:")
    if not name:
        return None

    age = simpledialog.askinteger("Registration", "Enter your age:")
    if not age:
        return None

    gender = simpledialog.askstring("Registration", "Enter your gender (M/F/O):")
    if not gender:
        return None

    worker = {
        "name": name,
        "age": age,
        "gender": gender.upper()
    }

    workers = load_data(WORKERS_FILE)
    workers.append(worker)
    save_data(workers, WORKERS_FILE)

    messagebox.showinfo("Success", "Worker registered successfully!")
    return worker


# Function to log in as worker
def worker_login():
    name = simpledialog.askstring("Worker Login", "Enter your name:")
    if not name:
        return None

    workers = load_data(WORKERS_FILE)
    for worker in workers:
        if worker["name"].lower() == name.lower():
            messagebox.showinfo("Success", f"Welcome back, {name}!")
            return worker

    messagebox.showwarning("Error", "Worker not found. Please register first.")
    return None


# Function to log in as supervisor
def supervisor_login():
    username = simpledialog.askstring("Supervisor Login", "Enter your username:")
    if not username:
        return None

    password = simpledialog.askstring("Supervisor Login", "Enter your password:", show="*")
    if not password:
        return None

    supervisors = load_data(SUPERVISORS_FILE)
    for supervisor in supervisors:
        if supervisor["username"].lower() == username.lower() and supervisor["password"] == password:
            messagebox.showinfo("Success", f"Welcome back, {username}!")
            return supervisor

    messagebox.showwarning("Error", "Invalid username or password.")
    return None


# Function to log an incident
def log_incident(worker):
    incident_type = simpledialog.askstring("Log Incident", "Enter incident type:")
    if not incident_type:
        return

    description = simpledialog.askstring("Log Incident", "Enter incident description:")
    if not description:
        return

    incident = {
        "user": worker["name"],
        "incident_type": incident_type,
        "description": description,
        "status": "open",  # New field for status tracking
        "resolution": ""  # New field for resolution details
    }

    incidents = load_data(INCIDENTS_FILE)
    incidents.append(incident)
    save_data(incidents, INCIDENTS_FILE)

    messagebox.showinfo("Success", "Incident logged successfully!")


# Function to view worker's incidents
def view_worker_incidents(worker):
    incidents = load_data(INCIDENTS_FILE)
    worker_incidents = [inc for inc in incidents if inc["user"].lower() == worker["name"].lower()]

    if not worker_incidents:
        messagebox.showinfo("Info", "No incidents logged for you.")
        return

    incidents_str = "\n".join(
        [f"{i + 1}. {inc['incident_type']}: {inc['description']} [Status: {inc.get('status', 'open')}]"
         for i, inc in enumerate(worker_incidents)])
    messagebox.showinfo("Your Incidents", incidents_str)


# Function to view all incidents (for supervisor)
def view_all_incidents():
    incidents = load_data(INCIDENTS_FILE)
    if not incidents:
        messagebox.showinfo("Info", "No incidents reported yet.")
        return

    incidents_str = "\n".join(
        [f"{i + 1}. {inc['user']} - {inc['incident_type']}: {inc['description']} [Status: {inc.get('status', 'open')}]"
         for i, inc in enumerate(incidents)])
    messagebox.showinfo("All Incidents", incidents_str)


# Function to view resolved incidents
def view_resolved_incidents():
    incidents = load_data(INCIDENTS_FILE)
    resolved_incidents = [inc for inc in incidents if inc.get('status') == 'resolved']

    if not resolved_incidents:
        messagebox.showinfo("Info", "No resolved incidents found.")
        return

    incidents_str = "\n".join([
                                  f"{i + 1}. {inc['user']} - {inc['incident_type']}: {inc['description']}\n   Resolution: {inc.get('resolution', 'No details')}"
                                  for i, inc in enumerate(resolved_incidents)])
    messagebox.showinfo("Resolved Incidents", incidents_str)


# Function to respond to incident (for supervisor)
def respond_to_incident(supervisor):
    incidents = load_data(INCIDENTS_FILE)
    open_incidents = [inc for inc in incidents if inc.get('status', 'open') == 'open']

    if not open_incidents:
        messagebox.showinfo("Info", "No open incidents to respond to.")
        return

    # Show only open incidents for selection
    incidents_str = "\n".join([f"{i + 1}. {inc['user']} - {inc['incident_type']}: {inc['description']}"
                               for i, inc in enumerate(open_incidents)])

    incident_num = simpledialog.askinteger(
        "Respond to Incident",
        f"Open Incidents:\n{incidents_str}\n\nEnter incident number to respond to (1-{len(open_incidents)}):",
        minvalue=1,
        maxvalue=len(open_incidents)
    )

    if not incident_num:
        return

    action = simpledialog.askinteger(
        "Incident Action",
        "1. Add response\n2. Mark as resolved\n3. Cancel",
        minvalue=1,
        maxvalue=3
    )

    if action == 1:  # Add response
        response = simpledialog.askstring("Respond", "Enter your response:")
        if not response:
            return

        # Find the original incident in the full list
        original_index = incidents.index(open_incidents[incident_num - 1])
        incidents[original_index]['response'] = response

        messages = load_data(MESSAGES_FILE)
        messages.append({
            "supervisor": supervisor["username"],
            "incident_number": original_index + 1,
            "response": response,
            "action": "responded"
        })
        save_data(messages, MESSAGES_FILE)

        messagebox.showinfo("Success", "Response added successfully!")

    elif action == 2:  # Mark as resolved
        resolution = simpledialog.askstring("Resolution", "Enter resolution details:")
        if not resolution:
            return

        # Find the original incident in the full list
        original_index = incidents.index(open_incidents[incident_num - 1])
        incidents[original_index]['status'] = 'resolved'
        incidents[original_index]['resolution'] = resolution
        incidents[original_index]['resolved_by'] = supervisor["username"]

        messages = load_data(MESSAGES_FILE)
        messages.append({
            "supervisor": supervisor["username"],
            "incident_number": original_index + 1,
            "resolution": resolution,
            "action": "resolved"
        })
        save_data(messages, MESSAGES_FILE)

        messagebox.showinfo("Success", "Incident marked as resolved!")

    save_data(incidents, INCIDENTS_FILE)


# Function to display safety tips
def show_safety_tips():
    tips = [
        "1. Always wear protective gear when required",
        "2. Keep your work area clean and organized",
        "3. Report unsafe conditions immediately",
        "4. Take regular breaks to avoid fatigue",
        "5. Know the emergency procedures for your area"
    ]
    messagebox.showinfo("Safety Tips", "\n".join(tips))


# Main menu for workers
def worker_menu(worker):
    while True:
        choice = simpledialog.askinteger(
            "Worker Menu",
            "1. Log incident\n2. View my incidents\n3. Safety tips\n4. Logout",
            minvalue=1, maxvalue=4
        )

        if choice == 1:
            log_incident(worker)
        elif choice == 2:
            view_worker_incidents(worker)
        elif choice == 3:
            show_safety_tips()
        elif choice == 4:
            break


# Main menu for supervisors
def supervisor_menu(supervisor):
    while True:
        choice = simpledialog.askinteger(
            "Supervisor Menu",
            "1. View all incidents\n2. View open incidents\n3. View resolved incidents\n4. Respond to incident\n5. Safety tips\n6. Logout",
            minvalue=1, maxvalue=6
        )

        if choice == 1:
            view_all_incidents()
        elif choice == 2:
            view_open_incidents()
        elif choice == 3:
            view_resolved_incidents()
        elif choice == 4:
            respond_to_incident(supervisor)
        elif choice == 5:
            show_safety_tips()
        elif choice == 6:
            break


# New function to view open incidents
def view_open_incidents():
    incidents = load_data(INCIDENTS_FILE)
    open_incidents = [inc for inc in incidents if inc.get('status', 'open') == 'open']

    if not open_incidents:
        messagebox.showinfo("Info", "No open incidents found.")
        return

    incidents_str = "\n".join([f"{i + 1}. {inc['user']} - {inc['incident_type']}: {inc['description']}"
                               for i, inc in enumerate(open_incidents)])
    messagebox.showinfo("Open Incidents", incidents_str)


# Main application function
def main():
    ensure_data_dir()

    # Create default supervisor if none exists
    if not os.path.exists(SUPERVISORS_FILE):
        save_data([{"username": "admin", "password": "admin"}], SUPERVISORS_FILE)

    while True:
        choice = simpledialog.askinteger(
            "Main Menu",
            "1. Login as Worker\n2. Login as Supervisor\n3. Register as Worker\n4. Exit",
            minvalue=1, maxvalue=4
        )

        if choice == 1:
            worker = worker_login()
            if worker:
                worker_menu(worker)
        elif choice == 2:
            supervisor = supervisor_login()
            if supervisor:
                supervisor_menu(supervisor)
        elif choice == 3:
            register_worker()
        elif choice == 4:
            break


if __name__ == "__main__":
    main()



