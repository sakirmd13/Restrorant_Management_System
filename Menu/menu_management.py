import json
import os

class Menu:
    def __init__(self):
        self.menu = {
            "Breakfast": [],
            "Lunch": [],
            "Dinner": [],
            "Beverages": []
        }
        self.load_menu()

    def load_menu(self):
        if os.path.exists("Menu.json"):
            try:
                with open("Menu.json", "r") as file:
                    data = file.read()
                    if data:
                        self.menu = json.loads(data)
                    else:
                        self.save_menu()
            except:
                self.save_menu()
        else:
            self.save_menu()

    def save_menu(self):
        with open("Menu.json", "w") as file:
            json.dump(self.menu, file, indent=4)

    def display_menu(self):
        print("\n--- Menu ---")
        for category in self.menu:
            print(f"\n{category}:")
            if not self.menu[category]:
                print("No items available.")
            else:
                count = 1
                for item in self.menu[category]:
                    print(f"{count}. {item['item_name']} - ${item['item_price']}")
                    count += 1

    def add_item(self, category):
        item_name = input(f"Enter item name for {category}: ")
        item_price = input(f"Enter price for {item_name}: ")
        self.menu[category].append({"item_name": item_name, "item_price": item_price})
        self.save_menu()
        print(f"{item_name} added to {category}.")

def main():
    menu = Menu()

    while True:
        print("\nMenu Management System")
        print("1. Display Menu")
        print("2. Add Items")
        print("3. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            menu.display_menu()

        elif choice == '2':
            print("\nSelect Category")
            print("1. Breakfast")
            print("2. Lunch")
            print("3. Dinner")
            print("4. Beverages")
            print("5. Go Back")
            option = input("Enter choice: ")

            if option == '1':
                menu.add_item("Breakfast")
            elif option == '2':
                menu.add_item("Lunch")
            elif option == '3':
                menu.add_item("Dinner")
            elif option == '4':
                menu.add_item("Beverages")
            elif option == '5':
                continue
            else:
                print("Invalid choice. Try again.")

        elif choice == '3':
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
