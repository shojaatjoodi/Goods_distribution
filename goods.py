

# goods.py

import tkinter as tk
from tkinter import ttk, messagebox
import xlsxwriter # pip install xlsxwriter
# Import the database connection functions from db.py
from db import connect_db # Assuming you have a db.py file with the connect_db function defined

def fetch_goods():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT good_id, name, stock_quantity FROM Goods")
    rows = cursor.fetchall()
    conn.close()
    return rows

def fetch_suppliers():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT supplier_id, name FROM Suppliers")
    rows = cursor.fetchall()
    conn.close()
    return rows

def fetch_companies():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT company_id, name FROM Companies")
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_delivery(good_id, supplier_id, company_id, quantity):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Insert into Deliveries table
        query = """
            INSERT INTO Deliveries (good_id, supplier_id, company_id, quantity_received)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (good_id, supplier_id, company_id, quantity))

        # Update Goods stock
        update = "UPDATE Goods SET stock_quantity = stock_quantity + %s WHERE good_id = %s"
        cursor.execute(update, (quantity, good_id))

        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Delivery recorded and stock updated.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add delivery:\n{e}")


# def fetch_delivery_history():
#     conn = connect_db()
#     cursor = conn.cursor()
#     query = """
#         SELECT d.delivery_id, g.name, s.name, c.name, d.quantity_received, d.delivery_date
#         FROM Deliveries d
#         JOIN Goods g ON d.good_id = g.good_id
#         JOIN Suppliers s ON d.supplier_id = s.supplier_id
#         JOIN Companies c ON d.company_id = c.company_id
#         ORDER BY d.delivery_date DESC
#     """
#     cursor.execute(query)
#     rows = cursor.fetchall()
#     conn.close()
#     return rows



