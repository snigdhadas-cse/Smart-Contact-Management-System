import sqlite3
import csv
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, filedialog

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

    if not name or not phone:
        messagebox.showwarning("Input Error", "Name and Phone number are required!")
        return

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
    messagebox.showinfo("Deleted", "Contact deleted successfully!")
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

    if not name or not phone:
        messagebox.showwarning("Input Error", "Name and Phone number are required!")
        return

    run_query("""
        UPDATE contacts SET name=?, phone=?, email=?, address=?
        WHERE id=?
    """, (name, phone, email, address, contact_id))
    messagebox.showinfo("Updated", "Contact updated successfully!")
    clear_fields()
    view_contacts()

def clear_fields():
    entry_name.delete(0, 'end')
    entry_phone.delete(0, 'end')
    entry_email.delete(0, 'end')
    entry_address.delete(0, 'end')

# -------------------- CSV Import / Export --------------------
def export_csv():
    file = filedialog.asksaveasfilename(defaultextension=".csv",
                                        filetypes=[("CSV files", "*.csv")])
    if not file:
        return

    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, phone, email, address FROM contacts")
    data = cursor.fetchall()
    conn.close()

    with open(file, mode="w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Phone", "Email", "Address"])
        writer.writerows(data)
    messagebox.showinfo("Export Complete", "Contacts exported successfully!")

def import_csv():
    file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not file:
        return

    with open(file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                run_query("INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)",
                          (row["Name"], row["Phone"], row["Email"], row["Address"]))
            except sqlite3.IntegrityError:
                continue  # skip duplicates
    messagebox.showinfo("Import Complete", "Contacts imported successfully!")
    view_contacts()

# -------------------- UI Setup (ttkbootstrap) --------------------
root = ttk.Window(themename="cosmo")  # You can try: cosmo, flatly, solar, morph, etc.
root.title("Smart Contact Manager")
root.geometry("850x600")

# Title Label
ttk.Label(root, text="📒 Smart Contact Manager", font=("Segoe UI", 20, "bold")).pack(pady=15)

frame = ttk.Frame(root, padding=10)
frame.pack()

# Input Fields
ttk.Label(frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_name = ttk.Entry(frame, width=40)
entry_name.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame, text="Phone:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_phone = ttk.Entry(frame, width=40)
entry_phone.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(frame, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
entry_email = ttk.Entry(frame, width=40)
entry_email.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(frame, text="Address:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
entry_address = ttk.Entry(frame, width=40)
entry_address.grid(row=3, column=1, padx=5, pady=5)

# Buttons
btn_frame = ttk.Frame(root, padding=10)
btn_frame.pack()

ttk.Button(btn_frame, text="Add Contact", command=add_contact, bootstyle=SUCCESS, width=15).grid(row=0, column=0, padx=5, pady=5)
ttk.Button(btn_frame, text="View All", command=view_contacts, bootstyle=INFO, width=15).grid(row=0, column=1, padx=5, pady=5)
ttk.Button(btn_frame, text="Update", command=update_contact, bootstyle=WARNING, width=15).grid(row=0, column=2, padx=5, pady=5)
ttk.Button(btn_frame, text="Delete", command=delete_contact, bootstyle=DANGER, width=15).grid(row=0, column=3, padx=5, pady=5)

# Search Bar
search_frame = ttk.Frame(root, padding=10)
search_frame.pack()

ttk.Label(search_frame, text="🔍 Search:").grid(row=0, column=0, padx=5)
entry_search = ttk.Entry(search_frame, width=40)
entry_search.grid(row=0, column=1, padx=5)
ttk.Button(search_frame, text="Search", command=search_contact, bootstyle=PRIMARY, width=15).grid(row=0, column=2, padx=5)

# CSV Buttons
csv_frame = ttk.Frame(root, padding=10)
csv_frame.pack()

ttk.Button(csv_frame, text="⬆ Import CSV", command=import_csv, bootstyle=SECONDARY, width=15).grid(row=0, column=0, padx=10)
ttk.Button(csv_frame, text="⬇ Export CSV", command=export_csv, bootstyle=SUCCESS, width=15).grid(row=0, column=1, padx=10)

# Treeview (Contact List)
columns = ("ID", "Name", "Phone", "Email", "Address")
contact_tree = ttk.Treeview(root, columns=columns, show="headings", bootstyle=INFO)
for col in columns:
    contact_tree.heading(col, text=col)
    contact_tree.column(col, width=160)
contact_tree.pack(pady=10, fill="both", expand=True)

# Initialize
init_db()
view_contacts()

root.mainloop()
