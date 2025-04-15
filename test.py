import json
import random
import datetime
import time
from collections import defaultdict

# AI recommendation system
class TourismAI:
    def __init__(self):
        self.load_data()
        
    def load_data(self):
        with open("data.json", "r") as file:
            self.destinations = json.load(file)
        with open("data1.json", "r") as file:
            self.guides = json.load(file)
    
    def recommend_destinations(self, preferences):
        """Recommend destinations based on user preferences"""
        budget = preferences.get('budget', float('inf'))
        preferred_activities = preferences.get('activities', [])
        
        recommendations = []
        for destination in self.destinations:
            cost = float(destination['cost'])
            if cost <= budget:
                matching_activities = 0
                for activity in preferred_activities:
                    if any(activity.lower() in attr.lower() for attr in destination['attractions']):
                        matching_activities += 1
                
                score = matching_activities + (100000 - cost)/10000  # Higher score for cheaper options
                recommendations.append((destination, score))
        
        # Sort by score
        recommendations.sort(key=lambda x: x[1], reverse=True)
        return [r[0] for r in recommendations[:3]]  # Return top 3
    
    def find_best_guide(self, state, language_preference=None):
        """Find suitable guides based on state and preferred language"""
        suitable_guides = []
        for guide in self.guides:
            if guide["state"].lower() == state.lower():
                score = 1
                if language_preference and any(language_preference.lower() in lang.lower() for lang in guide["languages"]):
                    score += 2
                suitable_guides.append((guide, score))
        
        suitable_guides.sort(key=lambda x: x[1], reverse=True)
        return [g[0] for g in suitable_guides[:2]]  # Return top 2