def open_goods_window():
    window = tk.Toplevel()
    window.title("Manage Goods & Deliveries")
    window.geometry("800x800")

    # --- Goods List ---
    goods_frame = tk.LabelFrame(window, text="Current Goods Stock", padx=10, pady=10)
    goods_frame.pack(fill="x", padx=10, pady=5)

    columns = ("ID", "Name", "Stock")
    tree = ttk.Treeview(goods_frame, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    tree.pack(fill="x", expand=True)

    def refresh_goods():
        for row in tree.get_children():
            tree.delete(row)
        for good in fetch_goods():
            tree.insert("", "end", values=good)

    refresh_goods()

    # --- Add Delivery ---
    delivery_frame = tk.LabelFrame(window, text="Record New Delivery", padx=10, pady=10)
    delivery_frame.pack(fill="both", expand=True, padx=10, pady=5)

    tk.Label(delivery_frame, text="Good:").grid(row=0, column=0, padx=5, pady=5)
    tk.Label(delivery_frame, text="Supplier:").grid(row=1, column=0, padx=5, pady=5)
    tk.Label(delivery_frame, text="Company:").grid(row=2, column=0, padx=5, pady=5)
    tk.Label(delivery_frame, text="Quantity Received:").grid(row=3, column=0, padx=5, pady=5)
    tk.Label(delivery_frame, text="Scale: Kg").grid(row=4, column=1, padx=5, pady=5) # this not implemented in database yet
    tk.Label(delivery_frame, text="Delivery Date:").grid(row=5, column=0, padx=5, pady=5) 

    goods = fetch_goods()
    suppliers = fetch_suppliers()
    companies = fetch_companies()

    good_var = tk.StringVar()
    supplier_var = tk.StringVar()
    company_var = tk.StringVar()
    quantity_entry = tk.Entry(delivery_frame)

    goods_map = {f"{g[1]} (Stock: {g[2]})": g[0] for g in goods}
    supplier_map = {s[1]: s[0] for s in suppliers}
    company_map = {c[1]: c[0] for c in companies}

    goods_menu = ttk.Combobox(delivery_frame, textvariable=good_var, values=list(goods_map.keys()), width=40)
    supplier_menu = ttk.Combobox(delivery_frame, textvariable=supplier_var, values=list(supplier_map.keys()), width=40)
    company_menu = ttk.Combobox(delivery_frame, textvariable=company_var, values=list(company_map.keys()), width=40)

    goods_menu.grid(row=0, column=1, pady=5, sticky="w")
    supplier_menu.grid(row=1, column=1, pady=5, sticky="w")
    company_menu.grid(row=2, column=1, pady=5, sticky="w")
    quantity_entry.grid(row=3, column=1, pady=5, sticky="w")

    def submit_delivery():
        try:
            gid = goods_map[good_var.get()]
            sid = supplier_map[supplier_var.get()]
            cid = company_map[company_var.get()]
            quantity = int(quantity_entry.get())

            if quantity > 0:
                add_delivery(gid, sid, cid, quantity)
                refresh_goods()
                refresh_history()
                quantity_entry.delete(0, 'end')
            else:
                messagebox.showwarning("Invalid Input", "Quantity must be positive.")
        except Exception as e:
            messagebox.showerror("Error", f"Check your input:\n{e}")

    tk.Button(delivery_frame, text="Add Delivery", command=submit_delivery).grid(row=4, column=1, pady=15)

    # tk.Button(delivery_frame, text="Refresh Goods", command=refresh_goods).grid(row=4, column=0, pady=10)
    # refresh_goods()


    # --- Delivery History ---
    history_frame = tk.LabelFrame(window, text="Delivery History", padx=10, pady=10)
    history_frame.pack(fill="both", expand=True, padx=10, pady=5)

    history_columns = ("ID", "Good", "Supplier", "Company", "Quantity", "Date")
    history_tree = ttk.Treeview(history_frame, columns=history_columns, show="headings")

    for col in history_columns:
        history_tree.heading(col, text=col)
        history_tree.column(col, width=120)

    history_tree.pack(fill="both", expand=True)

    def fetch_delivery_history():
        conn = connect_db()
        cursor = conn.cursor()
        query = """
            SELECT d.delivery_id, g.name, s.name, c.name, d.quantity_received, d.delivery_date
            FROM Deliveries d
            JOIN Goods g ON d.good_id = g.good_id
            JOIN Suppliers s ON d.supplier_id = s.supplier_id
            JOIN Companies c ON d.company_id = c.company_id
            ORDER BY d.delivery_date DESC
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    # This function fetches the delivery history from the database and populates the treeview
    # It is called when the window is opened and after a new delivery is added
    # It will be called when the button is clicked

    # now filter the delivery history by date, company, and good
    # def filter_delivery_history(start_date, end_date, company_id, good_id):
    #     conn = connect_db()
    #     cursor = conn.cursor()
    #     query = """
    #         SELECT d.delivery_id, g.name, s.name, c.name, d.quantity_received, d.delivery_date
    #         FROM Deliveries d
    #         JOIN Goods g ON d.good_id = g.good_id
    #         JOIN Suppliers s ON d.supplier_id = s.supplier_id
    #         JOIN Companies c ON d.company_id = c.company_id
    #         WHERE d.delivery_date BETWEEN %s AND %s
    #         AND d.company_id = %s
    #         AND d.good_id = %s
    #         ORDER BY d.delivery_date DESC
    #     """
    #     cursor.execute(query, (start_date, end_date, company_id, good_id))
    #     rows = cursor.fetchall()
    #     conn.close()
    #     return rows

    # showing just specific company delivery history
    def show_per_company_history(company_id):
        conn = connect_db()
        cursor = conn.cursor()
        query = """
            SELECT d.delivery_id, g.name, s.name, c.name, d.quantity_received, d.delivery_date
            FROM Deliveries d
            JOIN Goods g ON d.good_id = g.good_id
            JOIN Suppliers s ON d.supplier_id = s.supplier_id
            JOIN Companies c ON d.company_id = c.company_id
            WHERE d.company_id = %s
            ORDER BY d.delivery_date DESC
        """
        cursor.execute(query, (company_id,))
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    
    # adding a button to show delivery history per company
    def show_history_per_company():
        company_id = company_map[company_menu.get()]
        for row in history_tree.get_children():
            history_tree.delete(row)
        for item in show_per_company_history(company_id):
            history_tree.insert("", "end", values=item)


    # showing just specific good delivery history
    def show_per_good_history(good_id):
        conn = connect_db()
        cursor = conn.cursor()
        query = """
            SELECT d.delivery_id, g.name, s.name, c.name, d.quantity_received, d.delivery_date
            FROM Deliveries d
            JOIN Goods g ON d.good_id = g.good_id
            JOIN Suppliers s ON d.supplier_id = s.supplier_id
            JOIN Companies c ON d.company_id = c.company_id
            WHERE d.good_id = %s
            ORDER BY d.delivery_date DESC
        """
        cursor.execute(query, (good_id,))
        rows = cursor.fetchall()
        conn.close()
        return rows

    # adding a button to show delivery history per good
    def show_history_per_good():
        good_id = goods_map[goods_menu.get()]
        for row in history_tree.get_children():
            history_tree.delete(row)
        for item in show_per_good_history(good_id):
            history_tree.insert("", "end", values=item)

    # adding a button to show delivery history per good
    tk.Button(delivery_frame, text="Show History Per Good", command=show_history_per_good).grid(row=5, column=0, pady=10)
    # Adding a button to show delivery history per company
    tk.Button(delivery_frame, text="Show History Per Company", command=show_history_per_company).grid(row=5, column=1, pady=10)

    # Adding a button to show delivery history per date
    # tk.Button(delivery_frame, text="Show History Per Date", command=show_history_per_date).grid(row=5, column=2, pady=10)


    # Adding a function to store the delivery history in a excel file
    def export_delivery_history_to_excel():
        try:
            conn = connect_db()
            cursor = conn.cursor()
            query = """
                SELECT d.delivery_id, g.name, s.name, c.name, d.quantity_received, d.delivery_date
                FROM Deliveries d
                JOIN Goods g ON d.good_id = g.good_id
                JOIN Suppliers s ON d.supplier_id = s.supplier_id
                JOIN Companies c ON d.company_id = c.company_id
                ORDER BY d.delivery_date DESC
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            conn.close()  

            # Create a new workbook and add a worksheet
            workbook = xlsxwriter.Workbook('delivery_history.xlsx')
            worksheet = workbook.add_worksheet()
            # Define the header format
            header_format = workbook.add_format({'bold': True, 'bg_color': '#FFA07A', 'border': 1})
            # Write the header row
            headers = ["ID", "Good", "Supplier", "Company", "Quantity", "Date"]
            for col_num, header in enumerate(headers):
                worksheet.write(0, col_num, header, header_format)
            # Write the data rows
            for row_num, row in enumerate(rows, 1):
                # here we can add a code to show data of the delivery history in a better way
                # for example we can add a code to show the just for the specific company or good, date, etc: let's do it now:
                # then we can add the data to the excel file, 
                for col_num, value in enumerate(row):
                    worksheet.write(row_num, col_num, value)
            workbook.close()
            messagebox.showinfo("Success", "Delivery history exported to delivery_history.xlsx")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export delivery history:\n{e}")

    # Adding a button to store the delivery history in an excel file
    tk.Button(delivery_frame, text="Export Data to Excel", command=export_delivery_history_to_excel).grid(row=5, column=3, pady=10)



    def refresh_history():
        for row in history_tree.get_children():
            history_tree.delete(row)
        for item in fetch_delivery_history():
            history_tree.insert("", "end", values=item)

    # Initial load
    refresh_history()

        # Adding a button to show all delivery history
    tk.Button(delivery_frame, text="Show All History", command=refresh_history).grid(row=5, column=2, pady=10)


# we will considder this as a module and not run it directly
# we will run all the code in the main.py file 

