import tkinter as tk
import os
import requests
import zipfile
import re

# Current version of the app
LOCAL_VERSION = "1.0.0"

# URL for the version.txt file on GitHub
GITHUB_VERSION_URL = "https://raw.githubusercontent.com/YMQSec/Projects/main/Password%20Strength%20Analyzer/version.txt"

# URL to download the latest version's zip from GitHub
GITHUB_ZIP_URL = "https://github.com/YMQSec/Projects/archive/refs/heads/main.zip"

# Dropbox URL for the common passwords file
DROPBOX_FILE_URL = 'https://www.dropbox.com/scl/fi/b58abyc3cb063br2fyxgn/common_passwords.txt?rlkey=bkbg0puqtkda3mtuu0d6zrx4p&st=65kf0nro&dl=1'

# Local path for storing the common passwords file temporarily
local_file_path = 'common_passwords.txt'

# Download the common passwords file if it doesn't exist
def download_common_passwords():
    if not os.path.exists(local_file_path):
        print("Downloading common passwords file...")
        response = requests.get(DROPBOX_FILE_URL)
        with open(local_file_path, 'wb') as file:
            file.write(response.content)
        print("Common passwords file downloaded.")
    else:
        print("Common passwords file already exists.")

# Load common passwords into memory once
def load_common_passwords(filepath):
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="latin-1") as file:
                passwords = set(file.read().splitlines())  # Use a set for fast lookups
                if passwords:
                    print(f"Successfully loaded {len(passwords)} passwords.")
                else:
                    print("The common passwords file is empty.")
                return passwords
        except UnicodeDecodeError:
            print("Unable to read the common passwords list due to encoding issues.")
    else:
        print("Common passwords file does not exist.")
    return set()

# Function to check password strength and update the UI
def check_password_strength(password, common_passwords):
    score = 0
    feedback = []

    # Normalize the password to lowercase for comparison
    password = password.strip()

    # Priority check: Is the password too common?
    if password.lower() in common_passwords:
        feedback.append({"message": "Your password is too common. Avoid using it!", "style": "bad"})
        return {"strength": "Weak", "strength_style": "red", "score": 0, "feedback": feedback}

    # Password length check
    if len(password) >= 10:
        score += 2
        feedback.append({"message": "Password length is strong.", "style": "good"})
    elif 8 <= len(password) < 10:
        score += 1
        feedback.append({"message": "Password length is acceptable but could be longer.", "style": "acceptable"})
    else:
        feedback.append({"message": "Password is too short. Use at least 10 characters.", "style": "bad"})

    # Check for uppercase and lowercase letters
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)

    if has_upper and has_lower:
        score += 1
        feedback.append({"message": "Includes both lowercase and uppercase letters.", "style": "good"})
    else:
        if not has_upper:
            feedback.append({"message": "Add uppercase letters.", "style": "bad"})
        if not has_lower:
            feedback.append({"message": "Add lowercase letters.", "style": "bad"})

    # Check for numbers
    if re.search(r'\d', password):
        score += 1
        feedback.append({"message": "Includes numbers.", "style": "good"})
    else:
        feedback.append({"message": "Add some numbers.", "style": "bad"})

    # Check for special characters
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 1
        feedback.append({"message": "Includes special characters.", "style": "good"})
    else:
        feedback.append({"message": "Add special characters for a stronger password.", "style": "bad"})

    # Determine overall strength
    if score >= 5:
        strength = "Strong"
        strength_style = "green"
    elif score >= 3:
        strength = "Medium"
        strength_style = "orange"
    else:
        strength = "Weak"
        strength_style = "red"

    return {"strength": strength, "strength_style": strength_style, "score": score, "feedback": feedback}

# Check for updates when the app starts
def check_for_updates():
    try:
        response = requests.get(GITHUB_VERSION_URL)
        response.raise_for_status()

        latest_version = response.text.strip()

        if latest_version != LOCAL_VERSION:
            print(f"A new version ({latest_version}) is available! Current version: {LOCAL_VERSION}")
            download_update()
        else:
            print("You are using the latest version.")
    except requests.exceptions.RequestException as e:
        print(f"Error checking for updates: {e}")

# Download update if a new version is available
def download_update():
    print("Downloading the latest version...")
    response = requests.get(GITHUB_ZIP_URL)

    if response.status_code == 200:
        with open("latest_version.zip", "wb") as file:
            file.write(response.content)
        print("Update downloaded! Extract the contents to update.")
        extract_update()
    else:
        print(f"Failed to download the update. Status code: {response.status_code}")

# Extract the downloaded zip for the update
def extract_update():
    print("Extracting the update...")
    with zipfile.ZipFile("latest_version.zip", 'r') as zip_ref:
        zip_ref.extractall("Password Strength Analyzer")
    print("Update extracted successfully.")

# Download common passwords
download_common_passwords()

# Load common passwords into memory
common_passwords = load_common_passwords(local_file_path)

# Create the main window
root = tk.Tk()
root.title("Password Strength Analyzer")
root.geometry("600x500")
root.resizable(True, True)

# Styling for fonts
title_font = ('Helvetica', 18, 'bold')
label_font = ('Helvetica', 12)
feedback_font = ('Helvetica', 12)
strength_font = ('Helvetica', 16, 'bold')

# Add a title label
title_label = tk.Label(root, text="Password Strength Analyzer", font=title_font, fg="#333")
title_label.pack(pady=20)

# Password input field
password_label = tk.Label(root, text="Enter Password:", font=label_font, fg="#333")
password_label.pack(pady=10)
password_entry = tk.Entry(root, show="*", font=label_font, width=35, bd=2, relief="solid", highlightthickness=2)
password_entry.pack(padx=15, pady=5)

# Result label for password strength
result_label = tk.Label(root, text="Strength: ", font=strength_font, fg="#333")
result_label.pack(pady=15)

# Feedback area for suggestions
feedback_frame = tk.Frame(root)
feedback_frame.pack(pady=20)

# Function to check password strength and update UI
def check_strength(event=None):
    password = password_entry.get()

    for widget in feedback_frame.winfo_children():
        widget.destroy()

    if not password.strip():
        result_label.config(text="Strength: N/A", fg="red")
        feedback_label = tk.Label(feedback_frame, text="Password cannot be empty.", font=feedback_font, fg="red")
        feedback_label.pack(anchor="w", pady=5)
        return

    result = check_password_strength(password, common_passwords)
    strength = result['strength']
    feedback = result['feedback']

    if strength == "Strong":
        strength_color = "green"
    elif strength == "Medium":
        strength_color = "orange"
    else:
        strength_color = "red"

    result_label.config(text=f"Strength: {strength}", fg=strength_color)

    for item in feedback:
        message = item['message']
        style = item['style']
        feedback_color = "green" if style == "good" else "orange" if style == "acceptable" else "red"
        feedback_label = tk.Label(feedback_frame, text=message, font=feedback_font, fg=feedback_color)
        feedback_label.pack(anchor="w", pady=5)

# Bind the event to check password strength
password_entry.bind("<KeyRelease>", check_strength)
password_entry.bind("<Return>", check_strength)

# Footer with version info
footer_label = tk.Label(root, text=f"Password Strength Analyzer v{LOCAL_VERSION}", font=('Helvetica', 8), fg="#777")
footer_label.pack(side="bottom", pady=10)

# Start the Tkinter event loop
root.mainloop()
