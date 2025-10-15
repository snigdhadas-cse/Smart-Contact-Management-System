import tkinter as tk
from tkinter import messagebox, ttk

# Initialize main window
root = tk.Tk()
root.title("Contact Management System")
root.geometry("700x500")
root.config(bg="#e8f0fe")

# Contact list (temporary in-memory storage)
contacts = []

# Functions
def add_contact():
    name = entry_name.get()
    phone = entry_phone.get()
    email = entry_email.get()
    address = entry_address.get()

    if name == "" or phone == "":
        messagebox.showwarning("Input Error", "Name and Phone number are required!")
    else:
        contacts.append({"name": name, "phone": phone, "email": email, "address": address})
        messagebox.showinfo("Success", "Contact added successfully!")
        clear_fields()
        view_contacts()

def view_contacts():
    for row in contact_tree.get_children():
        contact_tree.delete(row)
    for contact in contacts:
        contact_tree.insert("", "end", values=(contact["name"], contact["phone"], contact["email"], contact["address"]))

def search_contact():
    search_term = entry_search.get().lower()
    for row in contact_tree.get_children():
        contact_tree.delete(row)
    for contact in contacts:
        if search_term in contact["name"].lower() or search_term in contact["phone"]:
            contact_tree.insert("", "end", values=(contact["name"], contact["phone"], contact["email"], contact["address"]))

def delete_contact():
    selected_item = contact_tree.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Select a contact to delete!")
        return
    selected_contact = contact_tree.item(selected_item)["values"]
    for contact in contacts:
        if contact["name"] == selected_contact[0] and contact["phone"] == selected_contact[1]:
            contacts.remove(contact)
            break
    messagebox.showinfo("Success", "Contact deleted successfully!")
    view_contacts()

def update_contact():
    selected_item = contact_tree.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Select a contact to update!")
        return

    selected_contact = contact_tree.item(selected_item)["values"]
    for contact in contacts:
        if contact["name"] == selected_contact[0] and contact["phone"] == selected_contact[1]:
            contact["name"] = entry_name.get()
            contact["phone"] = entry_phone.get()
            contact["email"] = entry_email.get()
            contact["address"] = entry_address.get()
            break
    messagebox.showinfo("Success", "Contact updated successfully!")
    clear_fields()
    view_contacts()

def clear_fields():
    entry_name.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_address.delete(0, tk.END)

# UI Layout
frame = tk.Frame(root, bg="#e8f0fe")
frame.pack(pady=10)

tk.Label(frame, text="Name:", bg="#e8f0fe").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_name = tk.Entry(frame, width=30)
entry_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Phone:", bg="#e8f0fe").grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_phone = tk.Entry(frame, width=30)
entry_phone.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame, text="Email:", bg="#e8f0fe").grid(row=2, column=0, padx=5, pady=5, sticky="e")
entry_email = tk.Entry(frame, width=30)
entry_email.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame, text="Address:", bg="#e8f0fe").grid(row=3, column=0, padx=5, pady=5, sticky="e")
entry_address = tk.Entry(frame, width=30)
entry_address.grid(row=3, column=1, padx=5, pady=5)

# Buttons
btn_frame = tk.Frame(root, bg="#e8f0fe")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add Contact", command=add_contact, bg="#34a853", fg="white", width=15).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="View All", command=view_contacts, bg="#4285f4", fg="white", width=15).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Update", command=update_contact, bg="#fbbc05", fg="black", width=15).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Delete", command=delete_contact, bg="#ea4335", fg="white", width=15).grid(row=0, column=3, padx=5)

# Search Section
search_frame = tk.Frame(root, bg="#e8f0fe")
search_frame.pack(pady=10)

tk.Label(search_frame, text="Search:", bg="#e8f0fe").grid(row=0, column=0, padx=5)
entry_search = tk.Entry(search_frame, width=30)
entry_search.grid(row=0, column=1, padx=5)
tk.Button(search_frame, text="Search", command=search_contact, bg="#673ab7", fg="white", width=15).grid(row=0, column=2, padx=5)

# Contact List (Treeview)
columns = ("Name", "Phone", "Email", "Address")
contact_tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    contact_tree.heading(col, text=col)
    contact_tree.column(col, width=150)
contact_tree.pack(pady=10)

root.mainloop()
