import datetime
from itertools import combinations

TOTAL_TABLES = 15
OPERATING_HOURS = (10, 22)  

tables = {i: {"status": "Available", "seats": 1 if i <= 3 else 2 if i <= 7 else 4, "bookings": {}} for i in range(1, TOTAL_TABLES + 1)}

def display_tables():
    print("\nTABLE STATUS\n-----------------")
    for i, table in tables.items():
        print(f"Table {i}: {table['status']}")
        for booking_time, duration in table["bookings"].items():
            try:
                day_of_week = datetime.datetime.strptime(booking_time, '%Y-%m-%d %H:%M').strftime('%A')
                print(f"  - Booked on {booking_time} ({day_of_week}) for {duration} hours")
            except ValueError:
                print(f"  - Invalid booking time format: {booking_time}")

def find_best_table_combination(people_count, available_tables):
    available = {t: tables[t]["seats"] for t in available_tables}
    if not available:
        return []
    best_combos = sorted((comb for r in range(1, min(4, len(available) + 1)) for comb in combinations(available.keys(), r)),
                          key=lambda x: abs(sum(available[t] for t in x) - people_count))
    return best_combos

def get_valid_input(prompt, min_val, max_val, dtype=int):
    while True:
        try:
            value = dtype(input(prompt).strip())
            if min_val <= value <= max_val:
                return value
            print(f"Invalid! Enter a value between {min_val} and {max_val}.")
        except ValueError:
            print("Invalid input! Please enter a valid number.")

def check_availability(date, time):
    try:
        hour = int(time.split(":")[0])
        if hour < OPERATING_HOURS[0] or hour >= OPERATING_HOURS[1]:
            print("Invalid time! Restaurant operates from 10 AM to 10 PM.")
            return []
    except ValueError:
        print("Invalid time format! Please enter time in HH:MM format.")
        return []
    
    datetime_key = f"{date} {time}"
    available_tables = [t for t in tables if datetime_key not in tables[t]["bookings"]]
    return available_tables

def book_tables():
    people_count = get_valid_input("Enter number of people (1 to 43): ", 1, 43)
    while True:
        date = input("Enter date (YYYY-MM-DD): ").strip()
        time = input("Enter time (HH:MM, 24-hour format): ").strip()
        available_tables = check_availability(date, time)

        if not available_tables:
            print("No tables available at this time. Suggested time slots:")
            for hour in range(OPERATING_HOURS[0], OPERATING_HOURS[1]):
                suggested_time = f"{hour:02d}:00"
                if check_availability(date, suggested_time):
                    print(f"- {date} at {suggested_time}")
            continue

        best_combos = find_best_table_combination(people_count, available_tables)
        if not best_combos:
            print("No suitable table combinations available.")
            return

        for combo in best_combos:
            choice = input(f"Book tables {', '.join(map(str, combo))}? (yes/no/exit): ").strip().lower()
            if choice == "yes":
                duration = get_valid_input("Enter duration in hours (1 to 24): ", 1, 24)
                datetime_key = f"{date} {time}"
                
                for table in combo:
                    tables[table]["bookings"][datetime_key] = duration
                    tables[table]["status"] = "Booked"
                
                print(f"Tables {', '.join(map(str, combo))} booked for {date} at {time} for {duration} hours!")
                return
            elif choice == "exit":
                print("Exiting booking process...")
                return
        print("No more suitable tables available. Exiting...")

def release_table():
    table_number = get_valid_input("Enter table number to release (1-15): ", 1, TOTAL_TABLES)
    if tables[table_number]["status"] == "Booked":
        tables[table_number].update({"status": "Available", "bookings": {}})
        print(f"Table {table_number} is now available.")
    else:
        print(f"Table {table_number} is already available.")

def cancel_booking():
    table_number = get_valid_input("Enter table number to cancel booking (1-15): ", 1, TOTAL_TABLES)
    if tables[table_number]["bookings"]:
        print("Current bookings:")
        bookings = list(tables[table_number]["bookings"].items())
        for index, (booking_time, duration) in enumerate(bookings, start=1):
            print(f"{index}. {booking_time} for {duration} hours")
        choice = get_valid_input("Enter the booking number to cancel: ", 1, len(bookings))
        
        selected_booking = bookings[choice - 1][0]
        del tables[table_number]["bookings"][selected_booking]
        
        if not tables[table_number]["bookings"]:
            tables[table_number]["status"] = "Available"
        
        print(f"Booking on {selected_booking} canceled.")
    else:
        print(f"Table {table_number} has no bookings.")

while True:
    display_tables()
    choice = input("\n1️ Show Available Tables\n2️ Book Table\n3️ Release Table\n4️ Cancel Booking\n5️ Exit\nEnter choice: ").strip()
    if choice == "1":
        best_combos = find_best_table_combination(get_valid_input("Enter number of people (1 to 43): ", 1, 43), list(tables.keys()))
        print(f"Best available table combinations: {best_combos if best_combos else 'None'}")
    elif choice == "2":
        book_tables()
    elif choice == "3":
        release_table()
    elif choice == "4":
        cancel_booking()
    elif choice == "5":
        print("Exiting... Thank you!")
        break
    else:
        print("Invalid choice, try again!")
