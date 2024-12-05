import os
import requests  # We need the requests library to download the file
import re

# Function to categorize feedback (green for good, orange for acceptable, red for bad)
def categorize_feedback(level):
    if level == "good":
        return "color: green;"
    elif level == "acceptable":
        return "color: orange;"
    else:
        return "color: red;"

# File URL for the common passwords file
dropbox_file_url = 'https://www.dropbox.com/scl/fi/b58abyc3cb063br2fyxgn/common_passwords.txt?rlkey=bkbg0puqtkda3mtuu0d6zrx4p&st=65kf0nro&dl=1'

# Download the common password file from Dropbox
def download_file(file_url, destination):
    response = requests.get(file_url)
    
    if response.status_code == 200:
        print("File downloaded successfully!")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")
    
    with open(destination, 'wb') as f:
        f.write(response.content)

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
    return set()  # Return an empty set if the file doesn't exist or fails to load

def check_password_strength(password, common_passwords):
    score = 0
    feedback = []

    # Normalize the password to lowercase for comparison
    password = password.strip()

    # Priority check: Is the password too common?
    if password.lower() in common_passwords:
        feedback.append({"message": "Your password is too common. Avoid using it!", "style": categorize_feedback("bad")})
        return {"strength": "Weak", "strength_style": categorize_feedback("bad"), "score": 0, "feedback": feedback}

    # Password length check
    if len(password) >= 12:
        score += 2
        feedback.append({"message": "Password length is strong.", "style": categorize_feedback("good")})
    elif 8 <= len(password) < 12:
        score += 1
        feedback.append({"message": "Password length is acceptable but could be longer.", "style": categorize_feedback("acceptable")})
    else:
        feedback.append({"message": "Password is too short. Use at least 12 characters.", "style": categorize_feedback("bad")})

    # Check for uppercase and lowercase letters
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)

    if has_upper and has_lower:
        score += 1
        feedback.append({"message": "Includes both lowercase and uppercase letters.", "style": categorize_feedback("good")})
    else:
        if not has_upper:
            feedback.append({"message": "Add uppercase letters.", "style": categorize_feedback("bad")})
        if not has_lower:
            feedback.append({"message": "Add lowercase letters.", "style": categorize_feedback("bad")})

    # Check for numbers
    if re.search(r'\d', password):
        score += 1
        feedback.append({"message": "Includes numbers.", "style": categorize_feedback("good")})
    else:
        feedback.append({"message": "Add some numbers.", "style": categorize_feedback("bad")})

    # Check for special characters
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 1
        feedback.append({"message": "Includes special characters.", "style": categorize_feedback("good")})
    else:
        feedback.append({"message": "Add special characters for a stronger password.", "style": categorize_feedback("bad")})

    # Determine overall strength
    if score >= 5:
        strength = "Strong"
        strength_style = categorize_feedback("good")
    elif score >= 3:
        strength = "Medium"
        strength_style = categorize_feedback("acceptable")
    else:
        strength = "Weak"
        strength_style = categorize_feedback("bad")

    return {"strength": strength, "strength_style": strength_style, "score": score, "feedback": feedback}
