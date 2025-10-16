import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# -------------------- Database Setup --------------------
def init_db():
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL UNIQUE,
            email TEXT,
            address TEXT
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

# -------------------- Functions --------------------
def add_contact():
    name = entry_name.get().strip()
    phone = entry_phone.get().strip()
    email = entry_email.get().strip()
    address = entry_address.get().strip()

    if name == "" or phone == "":
        messagebox.showwarning("Input Error", "Name and Phone number are required!")
    else:
        try:
            run_query("INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)",
                      (name, phone, email, address))
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
    search_term = entry_search.get().lower()
    for row in contact_tree.get_children():
        contact_tree.delete(row)
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM contacts
        WHERE LOWER(name) LIKE ? OR phone LIKE ?
    """, ('%' + search_term + '%', '%' + search_term + '%'))
    for row in cursor.fetchall():
        contact_tree.insert("", "end", values=row)
    conn.close()

def delete_contact():
    selected_item = contact_tree.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Select a contact to delete!")
        return
    contact_id = contact_tree.item(selected_item)["values"][0]
    run_query("DELETE FROM contacts WHERE id=?", (contact_id,))
    messagebox.showinfo("Success", "Contact deleted successfully!")
    view_contacts()

def update_contact():
    selected_item = contact_tree.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Select a contact to update!")
        return

    contact_id = contact_tree.item(selected_item)["values"][0]
    name = entry_name.get().strip()
    phone = entry_phone.get().strip()
    email = entry_email.get().strip()
    address = entry_address.get().strip()

    if name == "" or phone == "":
        messagebox.showwarning("Input Error", "Name and Phone number are required!")
    else:
        run_query("""
            UPDATE contacts SET name=?, phone=?, email=?, address=?
            WHERE id=?
        """, (name, phone, email, address, contact_id))
        messagebox.showinfo("Success", "Contact updated successfully!")
        clear_fields()
        view_contacts()

def clear_fields():
    entry_name.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_address.delete(0, tk.END)

# -------------------- UI Setup --------------------
root = tk.Tk()
root.title("Contact Management System")
root.geometry("750x550")
root.config(bg="#e8f0fe")

frame = tk.Frame(root, bg="#e8f0fe")
frame.pack(pady=10)

tk.Label(frame, text="Name:", bg="#e8f0fe").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_name = tk.Entry(frame, width=35)
entry_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Phone:", bg="#e8f0fe").grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_phone = tk.Entry(frame, width=35)
entry_phone.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame, text="Email:", bg="#e8f0fe").grid(row=2, column=0, padx=5, pady=5, sticky="e")
entry_email = tk.Entry(frame, width=35)
entry_email.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame, text="Address:", bg="#e8f0fe").grid(row=3, column=0, padx=5, pady=5, sticky="e")
entry_address = tk.Entry(frame, width=35)
entry_address.grid(row=3, column=1, padx=5, pady=5)

btn_frame = tk.Frame(root, bg="#e8f0fe")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add", command=add_contact, bg="#34a853", fg="white", width=15).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="View All", command=view_contacts, bg="#4285f4", fg="white", width=15).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Update", command=update_contact, bg="#fbbc05", fg="black", width=15).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Delete", command=delete_contact, bg="#ea4335", fg="white", width=15).grid(row=0, column=3, padx=5)

search_frame = tk.Frame(root, bg="#e8f0fe")
search_frame.pack(pady=10)

tk.Label(search_frame, text="Search:", bg="#e8f0fe").grid(row=0, column=0, padx=5)
entry_search = tk.Entry(search_frame, width=35)
entry_search.grid(row=0, column=1, padx=5)
tk.Button(search_frame, text="Search", command=search_contact, bg="#673ab7", fg="white", width=15).grid(row=0, column=2, padx=5)

columns = ("ID", "Name", "Phone", "Email", "Address")
contact_tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    contact_tree.heading(col, text=col)
    contact_tree.column(col, width=140)
contact_tree.pack(pady=10)

# -------------------- Initialize --------------------
init_db()
view_contacts()

root.mainloop()
