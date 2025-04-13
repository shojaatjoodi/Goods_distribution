from dotenv import load_dotenv 
from db import connect_db, close_database_connection 
import tkinter as tk
from tkinter import messagebox
from citizens import open_citizen_window
from goods import open_goods_window
from distribution import open_distribution_window
from reports import open_reports_window
import atexit 
from stringsUI import * 

load_dotenv() # Load environment variables from .env file

# Establish database connection 
db_connection = connect_db() 
atexit.register(close_database_connection, db_connection)


def main():
    language = "english"  # Set the default language 
    ui_language = json_en_messages
    if language == "persian":
        ui_language = json_per_messages
    if language == "english":
        ui_language = json_en_messages
    if language == "turkish":
        ui_language = json_turkish_messages         
    if db_connection is None or not db_connection.is_connected():
        messagebox.showerror("Database Connection Error", "Failed to connect to the database.")
        return
    

    # Create the main window for the application 
    root = tk.Tk()
    root.title(ui_language.APP_TITLE) 
    root.geometry("700x600")

    tk.Label(root, text=ui_language.WELCOME_MESSAGE, font=("Helvetica", 14)).pack(pady=20) # Welcome message
    tk.Label(root, text="Please select an option from the menu below:", font=("Helvetica", 12)).pack(pady=10) # Instruction message
    tk.Button(root, text="Manage Citizens", font=("Helvetica", 12), width=35, command=open_citizen_window).pack(pady=10) # Open citizen management window
    tk.Button(root, text="Manage Goods & Deliveries",font=("Helvetica", 12), width=35, command=open_goods_window).pack(pady=10) # Open goods management window
    tk.Button(root, text="Distribute Goods",font=("Helvetica", 12), width=35, command=open_distribution_window).pack(pady=10) # Open distribution management window
    tk.Button(root, text="View Reports", font=("Helvetica", 12), width=35, command=open_reports_window).pack(pady=10) # Open reports window 
    tk.Button(root, text="Manage Companies",font=("Helvetica", 12), width=35, command=open_goods_window).pack(pady=10)  # Placeholder for company management
    
    def confirm_exit(): 
        """Ask the user for confirmation before exiting the application."""
        if messagebox.askyesno("Exit Confirmation", "Are you sure you want to exit the application?"):
            root.quit()

    exit_btn = tk.Button(root, text="Exit", width=30, font=("Helvetica", 14), command=confirm_exit, bg="red", fg="white")
    exit_btn.pack(pady=20)
  
    root.mainloop()

if __name__ == "__main__":
    main()
