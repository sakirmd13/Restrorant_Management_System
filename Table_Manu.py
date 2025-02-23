import datetime

TOTAL_TABLES = 15
tables = {
    1:  {"status": "Available", "seats": 1, "bookings": {}},
    2:  {"status": "Available", "seats": 1, "bookings": {}},
    3:  {"status": "Available", "seats": 1, "bookings": {}},
    4:  {"status": "Available", "seats": 2, "bookings": {}},
    5:  {"status": "Available", "seats": 2, "bookings": {}},
    6:  {"status": "Available", "seats": 2, "bookings": {}},
    7:  {"status": "Available", "seats": 2, "bookings": {}},
    8:  {"status": "Available", "seats": 4, "bookings": {}},
    9:  {"status": "Available", "seats": 4, "bookings": {}},
    10: {"status": "Available", "seats": 4, "bookings": {}},
    11: {"status": "Available", "seats": 4, "bookings": {}},
    12: {"status": "Available", "seats": 4, "bookings": {}},
    13: {"status": "Available", "seats": 4, "bookings": {}},
    14: {"status": "Available", "seats": 4, "bookings": {}},
    15: {"status": "Available", "seats": 4, "bookings": {}},
}

def show_status():
    print("\nTable Status:")
    for table, info in tables.items():
        print(f" Table {table}: {info['status']}")

def show_table_seats():
    print("\nTable & Seat Count:")
    for table, info in tables.items():
        print(f" Table {table}: {info['seats']} seats ({info['status']})")

def book_table(table_number):
    if table_number in tables:
        if tables[table_number]["status"] == "Available":
            tables[table_number]["status"] = "Booked"
            print(f" Table {table_number} booked successfully!")
        else:
            print(f" Table {table_number} is already booked.")
    else:
        print(" Invalid table number!")

def empty_table(table_number):
    if table_number in tables and tables[table_number]["status"] == "Booked":
        tables[table_number]["status"] = "Available"
        print(f" Table {table_number} is now available.")
    else:
        print(f" Table {table_number} is already available or invalid!")

def get_valid_number(user_input):
    try:
        num = int(input(user_input))
        return num if 1 <= num <= TOTAL_TABLES else None
    except ValueError:
        return None

def book_table_advanced(table_number, date, time):
    if table_number in tables:
        datetime_key = f"{date} {time}"
        if datetime_key not in tables[table_number]["bookings"]:
            tables[table_number]["bookings"][datetime_key] = "Booked"
            print(f" Table {table_number} booked successfully for {date} at {time}!")
        else:
            print(f" Table {table_number} is already booked for {date} at {time}.")
    else:
        print(" Invalid table number!")

def get_valid_date():
    date_str = input(" Enter date (YYYY-MM-DD): ").strip()
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except ValueError:
        print(" Invalid date format!")
        return None

def get_valid_time():
    time_str = input(" Enter time (HH:MM, 24-hour format): ").strip()
    try:
        datetime.datetime.strptime(time_str, "%H:%M")
        return time_str
    except ValueError:
        print(" Invalid time format!")
        return None

while True:
    choice = input("\n1️ Show Status\n2️ Show Table Seats\n3️ Book Table\n4️ Book Table (Advanced)\n5️ Empty Table\n6️ Exit\nEnter choice: ").strip()
    
    if choice == "1":
        show_status()
    elif choice == "2":
        show_table_seats()
    elif choice == "3":
        table_number = get_valid_number("Enter table number: ")
        if table_number:
            book_table(table_number)
        else:
            print(" Invalid table number!")
    elif choice == "4":
        table_number = get_valid_number("Enter table number: ")
        date = get_valid_date()
        time = get_valid_time()
        if table_number and date and time:
            book_table_advanced(table_number, date, time)
        else:
            print(" Invalid input!")
    elif choice == "5":
        table_number = get_valid_number("Enter table number: ")
        if table_number:
            empty_table(table_number)
        else:
            print(" Invalid table number!")
    elif choice == "6":
        print(" Exiting... Thank you!")
        break
    else:
        print(" Invalid choice, try again!")
