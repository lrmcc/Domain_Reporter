import shutil
import os
import tkinter.messagebox as tkmsg
from gui import Application

if __name__ == "__main__":
    from tkinter import messagebox as tkmsg  # Moved import statement

    # Check if whois is installed
    if not shutil.which("whois"):
        tkmsg.showerror("Error", "Whois is not installed. Please install Whois for the script to run as intended.")

    # Create "logs" directory if it doesn't exist
    logs_dir = os.path.join(os.getcwd(), "logs")
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
        print(f"Created 'logs' directory at {logs_dir}.\n")

    
    app = Application()
    app.mainloop()
