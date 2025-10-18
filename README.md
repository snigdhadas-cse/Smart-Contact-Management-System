
# 📇 Smart Contact Management System

A modern, user-friendly **Contact Management Application** built using **Python**, **Tkinter (ttkbootstrap)**, and **SQLite**.
This system allows multiple users to **sign up, log in**, and securely manage their own personalized contact lists — all through an elegant GUI interface.

---

## 🚀 Features

### 👤 User Authentication

* Secure **Login** and **Signup** functionality.
* Each user has a **unique account** and access to their own contacts only.
* Password confirmation on signup to avoid errors.

### 📒 Contact Management

* Add, view, search, update, and delete contacts.
* Store details like **name, phone, email, and address**.
* Search contacts by **name** or **phone number**.
* Export contacts as **CSV files** for backup or sharing.

### 💾 Persistent Storage

* All data is stored locally using **SQLite**.
* Separate tables for users and their contacts.
* Automatically creates database and tables on first run.

### 🎨 Modern User Interface

* Built with **ttkbootstrap**, giving the app a sleek, responsive design.
* Organized layout with labels, input fields, and a table view for contacts.
* Buttons styled for clarity and user convenience.

---

## 🧰 Technologies Used

| Component    | Technology                    |
| ------------ | ----------------------------- |
| Frontend GUI | `Tkinter` with `ttkbootstrap` |
| Database     | `SQLite3`                     |
| Language     | `Python 3.x`                  |
| File Export  | `CSV` module                  |


---

## 🗂️ Project Structure

```
📦 smart-contact-manager/
 ┣ 📜 contact_manager.py      # Main application file
 ┣ 📜 contacts.db             # Auto-generated SQLite database
 ┣ 📜 README.md               # Project documentation
 ┗ 📂 assets/                 # (Optional) Future icons or images
```

---

## 📦 Database Schema

### Table: `users`

| Field    | Type         | Description     |
| -------- | ------------ | --------------- |
| id       | INTEGER (PK) | User ID         |
| username | TEXT         | Unique username |
| password | TEXT         | User password   |

### Table: `contacts`

| Field   | Type         | Description    |
| ------- | ------------ | -------------- |
| id      | INTEGER (PK) | Contact ID     |
| user_id | INTEGER (FK) | Linked user ID |
| name    | TEXT         | Contact name   |
| phone   | TEXT         | Phone number   |
| email   | TEXT         | Email address  |
| address | TEXT         | Address        |

---

## 💡 Future Enhancements

* 🔒 Password encryption using **hashlib/bcrypt**
* 🎂 Birthday reminders and notifications
* ☁️ Cloud synchronization (Firebase or Google Drive)
* 🖼️ Profile picture support for each contact
* 🌙 Light/Dark mode toggle

---

## 🧑‍💻 Author

**Snigdha Das**
💼 GitHub: [snigdhadas-cse](https://github.com/snigdhadas-cse)
🔗 LinkedIn: [Snigdha Das](https://www.linkedin.com/in/snigdhadas-cse/)

---

## 🪪 License

This project is open-source and available under the **MIT License**.
Feel free to use, modify, and distribute with proper attribution.

---
