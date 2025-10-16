
# 📇 Contact Management System (Python + Tkinter + SQLite)

## 🧩 Overview

The **Contact Management System** is a simple yet functional desktop application built using **Python, Tkinter**, and **SQLite**.
It allows users to store, view, search, update, and delete contact information through an intuitive graphical interface.
The data is stored **permanently** in a local SQLite database (`contacts.db`), making it a lightweight and efficient solution for managing contact lists.

---

## 🚀 Features

### 🧠 Core Functionalities

* ➕ **Add New Contact** — Add contact details including name, phone, email, and address.
* 📋 **View All Contacts** — Display all saved contacts in a scrollable table.
* 🔍 **Search Contact** — Quickly find contacts by name or phone number.
* ✏️ **Update Contact** — Edit and update existing contact details.
* ❌ **Delete Contact** — Remove unwanted contacts from the database.
* 💾 **Persistent Storage** — Uses SQLite for permanent data saving.

### 🎨 User Interface

* Designed with **Tkinter**, Python’s built-in GUI toolkit.
* Clean and minimal interface for easy navigation.
* Organized layout with input fields, buttons, and a contact list table.
* Responsive buttons with color-coded actions.

---

## 🏗️ Technologies Used

| Component            | Technology |
| -------------------- | ---------- |
| **Frontend (GUI)**   | Tkinter    |
| **Backend Database** | SQLite3    |
| **Language**         | Python 3.x |

---


## 🗃️ Database Information

* The SQLite database file `contacts.db` is automatically created when you first run the app.
* Each record contains:

  * **ID** (Auto Increment)
  * **Name**
  * **Phone** (Unique)
  * **Email**
  * **Address**

---

## 📂 Project Structure

```
Contact-Management-System/
│
├── contact_manager.py      # Main Python code
├── contacts.db             # Auto-created SQLite database
├── README.md               # Project documentation
└── requirements.txt        # (Optional) List of dependencies
```

---

## 💡 Future Enhancements

* 🌈 Modern UI using **CustomTkinter** or **ttkbootstrap**
* 🧾 CSV/Excel import & export support
* 🧑‍💼 Contact profile photo support
* 🔐 Login system for multiple users
* ☁️ Cloud backup using Firebase or Google Sheets
* 🔔 Birthday reminders and category tagging

---

---

## 👩‍💻 Author

**Snigdha Das**
📚 B.Tech CSE Student, Narula Institute of Technology
💬 Passionate about Python and Java Development
🌐 [snigdhadas-cse](https://github.com//snigdhadas-cse)

---

## 🪪 License

This project is licensed under the **MIT License** — feel free to use and modify it for learning or development purposes.

---
