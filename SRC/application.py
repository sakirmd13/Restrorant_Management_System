from Authentication.signup import sign_up
from Authentication.signin import sign_in
from Authentication.Domain.Menu.menu import load_menu, display_menu, remove_menu_item, add_menu_item
from Authentication.Domain.Order.order import place_order, cancel_order, view_ongoing_orders
from Authentication.Domain.Billing.billing import generate_bill
from Authentication.Domain.Table.table import cancel_booking, release_table, display_tables, load_data, book_tables
import maskpass
import json
import datetime
import logging
import os

# Configure logging
path = os.getcwd()
LOG_FOLDER = os.path.join(path,'SRC','Logs','Application_log.txt')

if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)

log_file = os.path.join(LOG_FOLDER, 'application.log')
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,  # Log everything (DEBUG and above)
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def admin_main():
    data = load_data()

    while True:
        # Main menu for choosing Admin or Customer
        print("\nWelcome to the Restaurant Management System")
        print("1. Admin")
        print("2. Customer")
        print("3. Exit")
        choice = input("Please enter your choice (1/2/3): ")

        if choice == '1':  # Admin section
            print("\n--- Admin Panel ---")
            print("1. Sign Up")
            print("2. Sign In")
            admin_choice = input("Please select an option (1/2): ")

            if admin_choice == '1':  # Admin sign-up
                try:
                    name = input("Enter your name: ")
                    age = input("Enter your age: ")
                    worktype = input("Enter your worktype: ")
                    password = input("Enter your Password: ")

                    sign_up(password, name, age, worktype)
                    logging.info(f"Admin signed up successfully with name: {name}, worktype: {worktype}")
                except Exception as e:
                    logging.error(f"Error during admin sign-up: {e}")
                    print("\033[91mAn error occurred during sign-up. Please check the log file.\033[0m")

            elif admin_choice == '2':  # Admin sign-in
                admin_id = input("Enter your Admin ID: ")
                password = maskpass.askpass('Enter your password: ', mask='*')  

                if sign_in(admin_id, password):
                    logging.info(f"Admin {admin_id} signed in successfully.")
                    print("\n--- Admin Dashboard ---")
                    menu = load_menu()
                    orders = []  # Initialize empty orders list

                    while True:
                        print("1. Add Menu Item")
                        print("2. Remove Menu Item")
                        print("3. View Ongoing Orders")
                        print("4. Cancel Order")
                        print("5. Cancel Table")
                        print("6. Logout")
                        admin_action = input("Select action: ")

                        if admin_action == '1':
                            add_menu_item()
                            logging.info("Added a menu item.")
                        elif admin_action == '2':
                            remove_menu_item(menu)
                            logging.info("Removed a menu item.")
                        elif admin_action == '3':
                            view_ongoing_orders()
                            logging.info("Viewed ongoing orders.")
                        elif admin_action == '4':
                            # Load orders from the file before canceling
                            date_today = datetime.datetime.now().strftime("%Y-%m-%d")
                            filename = f"{date_today}_orders.json"
                            try:
                                with open(filename, "r") as file:
                                    orders = json.load(file)
                                    cancel_order(orders)  # Allow admin to cancel orders
                                    logging.info(f"Cancelled orders from {filename}.")
                            except FileNotFoundError:
                                logging.warning("No orders found to cancel.")
                                print("No orders found to cancel.")
                        elif admin_action == '5':
                            cancel_booking()  # Function to cancel a table booking
                            logging.info("Cancelled a table booking.")
                        elif admin_action == '6':
                            print("Logged out successfully.")
                            logging.info(f"Admin {admin_id} logged out.")
                            break
                        else:
                            print("\033[91mInvalid choice. Please try again.\033[0m")

                else:
                    logging.warning(f"Failed sign-in attempt for Admin ID: {admin_id}")
                    print("\033[91mFailed to sign in. Please check your credentials.\033[0m")

        elif choice == '2':  # Customer section
            print("\n--- Customer Panel ---")
            menu = load_menu()
            orders = []  # Initialize empty orders list

            while True:
                print("\n1. Display Menu")
                print("2. Place Order")
                print("3. Display Tables")
                print("4. Book Table")
                print("5. Ongoing Orders")
                print("6. Generate Bill")
                print("7. Release Table")
                print("0. Exit")
                customer_choice = input("Please select an option: ")

                if customer_choice == '1':  # Display Menu
                    display_menu(menu)
                    logging.info("Displayed the menu to the customer.")
                elif customer_choice == '2':  # Place order
                    orders = place_order(menu)
                    logging.info(f"Customer placed an order: {orders}")
                elif customer_choice == '3':  # Display tables
                    display_tables(data)  # Pass the data to display_tables function
                    logging.info("Displayed the available tables.")
                elif customer_choice == '4':  # Book table
                    book_tables()
                    logging.info("Customer booked a table.")
                elif customer_choice == '5':  # View ongoing orders
                    view_ongoing_orders()
                    logging.info("Customer viewed ongoing orders.")
                elif customer_choice == '6':  # Generate bill
                    generate_bill(orders)  # Calls the modified generate_bill function
                    logging.info(f"Generated a bill for orders: {orders}")
                elif customer_choice == '7':  # Release table
                    release_table()
                    logging.info("Released a table.")
                
                elif customer_choice == '0':  # Exit customer panel
                    print("\033[95mThank you for visiting. Goodbye!\033[0m")
                    logging.info("Customer exited the system.")
                    break

        elif choice == '3':  # Exit program
            print("\033[95mExiting the system. Goodbye!\033[0m")
            logging.info("System exited.")
            break

admin_main()
