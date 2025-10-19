import customtkinter as ctk
from tkinter import ttk, filedialog, messagebox
import sqlite3
import bcrypt
import csv
import os
from PIL import Image, ImageTk

# -------------------- DATABASE SETUP --------------------
def init_db():
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password BLOB NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL UNIQUE,
            email TEXT,
            address TEXT,
            photo TEXT
        )
    """)
    conn.commit()
    conn.close()

def run_query(query, parameters=()):
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    cursor.execute(query, parameters)
    conn.commit()
    conn.close()

# -------------------- LOGIN / SIGNUP SYSTEM --------------------
def signup():
    username = entry_username.get().strip()
    password = entry_password.get().strip().encode('utf-8')

    if not username or not password:
        messagebox.showwarning("Input Error", "Username and password required!")
        return

    hashed = bcrypt.hashpw(password, bcrypt.gensalt())

    try:
        run_query("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
        messagebox.showinfo("Success", "Account created successfully! Please log in.")
        entry_username.delete(0, 'end')
        entry_password.delete(0, 'end')
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists!")

def login():
    username = entry_username.get().strip()
    password = entry_password.get().strip().encode('utf-8')

    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    result = cursor.fetchone()
    conn.close()

    if result:
        stored_password = result[0]
        # ✅ Ensure the stored password is bytes
        if isinstance(stored_password, str):
            stored_password = stored_password.encode('utf-8')

        if bcrypt.checkpw(password, stored_password):
            login_window.destroy()
            main_app()
            return

    messagebox.showerror("Login Failed", "Invalid username or password.")

# -------------------- CONTACT MANAGEMENT --------------------
def add_contact():
    name = entry_name.get().strip()
    phone = entry_phone.get().strip()
    email = entry_email.get().strip()
    address = entry_address.get().strip()
    photo = photo_path.get()

    if not name or not phone:
        messagebox.showwarning("Input Error", "Name and phone are required!")
        return

    try:
        run_query("INSERT INTO contacts (name, phone, email, address, photo) VALUES (?, ?, ?, ?, ?)",
                  (name, phone, email, address, photo))
        messagebox.showinfo("Success", "Contact added successfully!")
        clear_fields()
        view_contacts()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Phone number already exists!")

def view_contacts():
    for row in contact_tree.get_children():
        contact_tree.delete(row)
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts")
    for row in cursor.fetchall():
        contact_tree.insert("", "end", values=row)
    conn.close()

def search_contact():
    term = entry_search.get().lower()
    for row in contact_tree.get_children():
        contact_tree.delete(row)
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts WHERE LOWER(name) LIKE ? OR phone LIKE ?",
                   ('%' + term + '%', '%' + term + '%'))
    for row in cursor.fetchall():
        contact_tree.insert("", "end", values=row)
    conn.close()

def delete_contact():
    selected = contact_tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Select a contact to delete!")
        return
    contact_id = contact_tree.item(selected)["values"][0]
    run_query("DELETE FROM contacts WHERE id=?", (contact_id,))
    messagebox.showinfo("Success", "Contact deleted successfully!")
    view_contacts()

def update_contact():
    selected = contact_tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Select a contact to update!")
        return
    contact_id = contact_tree.item(selected)["values"][0]
    name = entry_name.get().strip()
    phone = entry_phone.get().strip()
    email = entry_email.get().strip()
    address = entry_address.get().strip()
    photo = photo_path.get()

    run_query("UPDATE contacts SET name=?, phone=?, email=?, address=?, photo=? WHERE id=?",
              (name, phone, email, address, photo, contact_id))
    messagebox.showinfo("Success", "Contact updated successfully!")
    clear_fields()
    view_contacts()

def clear_fields():
    entry_name.delete(0, 'end')
    entry_phone.delete(0, 'end')
    entry_email.delete(0, 'end')
    entry_address.delete(0, 'end')
    photo_path.set("")

# -------------------- PHOTO UPLOAD --------------------
def upload_photo():
    path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
    if path:
        photo_path.set(path)
        img = Image.open(path).resize((80, 80))
        img_tk = ImageTk.PhotoImage(img)
        lbl_photo.configure(image=img_tk)
        lbl_photo.image = img_tk

# -------------------- CSV IMPORT / EXPORT --------------------
def export_contacts():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                             filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, phone, email, address FROM contacts")
    rows = cursor.fetchall()
    conn.close()

    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Phone", "Email", "Address"])
        writer.writerows(rows)
    messagebox.showinfo("Export Complete", "Contacts exported successfully!")

def import_contacts():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return

    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                run_query("INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)",
                          (row["Name"], row["Phone"], row["Email"], row["Address"]))
            except sqlite3.IntegrityError:
                continue
    messagebox.showinfo("Import Complete", "Contacts imported successfully!")
    view_contacts()

# -------------------- MAIN APP WINDOW --------------------
def main_app():
    root = ctk.CTk()
    root.title("Smart Contact Management System")
    root.geometry("900x650")
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    title = ctk.CTkLabel(root, text="📇 Smart Contact Management System", font=("Arial Rounded MT Bold", 22))
    title.pack(pady=15)

    frame = ctk.CTkFrame(root, corner_radius=15)
    frame.pack(padx=20, pady=10, fill="x")

    global entry_name, entry_phone, entry_email, entry_address, photo_path, lbl_photo
    photo_path = ctk.StringVar()

    entry_name = ctk.CTkEntry(frame, placeholder_text="Full Name")
    entry_name.grid(row=0, column=0, padx=10, pady=8)
    entry_phone = ctk.CTkEntry(frame, placeholder_text="Phone Number")
    entry_phone.grid(row=0, column=1, padx=10, pady=8)
    entry_email = ctk.CTkEntry(frame, placeholder_text="Email")
    entry_email.grid(row=1, column=0, padx=10, pady=8)
    entry_address = ctk.CTkEntry(frame, placeholder_text="Address")
    entry_address.grid(row=1, column=1, padx=10, pady=8)

    ctk.CTkButton(frame, text="Upload Photo", command=upload_photo).grid(row=2, column=0, pady=8)
    lbl_photo = ctk.CTkLabel(frame, text="")
    lbl_photo.grid(row=2, column=1, pady=8)

    btn_frame = ctk.CTkFrame(root)
    btn_frame.pack(pady=10)
    ctk.CTkButton(btn_frame, text="Add", width=100, command=add_contact).grid(row=0, column=0, padx=6)
    ctk.CTkButton(btn_frame, text="Update", width=100, fg_color="#ffb300", command=update_contact).grid(row=0, column=1, padx=6)
    ctk.CTkButton(btn_frame, text="Delete", width=100, fg_color="#ff5252", command=delete_contact).grid(row=0, column=2, padx=6)
    ctk.CTkButton(btn_frame, text="Export CSV", width=120, fg_color="#00c853", command=export_contacts).grid(row=0, column=3, padx=6)
    ctk.CTkButton(btn_frame, text="Import CSV", width=120, fg_color="#2979ff", command=import_contacts).grid(row=0, column=4, padx=6)

    search_frame = ctk.CTkFrame(root)
    search_frame.pack(pady=10)
    global entry_search
    entry_search = ctk.CTkEntry(search_frame, placeholder_text="Search by Name or Phone", width=300)
    entry_search.grid(row=0, column=0, padx=10, pady=8)
    ctk.CTkButton(search_frame, text="Search", command=search_contact).grid(row=0, column=1, padx=10)

    tree_frame = ctk.CTkFrame(root)
    tree_frame.pack(pady=10, padx=10, fill="both", expand=True)
    global contact_tree
    columns = ("ID", "Name", "Phone", "Email", "Address", "Photo")
    contact_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=12)
    for col in columns:
        contact_tree.heading(col, text=col)
        contact_tree.column(col, width=140)
    contact_tree.pack(fill="both", expand=True)

    view_contacts()
    root.mainloop()

# -------------------- LOGIN WINDOW --------------------
init_db()
login_window = ctk.CTk()
login_window.title("Login | Smart Contact System")
login_window.geometry("400x350")
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

ctk.CTkLabel(login_window, text="🔐 Login to Continue", font=("Arial Rounded MT Bold", 20)).pack(pady=20)
entry_username = ctk.CTkEntry(login_window, placeholder_text="Username")
entry_username.pack(pady=10)
entry_password = ctk.CTkEntry(login_window, placeholder_text="Password", show="*")
entry_password.pack(pady=10)

ctk.CTkButton(login_window, text="Login", command=login).pack(pady=10)
ctk.CTkButton(login_window, text="Sign Up", fg_color="#00bfa5", command=signup).pack(pady=5)

login_window.mainloop()