# Chat system
class ChatSystem:
    def __init__(self):
        self.messages = defaultdict(list)
        self.active_users = {}
        self.load_messages()
    
    def load_messages(self):
        try:
            with open("chat_history.json", "r") as file:
                self.messages = defaultdict(list, json.load(file))
        except (FileNotFoundError, json.JSONDecodeError):
            self.messages = defaultdict(list)
    
    def save_messages(self):
        with open("chat_history.json", "w") as file:
            json.dump(dict(self.messages), file, indent=4)
    
    def send_message(self, sender, receiver, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        chat_id = self._get_chat_id(sender, receiver)
        
        msg = {
            "sender": sender,
            "timestamp": timestamp,
            "message": message,
            "read": False
        }
        
        self.messages[chat_id].append(msg)
        self.save_messages()
        return True
    
    def get_messages(self, user1, user2):
        chat_id = self._get_chat_id(user1, user2)
        return self.messages[chat_id]
    
    def get_unread_count(self, username):
        unread_counts = {}
        for chat_id, msgs in self.messages.items():
            users = chat_id.split('_')
            if username in users:
                other_user = users[0] if users[0] != username else users[1]
                unread_counts[other_user] = sum(1 for msg in msgs if msg['sender'] != username and not msg['read'])
        return unread_counts
    
    def mark_as_read(self, reader, sender):
        chat_id = self._get_chat_id(reader, sender)
        for msg in self.messages[chat_id]:
            if msg['sender'] == sender:
                msg['read'] = True
        self.save_messages()
    
    def _get_chat_id(self, user1, user2):
        # Create a consistent chat ID regardless of order
        return '_'.join(sorted([user1, user2]))

# User database functions
def get_user_type(username):
    try:
        with open("user_types.json", "r") as file:
            user_types = json.load(file)
            return user_types.get(username, None)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def set_user_type(username, user_type):
    try:
        with open("user_types.json", "r") as file:
            user_types = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        user_types = {}
    
    user_types[username] = user_type
    
    with open("user_types.json", "w") as file:
        json.dump(user_types, file, indent=4)

def save_tourist_profile(username, profile):
    try:
        with open("tourist_profiles.json", "r") as file:
            profiles = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        profiles = {}
    
    profiles[username] = profile
    
    with open("tourist_profiles.json", "w") as file:
        json.dump(profiles, file, indent=4)

def get_tourist_profile(username):
    try:
        with open("tourist_profiles.json", "r") as file:
            profiles = json.load(file)
            return profiles.get(username, {})
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_guide_profile(username, profile):
    try:
        with open("guide_profiles.json", "r") as file:
            profiles = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        profiles = {}
    
    profiles[username] = profile
    
    with open("guide_profiles.json", "w") as file:
        json.dump(profiles, file, indent=4)

def get_guide_profile(username):
    try:
        with open("guide_profiles.json", "r") as file:
            profiles = json.load(file)
            return profiles.get(username, None)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def get_all_guides():
    try:
        with open("guide_profiles.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def get_all_tourists():
    try:
        with open("tourist_profiles.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

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
    print("\n=== User Registration ===")
    username = input("Enter username: ")
    password = input("Enter password: (8-15 characters with uppercase, lowercase, digits, special symbols): ")

    if passwordvad(password):
        cpassword = input("Enter password to confirm: ")
        if password == cpassword:
            with open("user_data.txt", "a") as user_file:
                user_file.write(f"{username}:{password}\n")
            print("Registration successful")
            login(username)
        else:
            print("Passwords do not match")
    else:
        print("Invalid password. Follow password guidelines.")

def login(auto_username=None):
    print("\n=== User Login ===")
    if auto_username:
        username = auto_username
        print(f"Username: {username}")
    else:
        username = input("Enter username: ")
    
    if not auto_username:
        password = input("Enter password: ")

        found = False
        with open("user_data.txt", "r") as user_file:
            for line in user_file:
                if line.strip():
                    stored_username, stored_password = line.strip().split(":")
                    if username == stored_username and password == stored_password:
                        found = True
                        break
        
        if not found:
            print("Username does not exist or incorrect password")
            return

    user_type = get_user_type(username)
    
    if not user_type:
        tourist_guide_selection(username)
    else:
        if user_type == "tourist":
            tourist_menu(username)
        elif user_type == "guide":
            guide_menu(username)

def tourist_guide_selection(username):
    print("\n=== Welcome to the Tourist Guide System ===")
    print("Please register as a tourist or guide:")
    print("1. Register as a Tourist")
    print("2. Register as a Guide")
    
    choice = input("Enter your choice (1/2): ")
    if choice == "1":
        register_tourist(username)
    elif choice == "2":
        register_guide(username)
    else:
        print("Invalid choice. Please try again.")
        tourist_guide_selection(username)

def register_tourist(username):
    print("\n=== Tourist Registration ===")
    name = input("Enter your full name: ")
    age = input("Enter your age: ")
    state = input("Enter your state of residence: ")
    interests = input("Enter your travel interests (nature, history, adventure, etc.): ")
    budget = input("Enter your typical travel budget: ")
    
    profile = {
        "name": name,
        "age": age,
        "state": state,
        "interests": [interest.strip() for interest in interests.split(",")],
        "budget": budget,
        "registration_date": datetime.datetime.now().strftime("%Y-%m-%d")
    }
    
    save_tourist_profile(username, profile)
    set_user_type(username, "tourist")
    
    print(f"\nWelcome {name}! You have registered as a Tourist.")
    time.sleep(1)
    tourist_menu(username)

def register_guide(username):
    print("\n=== Guide Registration ===")
    name = input("Enter your full name: ")
    gender = input("Enter your gender: ")
    state = input("Enter the state you operate in: ")
    languages = input("Enter the languages you speak (comma-separated): ")
    phone = input("Enter your phone number: ")
    experience = input("Enter years of experience as a guide: ")
    specialization = input("Enter your specialization (nature, history, culture, etc.): ")
    
    profile = {
        "name": name,
        "gender": gender,
        "state": state,
        "languages": [lang.strip() for lang in languages.split(",")],
        "phno": phone,
        "experience": experience,
        "specialization": specialization,
        "rating": 0,
        "reviews": [],
        "registration_date": datetime.datetime.now().strftime("%Y-%m-%d")
    }
    
    save_guide_profile(username, profile)
    set_user_type(username, "guide")
    
    # Also add to the original guides.json for compatibility
    with open("data1.json", "r") as file:
        guides = json.load(file)
    
    guides.append({
        "name": name,
        "gender": gender,
        "state": state,
        "languages": [lang.strip() for lang in languages.split(",")],
        "phno": phone
    })
    
    with open("data1.json", "w") as file:
        json.dump(guides, file, indent=4)
    
    print(f"\nThank you {name}! You have registered as a Guide.")
    time.sleep(1)
    guide_menu(username)

def tourist_menu(username):
    profile = get_tourist_profile(username)
    
    while True:
        print(f"\n=== Tourist Menu - Welcome {profile.get('name', username)} ===")
        print("1. View Destinations")
        print("2. Get AI Destination Recommendations")
        print("3. Find Guides")
        print("4. View Messages")
        print("5. Update Profile")
        print("6. Logout")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            view_destinations()
        elif choice == "2":
            get_ai_recommendations(username)
        elif choice == "3":
            find_guides(username)
        elif choice == "4":
            view_messages(username)
        elif choice == "5":
            update_tourist_profile(username)
        elif choice == "6":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

def guide_menu(username):
    profile = get_guide_profile(username)
    
    while True:
        print(f"\n=== Guide Menu - Welcome {profile.get('name', username)} ===")
        print("1. View Your Profile")
        print("2. View Messages")
        print("3. Update Profile")
        print("4. View Potential Tourists")
        print("5. Logout")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            view_guide_profile(username)
        elif choice == "2":
            view_messages(username)
        elif choice == "3":
            update_guide_profile(username)
        elif choice == "4":
            view_potential_tourists(username)
        elif choice == "5":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

def view_guide_profile(username):
    profile = get_guide_profile(username)
    if profile:
        print("\n=== Your Guide Profile ===")
        print(f"Name: {profile['name']}")
        print(f"State: {profile['state']}")
        print(f"Languages: {', '.join(profile['languages'])}")
        print(f"Phone: {profile['phno']}")
        print(f"Experience: {profile['experience']} years")
        print(f"Specialization: {profile['specialization']}")
        print(f"Rating: {profile['rating']} stars")
        
        if profile['reviews']:
            print("\nReviews:")
            for review in profile['reviews']:
                print(f"- {review['text']} ({review['rating']} stars)")
    else:
        print("Profile not found.")
    
    input("\nPress Enter to continue...")

def update_tourist_profile(username):
    profile = get_tourist_profile(username)
    
    print("\n=== Update Tourist Profile ===")
    print("Leave blank to keep current value")
    
    name = input(f"Name [{profile.get('name', '')}]: ")
    age = input(f"Age [{profile.get('age', '')}]: ")
    state = input(f"State [{profile.get('state', '')}]: ")
    interests = input(f"Interests [{', '.join(profile.get('interests', []))}]: ")
    budget = input(f"Budget [{profile.get('budget', '')}]: ")
    
    if name:
        profile['name'] = name
    if age:
        profile['age'] = age
    if state:
        profile['state'] = state
    if interests:
        profile['interests'] = [interest.strip() for interest in interests.split(",")]
    if budget:
        profile['budget'] = budget
    
    save_tourist_profile(username, profile)
    print("Profile updated successfully!")

def update_guide_profile(username):
    profile = get_guide_profile(username)
    
    print("\n=== Update Guide Profile ===")
    print("Leave blank to keep current value")
    
    name = input(f"Name [{profile.get('name', '')}]: ")
    state = input(f"State [{profile.get('state', '')}]: ")
    languages = input(f"Languages [{', '.join(profile.get('languages', []))}]: ")
    phone = input(f"Phone [{profile.get('phno', '')}]: ")
    experience = input(f"Experience [{profile.get('experience', '')}]: ")
    specialization = input(f"Specialization [{profile.get('specialization', '')}]: ")
    
    if name:
        profile['name'] = name
    if state:
        profile['state'] = state
    if languages:
        profile['languages'] = [lang.strip() for lang in languages.split(",")]
    if phone:
        profile['phno'] = phone
    if experience:
        profile['experience'] = experience
    if specialization:
        profile['specialization'] = specialization
    
    save_guide_profile(username, profile)
    
    # Update in data1.json as well
    with open("data1.json", "r") as file:
        guides = json.load(file)
    
    for guide in guides:
        if guide['name'] == profile['name'] or (guide.get('username') == username):
            guide['name'] = profile['name']
            guide['state'] = profile['state']
            guide['languages'] = profile['languages']
            guide['phno'] = profile['phno']
            guide['username'] = username  # Add username reference
            break
    
    with open("data1.json", "w") as file:
        json.dump(guides, file, indent=4)
    
    print("Profile updated successfully!")

def get_ai_recommendations(username):
    ai = TourismAI()
    profile = get_tourist_profile(username)
    
    print("\n=== AI Destination Recommendations ===")
    print("Let's find the perfect destinations for you!")
    
    # Use existing preferences or get new ones
    if profile.get('interests'):
        use_profile = input(f"Would you like to use your profile interests ({', '.join(profile.get('interests', []))})? (y/n): ")
        if use_profile.lower() == 'y':
            activities = profile.get('interests', [])
        else:
            activities_input = input("What activities are you interested in? (comma-separated): ")
            activities = [act.strip() for act in activities_input.split(",")]
    else:
        activities_input = input("What activities are you interested in? (comma-separated): ")
        activities = [act.strip() for act in activities_input.split(",")]
    
    if profile.get('budget'):
        use_budget = input(f"Would you like to use your profile budget ({profile.get('budget')})? (y/n): ")
        if use_budget.lower() == 'y':
            try:
                budget = float(profile.get('budget', '0'))
            except ValueError:
                budget = float(input("Enter your budget (numbers only): "))
        else:
            budget = float(input("Enter your budget (numbers only): "))
    else:
        budget = float(input("Enter your budget (numbers only): "))
    
    preferences = {
        'budget': budget,
        'activities': activities
    }
    
    recommendations = ai.recommend_destinations(preferences)
    
    if recommendations:
        print("\nBased on your preferences, we recommend these destinations:")
        for i, destination in enumerate(recommendations, 1):
            print(f"\n{i}. {destination['state']}")
            print(f"   Attractions: {', '.join(destination['attractions'])}")
            print(f"   Approximate Cost: Rs. {destination['cost']}")
            
            # Find guides for this destination
            print("\n   Recommended Guides:")
            preferred_language = input("Do you have a preferred language for your guide? (leave blank if none): ")
            guides = ai.find_best_guide(destination['state'], preferred_language)
            
            if guides:
                for guide in guides:
                    print(f"   - {guide['name']} - Languages: {', '.join(guide['languages'])}, Phone: {guide['phno']}")
            else:
                print("   - No guides available for this destination")
    else:
        print("\nNo recommendations found based on your preferences.")
    
    input("\nPress Enter to continue...")

def view_destinations():
    print("\n=== View Destinations ===")
    state = input("Enter the state you want to explore (or leave blank to see all): ")
    
    with open("data.json", "r") as file:
        destinations = json.load(file)
    
    found = False
    for destination in destinations:
        if not state or destination["state"].lower() == state.lower():
            found = True
            print(f"\nState: {destination['state']}")
            print(f"Attractions: {', '.join(destination['attractions'])}")
            print(f"Approximate Cost: Rs. {destination['cost']}")
            
            if state:  # Only show guides if specific state
                view_guides_for_state(state)
                break
    
    if not found:
        print("No destinations found for the entered state.")
    
    input("\nPress Enter to continue...")

def view_guides_for_state(state):
    print("\n=== Available guides for this state ===")
    with open("data1.json", "r") as file:
        guides = json.load(file)
    
    found = False
    for guide in guides:
        if guide["state"].lower() == state.lower():
            found = True
            print(f"Name: {guide['name']}")
            print(f"Languages: {', '.join(guide['languages'])}")
            print(f"Phone: {guide['phno']}")
            print("")
    
    if not found:
        print("No guides available for this state.")

def find_guides(username):
    print("\n=== Find Guides ===")
    state = input("Enter the state you want to find guides for: ")
    
    tourist_profile = get_tourist_profile(username)
    
    with open("guide_profiles.json", "r") as file:
        try:
            guide_profiles = json.load(file)
        except json.JSONDecodeError:
            guide_profiles = {}
    
    found = False
    guides_list = []
    
    for guide_username, profile in guide_profiles.items():
        if profile["state"].lower() == state.lower():
            found = True
            guides_list.append((guide_username, profile))
    
    if found:
        print(f"\nGuides available in {state}:")
        for i, (guide_username, profile) in enumerate(guides_list, 1):
            print(f"{i}. {profile['name']}")
            print(f"   Experience: {profile.get('experience', 'N/A')} years")
            print(f"   Languages: {', '.join(profile['languages'])}")
            print(f"   Specialization: {profile.get('specialization', 'N/A')}")
            print(f"   Rating: {profile.get('rating', 'No ratings yet')}")
            print("")
        
        choice = input("Enter the number of the guide you would like to contact (or 0 to return): ")
        try:
            choice = int(choice)
            if 1 <= choice <= len(guides_list):
                guide_username, guide_profile = guides_list[choice-1]
                chat_with_guide(username, guide_username)
            elif choice != 0:
                print("Invalid choice.")
        except ValueError:
            print("Please enter a number.")
    else:
        print(f"No guides found for {state}.")
    
    input("\nPress Enter to continue...")

def view_potential_tourists(username):
    print("\n=== Potential Tourists ===")
    guide_profile = get_guide_profile(username)
    
    if not guide_profile:
        print("Your guide profile not found.")
        return
    
    guide_state = guide_profile['state']
    
    with open("tourist_profiles.json", "r") as file:
        try:
            tourist_profiles = json.load(file)
        except json.JSONDecodeError:
            tourist_profiles = {}
    
    potential_tourists = []
    
    for tourist_username, profile in tourist_profiles.items():
        # Match tourists based on their interests or state matching guide's state
        if any(interest.lower() in guide_profile.get('specialization', '').lower() for interest in profile.get('interests', [])) or \
           profile.get('state', '').lower() == guide_state.lower():
            potential_tourists.append((tourist_username, profile))
    
    if potential_tourists:
        print(f"\nPotential tourists who might be interested in your services:")
        for i, (tourist_username, profile) in enumerate(potential_tourists, 1):
            print(f"{i}. {profile.get('name', tourist_username)}")
            print(f"   Interests: {', '.join(profile.get('interests', ['Not specified']))}")
            print(f"   State: {profile.get('state', 'Not specified')}")
            print("")
        
        choice = input("Enter the number of the tourist you would like to contact (or 0 to return): ")
        try:
            choice = int(choice)
            if 1 <= choice <= len(potential_tourists):
                tourist_username, tourist_profile = potential_tourists[choice-1]
                chat_with_tourist(username, tourist_username)
            elif choice != 0:
                print("Invalid choice.")
        except ValueError:
            print("Please enter a number.")
    else:
        print("No potential tourists found.")
    
    input("\nPress Enter to continue...")

def view_messages(username):
    chat_system = ChatSystem()
    user_type = get_user_type(username)
    
    if user_type == "tourist":
        other_users = get_all_guides()
    else:  # guide
        other_users = get_all_tourists()
    
    unread_counts = chat_system.get_unread_count(username)
    
    users_with_messages = []
    
    for other_username, count in unread_counts.items():
        if other_username in other_users:
            users_with_messages.append((other_username, count, other_users[other_username]))
    
    # Add users with no unread messages but have chat history
    for other_username, profile in other_users.items():
        if other_username not in unread_counts and chat_system.get_messages(username, other_username):
            users_with_messages.append((other_username, 0, profile))
    
    if not users_with_messages:
        print("\nYou don't have any messages.")
        input("\nPress Enter to continue...")
        return
    
    print("\n=== Your Messages ===")
    for i, (other_username, unread, profile) in enumerate(users_with_messages, 1):
        unread_badge = f"({unread} unread)" if unread > 0 else ""
        print(f"{i}. {profile.get('name', other_username)} {unread_badge}")
    
    print("0. Back to menu")
    
    choice = input("\nSelect a conversation: ")
    try:
        choice = int(choice)
        if 1 <= choice <= len(users_with_messages):
            other_username, _, _ = users_with_messages[choice-1]
            
            if user_type == "tourist":
                chat_with_guide(username, other_username)
            else:  # guide
                chat_with_tourist(username, other_username)
        elif choice != 0:
            print("Invalid choice.")
    except ValueError:
        print("Please enter a number.")

def chat_with_guide(tourist_username, guide_username):
    chat_system = ChatSystem()
    tourist_profile = get_tourist_profile(tourist_username)
    guide_profile = get_guide_profile(guide_username)
    
    print(f"\n=== Chat with {guide_profile.get('name', guide_username)} ===")
    print(f"Guide info: {guide_profile.get('experience', 'N/A')} years exp., Specializes in {guide_profile.get('specialization', 'N/A')}")
    
    # Mark messages as read
    chat_system.mark_as_read(tourist_username, guide_username)
    
    # Display chat history
    messages = chat_system.get_messages(tourist_username, guide_username)
    
    if messages:
        for msg in messages:
            sender_name = guide_profile.get('name', guide_username) if msg['sender'] == guide_username else tourist_profile.get('name', tourist_username)
            print(f"[{msg['timestamp']}] {sender_name}: {msg['message']}")
    else:
        print("No previous messages.")
    
    while True:
        message = input("\nType your message (or 'exit' to return): ")
        
        if message.lower() == 'exit':
            break
        
        chat_system.send_message(tourist_username, guide_username, message)
        print(f"[Message sent to {guide_profile.get('name', guide_username)}]")
        
        # Simulate guide response for better user experience
        simulate_response = random.random() < 0.7  # 70% chance of immediate response
        
        if simulate_response:
            responses = [
                "Thank you for your message! I'll get back to you shortly.",
                "I've received your inquiry and will respond soon.",
                "Thanks for contacting me about your trip. Let me check my schedule.",
                "I appreciate your interest in my guide services. I'm available to discuss further.",
                "Thank you for reaching out. I'd be happy to help with your travel plans."
            ]
            
            time.sleep(random.uniform(1.5, 3.0))  # Simulate typing delay
            auto_response = random.choice(responses)
            chat_system.send_message(guide_username, tourist_username, auto_response)
            print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {guide_profile.get('name', guide_username)}: {auto_response}")

def chat_with_tourist(guide_username, tourist_username):
    chat_system = ChatSystem()
    guide_profile = get_guide_profile(guide_username)
    tourist_profile = get_tourist_profile(tourist_username)
    
    print(f"\n=== Chat with {tourist_profile.get('name', tourist_username)} ===")
    print(f"Tourist info: Interested in {', '.join(tourist_profile.get('interests', ['Not specified']))}")
    
    # Mark messages as read
    chat_system.mark_as_read(guide_username, tourist_username)
    
    # Display chat history
    messages = chat_system.get_messages(guide_username, tourist_username)
    
    if messages:
        for msg in messages:
            sender_name = guide_profile.get('name', guide_username) if msg['sender'] == guide_username else tourist_profile.get('name', tourist_username)
            print(f"[{msg['timestamp']}] {sender_name}: {msg['message']}")
    else:
        print("No previous messages.")
    
    while True:
        message = input("\nType your message (or 'exit' to return): ")
        
        if message.lower() == 'exit':
            break
        
        chat_system.send_message(guide_username, tourist_username, message)
        print(f"[Message sent to {tourist_profile.get('name', tourist_username)}]")

def display():
   def display():
    print("\n=============================================")
    print("Welcome to Tourist Guide.com")
    print("Your Smart Travel Companion with AI Integration")
    print("=============================================")
    
    print("\n1. Login")
    print("2. Register")
    print("3. Exit")
    
    choice = input("\nEnter your choice: ")
    if choice == "1":
        login()
    elif choice == "2":
        register()
    elif choice == "3":
        print("Thank you for visiting this site")
    else:
        print("Invalid choice")

if __name__ == "__main__":
    display()