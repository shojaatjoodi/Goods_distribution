# main.py
# we will considder this as a main module. 
# we will run all the code in the main.py file
# we will connect all the functions and modules in the main.py file
# we will consider the whole tables inside distribution_system.sql with other functions inside other modules and their relations
## I need to apply all the changes to the main.py file and run it to test the whole system 

from dotenv import load_dotenv

from db import connect_db, close_database_connection # Import the database connection functions from db.py

# Import the modules for different functionalities 
import tkinter as tk
from tkinter import messagebox
from citizens import open_citizen_window
from goods import open_goods_window
from distribution import open_distribution_window
from reports import open_reports_window
import atexit 

from stringsUI import * # Import all the strings from strings.py

load_dotenv() # Load environment variables from .env file

# Establish database connection 
db_connection = connect_db()
# Ensure the connection is closed when the program exits
atexit.register(close_database_connection, db_connection)

# # Ensure the connection is closed when the program exits
# if db_connection:
#     atexit.register(close_database_connection, db_connection)
# else:
#     messagebox.showerror("Database Error", "Failed to connect to the database. Please check your configuration.")
#     exit(1) # Exit the program if the connection fails

def main():
    language = "english"  # Set the default language to English
    ui_language = json_en_messages
    if language == "persian":
        ui_language = json_per_messages
    if language == "english":
        ui_language = json_en_messages
            
    # Check if the database connection is established 
    if db_connection is None or not db_connection.is_connected():
        messagebox.showerror("Database Connection Error", "Failed to connect to the database.")
        return
    

    # Create the main window for the application 
    root = tk.Tk()
    root.title(ui_language.APP_TITLE) # Set the title of the window
    root.geometry("700x600")

    tk.Label(root, text=ui_language.WELCOME_MESSAGE, font=("Helvetica", 14)).pack(pady=20) # Welcome message
    tk.Label(root, text="Please select an option from the menu below:", font=("Helvetica", 12)).pack(pady=10) # Instruction message
    tk.Button(root, text="Manage Citizens", font=("Helvetica", 12), width=35, command=open_citizen_window).pack(pady=10) # Open citizen management window
    tk.Button(root, text="Manage Goods & Deliveries",font=("Helvetica", 12), width=35, command=open_goods_window).pack(pady=10) # Open goods management window
    tk.Button(root, text="Distribute Goods",font=("Helvetica", 12), width=35, command=open_distribution_window).pack(pady=10) # Open distribution management window
    tk.Button(root, text="View Reports", font=("Helvetica", 12), width=35, command=open_reports_window).pack(pady=10) # Open reports window
    # Placeholder buttons for additional functionalities
    # tk.Button(root, text="Manage Suppliers", font=("Helvetica", 12), width=35, command=open_goods_window).pack(pady =10)  # Placeholder for supplier management
    tk.Button(root, text="Manage Companies",font=("Helvetica", 12), width=35, command=open_goods_window).pack(pady=10)  # Placeholder for company management
    
    # to sharpen the code and make it more readable we can create a function to create the buttons
    # def create_button(text, command):
    #     button = tk.Button(root, text=text, width=30, command=command)
    #     button.pack(pady=10) #     return button
    # create_button("Manage Citizens", open_citizen_window) # width is used to set the width of the button
    
    # # Title Label
    # title_label = tk.Label(root, text="Goods Distribution Management", font=("Arial", 18, "bold"))
    # title_label.pack(pady=20) # Add some padding for better spacing , its functionality is to show the title of 
    # # the system Welcome Message
    # # Buttons for modules
    # citizen_btn = tk.Button(root, text="Manage Citizens", width=30, command=open_citizen_window)
    # citizen_btn.pack(pady=10) # pady is used to add some space between the buttons

    # Exit button
    # fiirst ask the user if he wants to exit the application or not
    # if yes then exit the application
    # if no then return to the main menu 
    # exit_btn = tk.Button(root, text="Exit", width=30, command=root.quit)
    # exit_btn.pack(pady=20) # Exit the application
    # The command is to quit the application

    # Exit button
    def confirm_exit():
        """Ask the user for confirmation before exiting the application."""
        if messagebox.askyesno("Exit Confirmation", "Are you sure you want to exit the application?"):
            root.quit()  # Exit the application if the user confirms

    exit_btn = tk.Button(root, text="Exit", width=30, font=("Helvetica", 14), command=confirm_exit, bg="red", fg="white")
    exit_btn.pack(pady=20)



    # exit_btn = tk.Button(root, text="Exit", width=30, font=("Helvetica", 14), command=root.quit, bg="red", fg="white") # Exit the application
    # # The command is to quit the application
    # # The bg is used to set the background color of the button and fg is used to set the foreground color of the button
    # # The width is used to set the width of the button
    # exit_btn.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
