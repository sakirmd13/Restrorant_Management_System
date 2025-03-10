import json
import os
import getpass
import datetime  # For logging timestamps

# Define database folder and files
DATABASE_FOLDER = "SRC/DATABASE"
USER_FILE = os.path.join(DATABASE_FOLDER, "users.json")
LOG_FILE = os.path.join(DATABASE_FOLDER, "auth.log")

# Ensure the database folder exists
if not os.path.exists(DATABASE_FOLDER):
    os.makedirs(DATABASE_FOLDER)

# Ensure the user file exists
if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w") as file:
        json.dump({}, file)

# Logging function
def log_activity(action, username, status):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {action} - User: {username} - Status: {status}\n"
    with open(LOG_FILE, "a") as log_file:
        log_file.write(log_entry)

# Load user data
def load_users():
    try:
        with open(USER_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {}  # If JSON is corrupted, return an empty dictionary

# Save user data
def save_users(users):
    with open(USER_FILE, "w") as file:
        json.dump(users, file, indent=4)

# Sign-up function
def sign_up():
    users = load_users()
    
    username = input("Enter username: ").strip()
    if username in users:
        print("❌ Username already exists. Try logging in.")
        log_activity("Sign-up", username, "Failed (Username Exists)")
        return

    # Password entry with confirmation
    while True:
        password1 = getpass.getpass("Enter your password: ")
        password2 = getpass.getpass("Confirm your password: ")

        if password1 == password2:
            break
        else:
            print("⚠ Passwords do not match! Please try again.")

    # Assign "admin" role only to Md Sakir
    role = "admin" if username.lower() == "md sakir" else "user"

    # Store user data
    users[username] = {"password": password1, "role": role}
    save_users(users)
    
    print(f"✅ Sign-up successful! You are registered as a {role}.")
    log_activity("Sign-up", username, "Successful")

# Login function
def login():
    users = load_users()
    
    username = input("Enter username: ").strip()
    password = getpass.getpass("Enter password: ")
    
    if username in users and users[username]["password"] == password:
        role = users[username]["role"]
        print(f"✅ Login successful! Welcome, {username} 🎉")

        if role == "admin":
            print("🔹 You have **ADMIN** privileges. 🚀")
        log_activity("Login", username, "Successful")
    else:
        print("❌ Invalid username or password.")
        log_activity("Login", username, "Failed (Invalid Credentials)")

# Main loop
while True:
    choice = input("\nChoose an option: \n1️⃣ Sign-up \n2️⃣ Login\n3️⃣ Exit\nEnter choice: ").strip()
    
    if choice == "1":
        sign_up()
    elif choice == "2":
        login()
    elif choice == "3":
        print("👋 Exiting... Have a great day!")
        break
    else:
        print("❌ Invalid choice. Please enter 1, 2, or 3.")
