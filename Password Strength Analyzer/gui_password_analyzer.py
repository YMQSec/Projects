import tkinter as tk
import os
from password_strength import check_password_strength, load_common_passwords, download_file  # Import functions

def update_feedback(event=None):
    """Updates the password feedback in real time."""
    password = password_entry.get()
    if not password.strip():
        feedback_text.set("")  # Clear feedback if no input
        return

    result = check_password_strength(password, common_passwords)
    feedback_text.set(f"Strength: {result['strength']}\n" + "\n".join([item['message'] for item in result['feedback']]))

# File path for the common passwords file
local_file_path = 'common_passwords.txt'

# Dropbox file URL
dropbox_file_url = 'https://www.dropbox.com/scl/fi/b58abyc3cb063br2fyxgn/common_passwords.txt?rlkey=bkbg0puqtkda3mtuu0d6zrx4p&st=65kf0nro&dl=1'

# Download the common passwords file from Dropbox if it's not already present
if not os.path.exists(local_file_path):
    print("Downloading the common passwords file from Dropbox...")
    download_file(dropbox_file_url, local_file_path)  # Full Dropbox file URL
    print("Download complete!")

# Load the common passwords once
common_passwords = load_common_passwords(local_file_path)

# Create the main GUI window
root = tk.Tk()
root.title("Password Strength Analyzer")

# Add widgets
tk.Label(root, text="Enter Password:").pack(pady=5)
password_entry = tk.Entry(root, show="*")
password_entry.pack(pady=5)
password_entry.bind("<KeyRelease>", update_feedback)  # Bind real-time feedback to key release

feedback_text = tk.StringVar()
feedback_label = tk.Label(root, textvariable=feedback_text, justify="left")
feedback_label.pack(pady=10)

# Start the GUI event loop
root.mainloop()
