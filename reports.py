
# reports.py

import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox

# Import the database connection functions from db.py
from db import connect_db # Assuming you have a db.py file with the connect_db function defined


# --- Export to Excel Function ---
def export_to_excel(data, columns, filename):
    try:
        # Convert the data to a pandas DataFrame
        df = pd.DataFrame(data, columns=columns)
        # Write the DataFrame to an Excel file
        df.to_excel(filename, index=False, engine='openpyxl')
        messagebox.showinfo("Success", f"Report successfully exported to {filename}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to export report: {e}")

# --- Function to generate Total Goods Distributed per Item Report ---
def total_goods_per_item_report():
    try:
        # Create a new report window
        report_window = tk.Toplevel()
        report_window.title("Total Goods Distributed per Item")
        report_window.geometry("800x600")

        # Create the treeview (table) to display the report
        columns = ("Good", "Total Quantity Distributed")
        tree = ttk.Treeview(report_window, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200)

        tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Fetch the total goods distributed per item
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT g.name, SUM(d.quantity_given) as total_quantity
            FROM Distributions d
            JOIN Goods g ON d.good_id = g.good_id
            GROUP BY g.name
            ORDER BY total_quantity DESC
        """)
        rows = cursor.fetchall()
        conn.close()

        # Insert the rows into the treeview
        for row in rows:
            tree.insert("", "end", values=row)

        # Add Export to Excel button
        def export_report():
            export_to_excel(rows, columns, "goods_per_item_report.xlsx")

        export_button = tk.Button(report_window, text="Export to Excel", command=export_report)
        export_button.pack(pady=10)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate report: {e}")

# --- Function to generate Report: Total Goods Distributed per Company ---
def total_goods_per_company_report():
    try:
        # Create a new report window
        report_window = tk.Toplevel()
        report_window.title("Total Goods Distributed per Company")
        report_window.geometry("800x600")

        # Create the treeview (table) to display the report
        columns = ("Company", "Total Quantity Distributed")
        tree = ttk.Treeview(report_window, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200)

        tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Fetch the total goods distributed per company
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT cp.name, SUM(d.quantity_given) as total_quantity
            FROM Distributions d
            JOIN Companies cp ON d.company_id = cp.company_id
            GROUP BY cp.name
            ORDER BY total_quantity DESC
        """)
        rows = cursor.fetchall()
        conn.close()

        # Insert the rows into the treeview
        for row in rows:
            tree.insert("", "end", values=row)

        # Add Export to Excel button
        def export_report():
            export_to_excel(rows, columns, "goods_per_company_report.xlsx")

        export_button = tk.Button(report_window, text="Export to Excel", command=export_report)
        export_button.pack(pady=10)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate report: {e}")

# --- Function to generate Report: Total Goods Distributed per Citizen ---
def total_goods_per_citizen_report():
    try:
        # Create a new report window
        report_window = tk.Toplevel()
        report_window.title("Total Goods Distributed per Citizen")
        report_window.geometry("800x600")

        # Create the treeview (table) to display the report
        columns = ("Citizen", "Total Quantity Distributed")
        tree = ttk.Treeview(report_window, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200)

        tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Fetch the total goods distributed per citizen
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.full_name, SUM(d.quantity_given) as total_quantity
            FROM Distributions d
            JOIN Citizens c ON d.citizen_id = c.citizen_id
            GROUP BY c.full_name
            ORDER BY total_quantity DESC
        """)
        rows = cursor.fetchall()
        conn.close()

        # Insert the rows into the treeview
        for row in rows:
            tree.insert("", "end", values=row)

        # Add Export to Excel button
        def export_report():
            export_to_excel(rows, columns, "goods_per_citizen_report.xlsx")

        export_button = tk.Button(report_window, text="Export to Excel", command=export_report)
        export_button.pack(pady=10)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate report: {e}")

# --- Main Window to Show Available Reports ---
def open_reports_window():
    window = tk.Toplevel()
    window.title("Reports")
    window.geometry("400x300")

    # Create buttons for each report
    total_goods_button = tk.Button(window, text="Total Goods per Item", command=total_goods_per_item_report)
    total_goods_button.pack(pady=10)

    total_goods_per_company_button = tk.Button(window, text="Total Goods per Company", command=total_goods_per_company_report)
    total_goods_per_company_button.pack(pady=10)

    total_goods_per_citizen_button = tk.Button(window, text="Total Goods per Citizen", command=total_goods_per_citizen_report)
    total_goods_per_citizen_button.pack(pady=10)



# we will considder this as a module and not run it directly
# we will run the main.py file to test the reports module 

# Example usage: open the reports window
# open_reports_window()

# Note: This code assumes that the database and tables are already set up correctly.
# Make sure to replace the database connection details with your actual database configuration.

# Also, ensure that the necessary libraries (tkinter, mysql.connector) are installed in your Python environment.
# You can install mysql-connector-python using pip:
# pip install mysql-connector-python
# If you're using PostgreSQL, you can install psycopg2 using pip:
# pip install psycopg2
# If you're using MySQL, you can install mysql-connector-python using pip:
# pip install mysql-connector-python
# then change the import statement accordingly.
#  for MySQL:
# import mysql.connector

# then change the connection string in connect_db() to match your MySQL database configuration. 

# tkinter is included in the standard library, so you don't need to install it separately. 