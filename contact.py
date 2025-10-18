import sqlite3
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, filedialog
import csv

# -------------------- Database Setup --------------------
def init_db():
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()

    # User Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Contacts Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            address TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()

# -------------------- Utility --------------------
def run_query(query, params=()):
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

# -------------------- LOGIN WINDOW --------------------
def open_login_window():
    login_win = ttk.Window(themename="superhero")
    login_win.title("Login - Smart Contact Manager")
    login_win.geometry("400x350")

    ttk.Label(login_win, text="🔐 Login", font=("Segoe UI", 20, "bold")).pack(pady=20)

    frame = ttk.Frame(login_win, padding=10)
    frame.pack()

    ttk.Label(frame, text="Username:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_username = ttk.Entry(frame, width=30)
    entry_username.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entry_password = ttk.Entry(frame, width=30, show="*")
    entry_password.grid(row=1, column=1, padx=5, pady=5)

    def login():
        username = entry_username.get().strip()
        password = entry_password.get().strip()

        if not username or not password:
            messagebox.showwarning("Input Error", "All fields required!")
            return

        conn = sqlite3.connect("contacts.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            messagebox.showinfo("Welcome", f"Login successful! Welcome, {username}")
            login_win.destroy()
            open_main_window(user[0], username)
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def signup():
        login_win.destroy()
        open_signup_window()

    ttk.Button(frame, text="Login", command=login, bootstyle=SUCCESS, width=20).grid(row=2, columnspan=2, pady=10)
    ttk.Button(frame, text="Create New Account", command=signup, bootstyle=INFO, width=20).grid(row=3, columnspan=2, pady=5)

    login_win.mainloop()

# -------------------- SIGNUP WINDOW --------------------
def open_signup_window():
    signup_win = ttk.Window(themename="superhero")
    signup_win.title("Sign Up - Smart Contact Manager")
    signup_win.geometry("400x380")

    ttk.Label(signup_win, text="📝 Sign Up", font=("Segoe UI", 20, "bold")).pack(pady=20)

    frame = ttk.Frame(signup_win, padding=10)
    frame.pack()

    ttk.Label(frame, text="Username:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_username = ttk.Entry(frame, width=30)
    entry_username.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entry_password = ttk.Entry(frame, width=30, show="*")
    entry_password.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Confirm Password:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    entry_confirm = ttk.Entry(frame, width=30, show="*")
    entry_confirm.grid(row=2, column=1, padx=5, pady=5)

    def create_account():
        username = entry_username.get().strip()
        password = entry_password.get().strip()
        confirm = entry_confirm.get().strip()

        if not username or not password:
            messagebox.showwarning("Input Error", "All fields are required!")
            return
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        try:
            run_query("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            messagebox.showinfo("Success", "Account created successfully! Please login.")
            signup_win.destroy()
            open_login_window()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists!")

    ttk.Button(frame, text="Sign Up", command=create_account, bootstyle=SUCCESS, width=20).grid(row=3, columnspan=2, pady=15)
    ttk.Button(frame, text="Back to Login", command=lambda: [signup_win.destroy(), open_login_window()],
               bootstyle=INFO, width=20).grid(row=4, columnspan=2)

    signup_win.mainloop()

# -------------------- MAIN CONTACT WINDOW --------------------
def open_main_window(user_id, username):
    root = ttk.Window(themename="superhero")
    root.title(f"Smart Contact Manager - {username}")
    root.geometry("900x600")

    ttk.Label(root, text=f"📒 Welcome, {username}", font=("Segoe UI", 18, "bold")).pack(pady=10)

    # --- Functions (Specific to logged-in user) ---
    def view_contacts():
        for row in contact_tree.get_children():
            contact_tree.delete(row)
        conn = sqlite3.connect("contacts.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contacts WHERE user_id=?", (user_id,))
        for row in cursor.fetchall():
            contact_tree.insert("", "end", values=row)
        conn.close()

    def add_contact():
        name = entry_name.get().strip()
        phone = entry_phone.get().strip()
        email = entry_email.get().strip()
        address = entry_address.get().strip()
        if not name or not phone:
            messagebox.showwarning("Input Error", "Name and Phone number are required!")
            return
        try:
            run_query("INSERT INTO contacts (user_id, name, phone, email, address) VALUES (?, ?, ?, ?, ?)",
                      (user_id, name, phone, email, address))
            clear_fields()
            view_contacts()
            messagebox.showinfo("Added", "Contact added successfully!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Phone number already exists!")

    def update_contact():
        selected = contact_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a contact to update!")
            return
        contact_id = contact_tree.item(selected)["values"][0]
        name = entry_name.get()
        phone = entry_phone.get()
        email = entry_email.get()
        address = entry_address.get()
        run_query("UPDATE contacts SET name=?, phone=?, email=?, address=? WHERE id=?",
                  (name, phone, email, address, contact_id))
        view_contacts()
        clear_fields()
        messagebox.showinfo("Updated", "Contact updated successfully!")

    def delete_contact():
        selected = contact_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a contact to delete!")
            return
        contact_id = contact_tree.item(selected)["values"][0]
        run_query("DELETE FROM contacts WHERE id=?", (contact_id,))
        view_contacts()
        messagebox.showinfo("Deleted", "Contact deleted successfully!")

    def search_contact():
        search_term = entry_search.get().lower()
        for row in contact_tree.get_children():
            contact_tree.delete(row)
        conn = sqlite3.connect("contacts.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM contacts 
            WHERE user_id=? AND (LOWER(name) LIKE ? OR phone LIKE ?)
        """, (user_id, f'%{search_term}%', f'%{search_term}%'))
        for row in cursor.fetchall():
            contact_tree.insert("", "end", values=row)
        conn.close()

    def export_csv():
        file = filedialog.asksaveasfilename(defaultextension=".csv",
                                            filetypes=[("CSV files", "*.csv")])
        if not file:
            return
        conn = sqlite3.connect("contacts.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name, phone, email, address FROM contacts WHERE user_id=?", (user_id,))
        data = cursor.fetchall()
        conn.close()
        with open(file, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Phone", "Email", "Address"])
            writer.writerows(data)
        messagebox.showinfo("Exported", "Contacts exported successfully!")

    def clear_fields():
        entry_name.delete(0, 'end')
        entry_phone.delete(0, 'end')
        entry_email.delete(0, 'end')
        entry_address.delete(0, 'end')

    # --- UI Layout ---
    frame = ttk.Frame(root, padding=10)
    frame.pack(pady=5)

    ttk.Label(frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_name = ttk.Entry(frame, width=35)
    entry_name.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Phone:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entry_phone = ttk.Entry(frame, width=35)
    entry_phone.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    entry_email = ttk.Entry(frame, width=35)
    entry_email.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Address:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
    entry_address = ttk.Entry(frame, width=35)
    entry_address.grid(row=3, column=1, padx=5, pady=5)

    # Buttons
    btn_frame = ttk.Frame(root, padding=10)
    btn_frame.pack()

    ttk.Button(btn_frame, text="Add", command=add_contact, bootstyle=SUCCESS, width=15).grid(row=0, column=0, padx=5)
    ttk.Button(btn_frame, text="View All", command=view_contacts, bootstyle=INFO, width=15).grid(row=0, column=1, padx=5)
    ttk.Button(btn_frame, text="Update", command=update_contact, bootstyle=WARNING, width=15).grid(row=0, column=2, padx=5)
    ttk.Button(btn_frame, text="Delete", command=delete_contact, bootstyle=DANGER, width=15).grid(row=0, column=3, padx=5)

    # Search
    search_frame = ttk.Frame(root, padding=10)
    search_frame.pack()
    ttk.Label(search_frame, text="Search:").grid(row=0, column=0, padx=5)
    entry_search = ttk.Entry(search_frame, width=35)
    entry_search.grid(row=0, column=1, padx=5)
    ttk.Button(search_frame, text="Search", command=search_contact, bootstyle=PRIMARY, width=15).grid(row=0, column=2, padx=5)

    # Export
    ttk.Button(root, text="⬇ Export CSV", command=export_csv, bootstyle=SECONDARY, width=20).pack(pady=10)

    # Contact Table
    columns = ("ID", "Name", "Phone", "Email", "Address")
    contact_tree = ttk.Treeview(root, columns=columns, show="headings", bootstyle=INFO)
    for col in columns:
        contact_tree.heading(col, text=col)
        contact_tree.column(col, width=160)
    contact_tree.pack(fill="both", expand=True, pady=10)

    view_contacts()
    root.mainloop()

# -------------------- START APP --------------------
init_db()
open_login_window()
