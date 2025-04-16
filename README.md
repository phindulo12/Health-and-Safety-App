# Incident Logger App (Tkinter Based)

A simple desktop-based Incident Management System using Python's `tkinter` GUI library and JSON for data storage.

## 🔍 Overview

This app provides two user roles:

- **Worker**: Can register, log incidents, and view personal incident history.
- **Supervisor**: Can view all incidents, respond, and mark them as resolved.

## 🚀 Features

- Worker registration and login
- Supervisor login (default: `admin/admin`)
- Incident logging with type and description
- Incident resolution with response and status tracking
- View resolved/open incidents
- Safety tips display

## 📁 Directory Structure

```
data/
├── incidents.json
├── messages.json
├── supervisors.json
└── workers.json
```

These files are created automatically in the `data/` folder on first run.

## 🧰 Requirements

- Python 3.x

## ▶️ How to Run

1. Make sure Python is installed.
2. Run the script:
    ```bash
    python your_script_name.py
    ```
3. A GUI window will appear for interaction.

## 🛡️ Safety Tips Example

- Always wear protective gear
- Keep work area clean
- Report unsafe conditions immediately

## 🧪 Default Credentials

- **Supervisor Username**: `admin`
- **Password**: `admin`

## 📌 Notes

- Data is stored in local JSON files.
- The app uses `tkinter` dialogs for all input and output.

---

Made with ❤️ for workplace safety.
