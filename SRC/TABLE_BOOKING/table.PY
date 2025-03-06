import json
import os
import datetime
import uuid
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

# Generate unique booking ID
def generate_booking_id():
    return str(uuid.uuid4())[:8]

# Get valid integer input
def get_valid_input(prompt, min_value, max_value):
    while True:
        try:
            value = int(input(prompt).strip())
            if min_value <= value <= max_value:
                return value
            print(f"❌ Enter a number between {min_value} and {max_value}!")
        except ValueError:
            print("❌ Invalid input! Enter a valid number.")

# Get valid date within allowed range
# Get valid date within allowed range
def get_valid_date(prompt):
    today = datetime.datetime.now().date()
    max_date = today + datetime.timedelta(days=30)  # One month ahead

    while True:
        user_input = input(prompt).strip()
        if user_input.lower() == "cancel":
            return None, None
        try:
            date_obj = datetime.datetime.strptime(user_input, "%Y-%m-%d").date()
            if today <= date_obj <= max_date:
                return user_input, date_obj.strftime("%A")
            else:
                print(f"❌ You can only book from {today} to {max_date}!")
        except ValueError:
            print("❌ Invalid date format! Use YYYY-MM-DD.")


# Get valid time
def get_valid_time(prompt):
    while True:
        user_input = input(prompt).strip()
        if user_input.lower() == "cancel":
            return None
        try:
            hour, minute = map(int, user_input.split(":"))
            if OPERATING_HOURS[0] <= hour < OPERATING_HOURS[1]:
                return f"{hour:02d}:{minute:02d}"
            print(f"❌ Time must be between {OPERATING_HOURS[0]}:00 and {OPERATING_HOURS[1]}:00!")
        except ValueError:
            print("❌ Invalid time format! Use HH:MM (24-hour format).")

# Check table availability
def check_availability(date, time):
    available = []
    for table_id, table in data["tables"].items():
        if date not in table["bookings"] or time not in table["bookings"][date]:
            available.append(table_id)
    return available

# Find best table combination
def find_best_table_combination(people_count, available_tables):
    seat_map = {t_id: data["tables"][t_id]["seats"] for t_id in available_tables}
    exact_match = [t for t in available_tables if seat_map[t] == people_count]
    
    if exact_match:
        return exact_match[:1]  # Prioritize exact match
    
    # Try to find a combination of tables to fit people
    for size in range(1, len(available_tables) + 1):
        for combo in combinations(available_tables, size):
            if sum(seat_map[t] for t in combo) >= people_count:
                return combo
    
    return None

# Display tables
def display_tables():
    print("\nCurrent Table Status:")
    for table_id, table in data["tables"].items():
        print(f"Table {table_id} - Seats: {table['seats']} - Bookings: {len(table['bookings'])}")

# Show available dates
def show_available_dates():
    print("\nAvailable Booking Dates:")
    today = datetime.datetime.now().date()
    max_date = today + datetime.timedelta(days=30)

    for date in (today + datetime.timedelta(days=i) for i in range((max_date - today).days + 1)):
        print(date.strftime("%Y-%m-%d"))

# Book a table
def book_tables():
    name = input("Enter your name: ").strip()
    if not name:
        print("❌ Name cannot be empty!")
        return
    
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

        duration = get_valid_input("For how many hours? (1 to 12): ", 1, 12)
        end_time = (datetime.datetime.strptime(f"{date} {time}", '%Y-%m-%d %H:%M') + datetime.timedelta(hours=duration)).strftime('%H:%M')
        booking_id = generate_booking_id()

        for table in best_combo:
            data["tables"][table]["bookings"].setdefault(date, {})[time] = {"name": name, "booking_id": booking_id, "duration": duration, "end_time": end_time, "day": day, "people_count": people_count}
        
        save_data(data)
        print(f"✅ Table {', '.join(best_combo)} booked under '{name}' for {people_count} people with Booking ID: {booking_id} on {day} ({date}) from {time} for {duration} hours!")
        return
def search_booking():
    query = input("Enter Name or Booking ID: ").strip().lower()
    found = False
    
    for table_id, table in data["tables"].items():
        for date, bookings in table["bookings"].items():
            for time, details in bookings.items():
                if details["name"].lower() == query or details["booking_id"] == query:
                    found = True
                    print(f"\n🔍 Booking Found: \nTable: {table_id}, Date: {date}, Time: {time}, Name: {details['name']}, Booking ID: {details['booking_id']}, People: {details['people_count']}\n")
    
    if not found:
        print("❌ No booking found!")
def show_bookings_by_date():
    if not any(table["bookings"] for table in data["tables"].values()):
        print("📅 No bookings available!")
        return
    
    print("\n📅 Table Bookings by Date:\n")
    sorted_dates = sorted({date for table in data["tables"].values() for date in table["bookings"]})

    for date in sorted_dates:
        print(f"\n📅 {date}")
        for table_id, table in data["tables"].items():
            if date in table["bookings"]:
                for time, details in table["bookings"][date].items():
                    print(f"🪑 Table {table_id} - Time: {time} - Name: {details['name']} - People: {details['people_count']} - Booking ID: {details['booking_id']}")
def monthly_booking_report():
    today = datetime.datetime.now().date()
    month_end = today + datetime.timedelta(days=30)

    # Define week ranges
    week_ranges = {
        "1st Week": (today, today + datetime.timedelta(days=6)),
        "2nd Week": (today + datetime.timedelta(days=7), today + datetime.timedelta(days=13)),
        "3rd Week": (today + datetime.timedelta(days=14), today + datetime.timedelta(days=20)),
        "4th Week": (today + datetime.timedelta(days=21), month_end),
    }

    # Initialize counters
    weekly_bookings = {week: 0 for week in week_ranges}

    # Count bookings per week
    for table in data["tables"].values():
        for date_str in table["bookings"]:
            date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            for week, (start, end) in week_ranges.items():
                if start <= date_obj <= end:
                    weekly_bookings[week] += 1

    # Display report
    print("\n📊 **Monthly Booking Report**\n")
    for week, count in weekly_bookings.items():
        print(f"{week}: {count} bookings")

# Main menu
while True:
    choice = input("\n1. Show Tables\n2. Book Table\n3. Show Available Dates\n4. Search Booking\n5. Show bookings by date\n6. Monthly booking report\n7. Exit\nEnter choice: ").strip()
    if choice == "1":
        print("\nCurrent Table Status:")
        for table_id, table in data["tables"].items():
            print(f"Table {table_id} - Seats: {table['seats']} - Bookings: {len(table['bookings'])}")
    elif choice == "2":
        book_tables()
    elif choice == "3":
        show_available_dates()
    elif choice == "4":
        search_booking()
    elif choice == "5":
        show_bookings_by_date()
    elif choice == "6":
        monthly_booking_report()
    elif choice == "7":
        print ("THANK YOU FOR BOOKING")
        break
    else:
        print("❌ Invalid choice! Try again.")