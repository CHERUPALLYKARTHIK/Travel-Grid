import json

def passwordvad(password):
    if (
        len(password) >= 8 and len(password) <= 15 and
        any(c.islower() for c in password) and
        any(c.isupper() for c in password) and
        any(c.isdigit() for c in password) and
        any(c in "!@#$%^&*()_+" for c in password)
    ):
        return True
    return False

def register():
    print("Enter details for registration")
    username = input("Enter username: ")
    password = input("Enter password: (8-15 characters with uppercase, lowercase, digits, special symbols): ")

    if passwordvad(password):
        cpassword = input("Enter password to confirm: ")
        if password == cpassword:
            with open("user_data.txt", "a") as user_file:
                user_file.write(f"{username}:{password}\n")
            print("Registration successful")
            login()
        else:
            print("Passwords do not match")
    else:
        print("Invalid password. Follow password guidelines.")

def login():
    print("Enter details for login")
    username = input("Enter username: ")
    password = input("Enter password: ")

    with open("user_data.txt", "r") as user_file:
        for line in user_file:
            stored_username, stored_password = line.strip().split(":")
            if username == stored_username and password == stored_password:
                print("Login successful")
                tourist_guide()
                return
    print("Username does not exist or incorrect password")

def tourist_guide():
    print("Welcome to the Tourist Guide System")
    print("1. Register as a Tourist")
    print("2. Register as a Guide")
    print("3. View Destinations")
    print("4. Exit")

    choice = int(input("Enter your choice: "))
    if choice == 1:
        register_tourist()
    elif choice == 2:
        register_guide()
    elif choice == 3:
        view_destinations()
    elif choice == 4:
        print("Thank you for using the Tourist Guide System")
    else:
        print("Invalid choice. Please try again.")

def register_tourist():
    name = input("Enter your name: ")
    age = input("Enter your age: ")
    state = input("Enter your state of residence: ")

    print(f"Welcome {name}! You have registered as a Tourist.")
    print("Explore destinations and guides available.")

def register_guide():
    name = input("Enter your name: ")
    gender = input("Enter your gender: ")
    state = input("Enter the state you operate in: ")
    languages = input("Enter the languages you speak (comma-separated): ")
    phone = input("Enter your phone number: ")

    guide_data = {
        "name": name,
        "gender": gender,
        "state": state,
        "languages": languages.split(","),
        "phno": phone
    }

    with open("data1.json", "r") as file:
        guides = json.load(file)

    guides.append(guide_data)

    with open("data1.json", "w") as file:
        json.dump(guides, file, indent=4)

    print(f"Thank you {name}! You have registered as a Guide.")

def view_destinations():
    state = input("Enter the state you want to explore: ")

    with open("data.json", "r") as file:
        destinations = json.load(file)

    for destination in destinations:
        if destination["state"].lower() == state.lower():
            print(f"State: {destination['state']}")
            print(f"Attractions: {', '.join(destination['attractions'])}")
            print(f"Approximate Cost: {destination['cost']}")

            view_guides(state)
            return

    print("No destinations found for the entered state.")

def view_guides(state):
    print("\nAvailable guides for this state:")
    with open("data1.json", "r") as file:
        guides = json.load(file)

    for guide in guides:
        if guide["state"].lower() == state.lower():
            print(f"Name: {guide['name']}, Languages: {', '.join(guide['languages'])}, Phone: {guide['phno']}")

def display():
    print("Welcome to Tourist Guide.com")
    print("1. Login")
    print("2. Register")
    print("3. Exit")

    choice = int(input("Enter your choice: "))
    if choice == 1:
        login()
    elif choice == 2:
        register()
    elif choice == 3:
        print("Thank you for visiting this site")
    else:
        print("Invalid choice")

if __name__ == "__main__":
    display()

