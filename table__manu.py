import json
import os
import datetime
from itertools import combinations

TOTAL_TABLES = 15
OPERATING_HOURS = (10, 22)
DATA_FILE = "tables_data.json"

# Initialize tables with seating capacity
def initialize_tables():
    return {str(i): {"seats": 1 if i <= 3 else 2 if i <= 7 else 4, "bookings": {}} for i in range(1, TOTAL_TABLES + 1)}

# Load data from file
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("⚠ Error: Corrupt data file! Initializing fresh data.")
            return {"tables": initialize_tables()}
    return {"tables": initialize_tables()}

# Save data to file
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Auto-release past bookings
def auto_release_tables(data):
    today = datetime.datetime.now().date()
    for table in data["tables"].values():
        expired_dates = [date for date in table["bookings"] if datetime.datetime.strptime(date, '%Y-%m-%d').date() < today]
        for date in expired_dates:
            table["bookings"].pop(date, None)
    save_data(data)

data = load_data()
auto_release_tables(data)

# Display table status
def display_tables():
    print("\n📌 **TABLE STATUS** 📌\n-------------------------")
    for table_id, table in data["tables"].items():
        status = "Available" if not table["bookings"] else "Booked"
        print(f"Table {table_id} ({table['seats']} seats): {status}")
    print("\n")

# Check available tables
def check_availability(date, time):
    return [table_id for table_id, table in data["tables"].items() if date not in table["bookings"] or time not in table["bookings"][date]]

# Find the best table combination for given people count
def find_best_table_combination(people_count, available_tables):
    table_seats = {table_id: data["tables"][table_id]["seats"] for table_id in available_tables}
    for size in range(1, len(available_tables) + 1):
        for combo in combinations(available_tables, size):
            if sum(table_seats[table] for table in combo) >= people_count:
                return combo
    return None

# Validate integer input
def get_valid_input(prompt, min_val, max_val):
    while True:
        try:
            user_input = input(prompt).strip()
            if user_input.lower() == "cancel":
                return None
            value = int(user_input)
            if min_val <= value <= max_val:
                return value
            print(f"❌ Enter a number between {min_val} and {max_val}!")
        except ValueError:
            print("❌ Invalid input! Please enter a number.")

# Book a table
def book_tables():
    people_count = get_valid_input("Enter number of people (1 to 43): ", 1, 43)

    while True:
        date, day = get_valid_date("Enter date (YYYY-MM-DD, or 'cancel' to go back): ")
        if date is None:
            return

        time = get_valid_time("Enter time (HH:MM, 24-hour format, or 'cancel' to go back): ")
        if time is None:
            return

        available_tables = check_availability(date, time)

        if not available_tables:
            print("❌ No tables available at this time! Try another time.")
            continue

        best_combo = find_best_table_combination(people_count, available_tables)
        if not best_combo:
            print("❌ No suitable tables found! Try another time.")
            continue

        choice = input(f"Do you want to book Table {', '.join(best_combo)} on {day}? (yes/no/cancel): ").strip().lower()
        if choice == "cancel":
            return
        if choice != "yes":
            continue

        duration = get_valid_input("For how many hours? (1 to 12): ", 1, 12)
        end_time = (datetime.datetime.strptime(f"{date} {time}", '%Y-%m-%d %H:%M') + datetime.timedelta(hours=duration)).strftime('%H:%M')

        for table in best_combo:
            data["tables"][table]["bookings"].setdefault(date, {})[time] = {"duration": duration, "end_time": end_time, "day": day}

        save_data(data)
        print(f"✅ Table {', '.join(best_combo)} booked on {day} ({date}) from {time} for {duration} hours!")
        return

# Release a table
def release_table():
    table_number = get_valid_input("Enter table number to release (1-15, or 'cancel' to go back): ", 1, TOTAL_TABLES)
    if table_number is None:
        return

    table_key = str(table_number)

    if data["tables"][table_key]["bookings"]:
        data["tables"][table_key]["bookings"].clear()
        save_data(data)
        print(f"✅ Table {table_number} is now available!")
    else:
        print(f"⚠ Table {table_number} has no bookings!")

# Cancel a specific booking
def cancel_booking():
    table_number = get_valid_input("Enter table number to cancel booking (1-15, or 'cancel' to go back): ", 1, TOTAL_TABLES)
    if table_number is None:
        return

    table_key = str(table_number)
    if not data["tables"][table_key]["bookings"]:
        print(f"⚠ Table {table_number} has no bookings!")
        return

    date, _ = get_valid_date("Enter date of booking to cancel (YYYY-MM-DD, or 'cancel' to go back): ")
    if date is None or date not in data["tables"][table_key]["bookings"]:
        print("❌ No booking found for this date!")
        return

    time = get_valid_time("Enter time to cancel booking (HH:MM, or 'cancel' to go back): ")
    if time is None or time not in data["tables"][table_key]["bookings"][date]:
        print("❌ No booking found for this time!")
        return

    del data["tables"][table_key]["bookings"][date][time]

    if not data["tables"][table_key]["bookings"][date]:
        del data["tables"][table_key]["bookings"][date]

    save_data(data)
    print(f"✅ Booking for Table {table_number} on {date} at {time} has been cancelled!")

# Validate date input
def get_valid_date(prompt):
    while True:
        try:
            date_str = input(prompt).strip()
            if date_str.lower() == "cancel":
                return None, None
            input_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            if input_date >= datetime.date.today():
                return date_str, input_date.strftime("%A")
            print("❌ Enter today's or future date only!")
        except ValueError:
            print("❌ Invalid format! Use YYYY-MM-DD.")

# Validate time input
def get_valid_time(prompt):
    while True:
        try:
            time_str = input(prompt).strip()
            if time_str.lower() == "cancel":
                return None
            hour, minute = map(int, time_str.split(":"))
            if 0 <= minute < 60 and OPERATING_HOURS[0] <= hour < OPERATING_HOURS[1]:
                return time_str
            print("❌ Enter time within operating hours!")
        except ValueError:
            print("❌ Invalid format! Use HH:MM.")

# Main menu
while True:
    choice = input("\n1. Show Tables\n2. Book Table\n3. Release Table\n4. Cancel Booking\n5. Exit\nEnter choice: ").strip()
    if choice == "1":
        display_tables()
    elif choice == "2":
        book_tables()
    elif choice == "3":
        release_table()
    elif choice == "4":
        cancel_booking()
    elif choice == "5":
        break
    else:
        print("❌ Invalid choice! Try again.")
