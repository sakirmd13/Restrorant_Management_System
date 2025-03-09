import json
import datetime
import os
import logging
from Authentication.Domain.Menu.menu import display_menu  

database_folder = "C:/Users/Expert Solution/Desktop/New folder/SRC/Authentication/Database"


if not os.path.exists(database_folder):
    os.makedirs(database_folder)


path = os.getcwd()
LOG_FOLDER = os.path.join(path,'SRC','Logs','Application_log.txt')  # Path to log folder

if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)

log_file = os.path.join(LOG_FOLDER, 'order.log')
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,  
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def place_order(menu):
    """Allow customers to place an order."""
    orders = []  # Initialize orders as an empty list
    
    display_menu(menu)  # Display the menu for the user
    
    order_id = generate_order_id()  # Generate a unique order ID
    order_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get the current date and time
    
    while True:
        order_input = input("Enter the items you want to order : ")
        order_items = order_input.split(",")  # Split order input by commas
        
        for order_item in order_items:
            item_info = order_item.strip().lower()
            if '*' in item_info:
                # Process item with quantity
                item_name, quantity = item_info.split("*")
                try:
                    quantity = int(quantity)  # Convert quantity to integer
                except ValueError:
                    print(f"Invalid quantity for {item_name}. Skipping.")
                    logging.warning(f"Invalid quantity for item: {item_name}. Skipping.")
                    continue
            else:
                # Default quantity of 1 for items without quantity specified
                item_name, quantity = item_info, 1
            
            # Search for the item in the menu
            found = False
            for category in menu:  # Check all categories dynamically
                if category not in menu: 
                    continue  # Skip invalid categories

                for item in menu[category]:
                    if item['item_name'].lower() == item_name:
                        found = True
                        if 'half_plate_price' in item or 'full_plate_price' in item:
                            plate_choice = input(f"How many plates of {item['item_name']} would you like to order? (half/full): ").strip().lower()
                            if plate_choice == 'half' and 'half_plate_price' in item:
                                try:
                                    quantity_half = int(input(f"How many half plates of {item['item_name']} would you like to order? "))
                                    orders.append({
                                        "item_name": item['item_name'], 
                                        "price": item['half_plate_price'], 
                                        "quantity": quantity_half, 
                                        "order_id": order_id, 
                                        "order_time": order_time
                                    })
                                    logging.info(f"Added {quantity_half} half plates of {item['item_name']} to order {order_id}.")
                                except ValueError:
                                    print("Invalid input for quantity. Skipping.")
                                    logging.warning(f"Invalid quantity for half plates of {item['item_name']}. Skipping.")
                            elif plate_choice == 'full' and 'full_plate_price' in item:
                                try:
                                    quantity_full = int(input(f"How many full plates of {item['item_name']} would you like to order? "))
                                    orders.append({
                                        "item_name": item['item_name'], 
                                        "price": item['full_plate_price'], 
                                        "quantity": quantity_full, 
                                        "order_id": order_id, 
                                        "order_time": order_time
                                    })
                                    logging.info(f"Added {quantity_full} full plates of {item['item_name']} to order {order_id}.")
                                except ValueError:
                                    print("Invalid input for quantity. Skipping.")
                                    logging.warning(f"Invalid quantity for full plates of {item['item_name']}. Skipping.")
                            else:
                                print(f"Invalid plate option for {item['item_name']}. Skipping.")
                                logging.warning(f"Invalid plate option for item: {item['item_name']}. Skipping.")
                        else:
                            orders.append({
                                "item_name": item['item_name'], 
                                "price": item['item_price'], 
                                "quantity": quantity, 
                                "order_id": order_id, 
                                "order_time": order_time
                            })
                            logging.info(f"Added {quantity} of {item['item_name']} to order {order_id}.")
                        break
                if found:
                    break

            if not found:
                print(f"Item '{item_name}' not found in the menu. Skipping.")
                logging.warning(f"Item '{item_name}' not found in the menu. Skipping.")

        another_order = input("Would you like to add another item to your order? (y/n): ").strip().lower()
        if another_order != 'y':
            break

    save_order_to_file(orders)  # Save orders to the file
    return orders

def generate_order_id():
    """Generate a unique order ID."""
    date_today = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = os.path.join(database_folder, f"{date_today}_orders.json")

    order_number = 1  # Default starting order number
    
    try:
        with open(filename, "r") as file:
            existing_orders = json.load(file)
            existing_order_ids = [order['order_id'] for order in existing_orders]
            if existing_order_ids:
                max_order_number = max(int(order_id.replace("ORD", "")) for order_id in existing_order_ids)
                order_number = max_order_number + 1
    except FileNotFoundError:
        pass  # If the file doesn't exist, we start from order number 1
    
    order_id = f"ORD{order_number:04d}"  # Format the order ID with leading zeros
    logging.info(f"Generated order ID: {order_id}")
    return order_id

def save_order_to_file(orders):
    """Save order details to a JSON file."""
    date_today = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = os.path.join(database_folder, f"{date_today}_orders.json")
    
    try:
        # Read the existing orders from the file (if exists)
        try:
            with open(filename, "r") as file:
                existing_orders = json.load(file)
        except FileNotFoundError:
            existing_orders = []  # If file doesn't exist, initialize an empty list

        # Update the existing orders list
        existing_orders.extend(orders)  # Append new orders to the existing list

        # Save the updated list of orders to the file
        with open(filename, "w") as file:
            json.dump(existing_orders, file, indent=4)
        
        logging.info(f"Saved {len(orders)} order(s) to {filename}.")
        print(f"Order details saved to {filename}.")
        if orders:
            print(f"Your Order ID is: {orders[0]['order_id']}")  # Display the Order ID after saving
    except Exception as e:
        logging.error(f"Error saving order details: {e}")
        print(f"Error saving order details: {e}")

def cancel_order(orders):
    """Allow the customer to cancel an ongoing order."""
    if not orders:
        print("You have not placed any orders yet.")
        logging.info("No orders to cancel.")
        return orders

    while True:
        order_id = input("Enter the Order ID to cancel (or type 'back' to go back): ").strip()
        
        if order_id.lower() == 'back':
            break

        order_found = False
        for order in orders:
            if order['order_id'] == order_id:
                orders.remove(order)  # Remove the order from the in-memory list
                print(f"Order ID {order_id} has been canceled successfully.")
                logging.info(f"Order ID {order_id} has been canceled.")
                order_found = True
                break

        if order_found:
            save_order_to_file(orders)  # Save the updated orders list to the file
            break
        else:
            print("Order ID not found. Please try again.")
            logging.warning(f"Attempt to cancel non-existent Order ID: {order_id}.")

def view_ongoing_orders():
    """View ongoing orders placed by the user."""
    date_today = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = os.path.join(database_folder, f"{date_today}_orders.json")
    
    try:
        with open(filename, "r") as file:
            orders = json.load(file)
            if orders:
                print("\n--- Ongoing Orders ---")
                for order in orders:
                    print(f"Order ID: {order['order_id']}, Item: {order['item_name']} x{order['quantity']}, Price: {order['price'] * order['quantity']:.2f} (Time: {order['order_time']})")
                logging.info(f"Viewed ongoing orders from {filename}.")
            else:
                print("You have no ongoing orders.")
                logging.info("No ongoing orders to display.")
    except FileNotFoundError:
        print("No orders found.")
        logging.warning(f"No orders found in file: {filename}.")
