# This module handles the citizen management functionality of the application.  

import tkinter as tk
from tkinter import messagebox, ttk
# Import the database connection functions from db.py
from db import connect_db 
def add_citizen(name, national_id, address, phone):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = """
            INSERT INTO Citizens (name, national_id, address, phone)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (name, national_id, address, phone))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Citizen added successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add citizen:\n{e}")

def fetch_citizens():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT citizen_id, name, national_id, address, phone, eligible FROM Citizens")
        result = cursor.fetchall()
        conn.close()
        return result
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch citizens:\n{e}")
        return []

def delete_citizen(citizen_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Citizens WHERE citizen_id = %s", (citizen_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Citizen deleted successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete citizen:\n{e}")
        

def open_citizen_window():
    window = tk.Toplevel()
    window.title("Manage Citizens")
    window.geometry("800x550")

    # --- Input form ---
    frame = tk.LabelFrame(window, text="Add New Citizen", padx=10, pady=10)
    frame.pack(pady=10, fill="x", padx=10)

    tk.Label(frame, text="Full Name").grid(row=0, column=0, padx=5, pady=5)
    tk.Label(frame, text="National ID").grid(row=1, column=0, padx=5, pady=5)
    tk.Label(frame, text="Address").grid(row=0, column=2, padx=5, pady=5)
    tk.Label(frame, text="Phone").grid(row=1, column=2, padx=5, pady=5)

    name_entry = tk.Entry(frame)
    id_entry = tk.Entry(frame)
    address_entry = tk.Entry(frame)
    phone_entry = tk.Entry(frame)

    name_entry.grid(row=0, column=1, padx=5)
    id_entry.grid(row=1, column=1, padx=5)
    address_entry.grid(row=0, column=3, padx=5)
    phone_entry.grid(row=1, column=3, padx=5)



    def on_add(): 
        name = name_entry.get() 
        nid = id_entry.get() 
        if len(nid) != 10 or not nid.isdigit():
            messagebox.showwarning("Input Error", "National ID must be a 10 digit number.")
            return
        address = address_entry.get() 
        phone = phone_entry.get() 
        # Check if the phone number is 10 digit number
        if len(phone) != 10 or not phone.isdigit():
            messagebox.showwarning("Input Error", "Phone number must be a 10 digit number, without + sign.")
            return
        if name and nid:
            add_citizen(name, nid, address, phone)
            refresh_citizen_list()
            name_entry.delete(0, 'end')
            id_entry.delete(0, 'end')
            address_entry.delete(0, 'end')
            phone_entry.delete(0, 'end')
        else:
            messagebox.showwarning("Input Error", "Name and National ID are required.")

    # # Button to add a new citizen 
    tk.Button(frame, text="Add Citizen", command=on_add).grid(row=2, column=1, pady=10)


    # --- Search bar ---
    search_frame = tk.LabelFrame(window, text="Search Citizens", padx=10, pady=10)
    search_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(search_frame, text="Search by:").grid(row=0, column=0, padx=5)

    search_type = tk.StringVar()
    search_type.set("Name")
    dropdown = ttk.Combobox(search_frame, textvariable=search_type, values=["Name", "National ID"], state="readonly", width=12)
    dropdown.grid(row=0, column=1)

    search_entry = tk.Entry(search_frame, width=50)
    search_entry.grid(row=0, column=2, padx=5)

    # --- Citizens list ---
    list_frame = tk.LabelFrame(window, text="Citizens List", padx=10, pady=10)
    list_frame.pack(fill="both", expand=True, padx=10)

    columns = ("ID", "Name", "National ID", "Address", "Phone", "Eligible")
    tree = ttk.Treeview(list_frame, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120 if col == "Name" else 100)

    tree.pack(fill="both", expand=True)

    def refresh_citizen_list(filtered=None):
        for row in tree.get_children():
            tree.delete(row)
        data = filtered if filtered is not None else fetch_citizens()
        for citizen in data:
            tree.insert("", "end", values=citizen)

    def on_search(event=None):
        keyword = search_entry.get().lower()
        key = search_type.get()
        filtered = []
        for citizen in fetch_citizens():
            value = citizen[1].lower() if key == "Name" else citizen[2].lower()
            if keyword in value:
                filtered.append(citizen)
        refresh_citizen_list(filtered)

    search_entry.bind("<KeyRelease>", on_search)

    refresh_citizen_list() 