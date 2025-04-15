import streamlit as st
import json
import os
from datetime import datetime

# --- Apply custom styling ---
def apply_custom_styles():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=Lato:wght@300;400;700&family=Playfair+Display:ital,wght@0,400;0,600;1,400;1,600&display=swap');

        .stApp {
            background-image: url("https://images.unsplash.com/photo-1530789253388-582c481c54b0");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }

        .custom-info-box {
            background: rgba(0, 0, 0, 0.8);  /* Changed to black background */
            padding: 1.2rem 1.5rem;
            border-radius: 12px;
            border-left: 5px solid #4dd0e1;
            margin-bottom: 1.5rem;
            color: #ffffff;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
            font-family: 'Lato', sans-serif;
            font-size: 1.05rem;
        }

        .custom-alert-box {
            background: rgba(0, 0, 0, 0.8);  /* Changed to black background */
            padding: 1.2rem 1.5rem;
            border-radius: 12px;
            border-left: 5px solid #ff5252;
            margin-bottom: 1.5rem;
            color: #ffffff;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
            font-family: 'Lato', sans-serif;
            font-size: 1.05rem;
        }

        .main-heading h2 {
            font-family: 'Roboto Slab', serif;
            font-size: 2.7rem;
            font-weight: 800;
            color: #ffffff;  /* Changed text color to white for better visibility */
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.4);
        }

        .main-heading .sub-quote {
            font-size: 1.1rem;
            color: #FF5722;
            margin-top: 0.4rem;
            font-style: italic;
        }

        header, footer, .stDeployButton,
        [data-testid="stHeader"], 
        [data-testid="stToolbar"],
        .css-1dp5vir, .css-14xtw13,
        .css-1adrfps, .css-1rs6os {
            display: none !important;
        }

        div:empty {
            display: none !important;
        }

        .block-container {
            background-color: transparent !important;
        }

        section[data-testid="stSidebar"] {
            background-color: rgba(0, 0, 0, 0.9);  /* Changed to black background */
            backdrop-filter: blur(4px);
            border-right: 1px solid rgba(255, 255, 255, 0.2);
        }

        section[data-testid="stSidebar"] * {
            color: #ffffff !important;
        }

        .main-box {
            background-color: rgba(0, 0, 0, 0.9);  /* Changed to black background */
            padding: 2.5rem;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(8px);
            max-width: 850px;
            margin: 2rem auto;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .main-heading {
            text-align: center;
            margin-bottom: 2rem;
        }

        .sub-quote {
            font-family: 'Playfair Display', serif;
            font-style: italic;
            font-size: 1.1rem;
            color: #f0f8ff;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
        }

        h3 {
            font-family: 'Montserrat', sans-serif;
            font-weight: 600;
            color: #ffffff !important;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
        }

        h4, h5, h6 {
            font-family: 'Montserrat', sans-serif;
            color: #ffffff !important;
        }

        p, label, div, span {
            font-family: 'Lato', sans-serif;
            color: #ffffff !important;
            font-size: 1.05rem;
        }

        .stButton>button {
            background-color: #FF9E44;
            color: white !important;
            border-radius: 8px;
            font-weight: 600;
            border: none;
            padding: 0.5rem 1rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        .stButton>button:hover {
            background-color: #FF7E1C;
            transform: translateY(-2px);
            box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
        }

        /* Input fields and select boxes */
        .stTextInput>div>div>input, 
        .stNumberInput>div>div>input {
            background-color: rgba(0, 0, 0, 0.9) !important;  /* Changed to black background */
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            color: #ffffff !important;
        }

        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            background-color: rgba(0, 0, 0, 0.9) !important;  /* Added black background for tab list */
            border-radius: 8px 8px 0 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        }

        .stTabs [data-baseweb="tab"] {
            background-color: rgba(0, 0, 0, 0.8) !important;  /* Added black background for tabs */
            color: white !important;
            border-radius: 5px 5px 0 0;
            margin-right: 2px;
            padding: 10px 20px;
        }

        .stTabs [aria-selected="true"] {
            background-color: rgba(77, 208, 225, 0.2) !important;  /* Active tab with slight tint */
            border-bottom: 2px solid #4dd0e1 !important;
        }

        .stTabs [data-baseweb="tab-panel"] {
            background-color: rgba(0, 0, 0, 0.8) !important;  /* Added black background for tab content */
            border-radius: 0 0 8px 8px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        /* Select box containers */
        .stSelectbox > div[data-baseweb="select"], 
        .stMultiselect > div[data-baseweb="select"] {
            background-color: rgba(0, 0, 0, 0.9) !important;  /* Changed to black background */
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 8px;
        }

        /* Input text and placeholder fix */
        .stSelectbox div[data-baseweb="select"] input,
        .stMultiselect div[data-baseweb="select"] input {
            color: #ffffff !important;
        }

        .stSelectbox div[data-baseweb="select"] input::placeholder,
        .stMultiselect div[data-baseweb="select"] input::placeholder {
            color: rgba(255, 255, 255, 0.6) !important;
        }

        .stSelectbox div[data-baseweb="select"] > div > div,
        .stMultiselect div[data-baseweb="select"] > div > div {
            color: #ffffff !important;
        }

        /* Dropdown container and menu */
        div[data-baseweb="popover"], 
        div[data-baseweb="popover"] > div {
            background-color: rgba(0, 0, 0, 0.9) !important;
        }

        div[data-baseweb="popover"] div[data-baseweb="menu"],
        div[data-baseweb="popover"] div[role="listbox"] {
            background-color: rgba(0, 0, 0, 0.9) !important;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        /* Dropdown options */
        div[data-baseweb="popover"] div[data-baseweb="menu"] ul li,
        div[data-baseweb="popover"] div[role="listbox"] ul li,
        div[data-baseweb="popover"] div[role="option"] {
            background-color: rgba(0, 0, 0, 0.9) !important;
            color: #ffffff !important;
        }

        div[data-baseweb="popover"] div[data-baseweb="menu"] ul li:hover,
        div[data-baseweb="popover"] div[role="listbox"] ul li:hover,
        div[data-baseweb="popover"] div[role="option"]:hover {
            background-color: rgba(77, 208, 225, 0.3) !important;
        }

        .stMultiselect [data-baseweb="tag"] {
            background-color: rgba(77, 208, 225, 0.5) !important;
            color: #ffffff !important;
        }

        div[data-baseweb="select"] [aria-selected="true"] {
            background-color: rgba(0, 0, 0, 0.9) !important;
        }

        div[role="listbox"], 
        div[role="option"],
        div[data-baseweb="select-dropdown"],
        div[data-baseweb="menu"] {
            background-color: rgba(0, 0, 0, 0) !important;
            color: #737373 !important;
        }

        .ai-chat-container {
            background-color: rgba(0, 0, 0, 0.9);  /* Changed to black background */
            border-radius: 12px;
            padding: 20px;
            margin-top: 30px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        }

        .chat-message {
            padding: 10px 15px;
            border-radius: 8px;
            margin-bottom: 10px;
            max-width: 80%;
            word-wrap: break-word;
        }

        .user-message {
            background-color: rgba(255, 158, 68, 0.7);
            margin-left: auto;
            text-align: right;
        }

        .ai-message {
            background-color: rgba(77, 208, 225, 0.7);
            margin-right: auto;
        }

        .chat-input {
            margin-top: 15px;
        }

        div.block-container {
            padding-top: 1rem !important;
            margin-top: 0 !important;
        }

        section.main {
            margin-top: 0 !important;
        }

        .css-1544g2n.e1fqkh3o4 {
            margin-top: 0 !important;
            padding-top: 0 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )



# --- Password validation ---
def password_valid(password):
    return (
        8 <= len(password) <= 15 and
        any(c.islower() for c in password) and
        any(c.isupper() for c in password) and
        any(c.isdigit() for c in password) and
        any(c in "!@#$%^&*()_+" for c in password)
    )

# --- Check if username exists ---
def username_exists(username):
    if not os.path.exists("user_data.txt"):
        return False
    
    with open("user_data.txt", "r") as f:
        for line in f:
            stored_user = line.strip().split(":")[0]
            if username == stored_user:
                return True
    return False

# --- Registration ---
def register():
    st.subheader("📝 Register")
    username = st.text_input("Username")
    
    # Display password requirements
    st.markdown("""
    **Password Requirements:**
    - 8-15 characters long
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character (!@#$%^&*()_+)
    """)
    
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    role = st.selectbox("Select Role", ["Tourist", "Guide", "Admin"])

    if st.button("Register"):
        if not username:
            st.error("Username cannot be empty.")
        elif username_exists(username):
            st.error("Username already exists. Please choose a different username.")
        elif not password_valid(password):
            st.error("Password does not meet the requirements.")
        elif password != confirm_password:
            st.error("Passwords do not match.")
        else:
            # Save the user data including the role
            with open("user_data.txt", "a") as f:
                f.write(f"{username}:{password}:{role}\n")
            st.success("Registration successful. Please log in.")
            # Redirect to login page
            st.session_state.nav = "Login"
            st.rerun()  # Updated from experimental_rerun()

# --- Login ---
def login():
    st.subheader("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if not username or not password:
            st.error("Username and password cannot be empty.")
            return
        
        try:
            with open("user_data.txt", "r") as f:
                for line in f:
                    line = line.strip()
                    if not line:  # Skip empty lines
                        continue
                        
                    # Handle case where there might not be exactly 3 fields
                    parts = line.split(":")
                    if len(parts) < 2:
                        continue  # Skip invalid entries
                        
                    stored_user = parts[0]
                    stored_pass = parts[1]
                    role = parts[2] if len(parts) > 2 else "Tourist"  # Default to Tourist if role is missing
                    
                    if username == stored_user and password == stored_pass:
                        st.success("Login successful.")
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.role = role
                        # Redirect to appropriate dashboard based on role
                        if role == "Tourist":
                            st.session_state.nav = "Tourist Dashboard"
                        elif role == "Guide":
                            st.session_state.nav = "Guide Dashboard"
                        elif role == "Admin":
                            st.session_state.nav = "Admin Dashboard"
                        st.rerun()  # Changed from experimental_rerun()
                        return
            st.error("Incorrect username or password.")
        except FileNotFoundError:
            st.error("No users found. Please register first.")



# --- Tourist Registration ---
def register_tourist():
    if not st.session_state.logged_in or st.session_state.role != "Tourist":
        st.warning("Please login as a Tourist first.")
        return
        
    st.subheader("🌴 Complete Tourist Profile")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, max_value=120, step=1)
    state = st.text_input("State")

    if st.button("Submit Tourist Info"):
        if not name or not state:
            st.error("Please fill in all fields.")
            return
            
        tourist_data = {
            "username": st.session_state.username,
            "name": name,
            "age": age,
            "state": state
        }
        
        tourists = []
        if os.path.exists("tourists.json"):
            with open("tourists.json", "r") as f:
                tourists = json.load(f)
                
        # Check if this user already has a profile
        for i, tourist in enumerate(tourists):
            if tourist.get("username") == st.session_state.username:
                tourists[i] = tourist_data
                with open("tourists.json", "w") as f:
                    json.dump(tourists, f, indent=4)
                st.success(f"Profile updated successfully, {name}!")
                return
                
        # If not, add new profile
        tourists.append(tourist_data)
        with open("tourists.json", "w") as f:
            json.dump(tourists, f, indent=4)
        st.success(f"Welcome {name}! Your tourist profile is complete.")

# --- Guide Registration ---
def register_guide():
    if not st.session_state.logged_in or st.session_state.role != "Guide":
        st.warning("Please login as a Guide first.")
        return
        
    st.subheader("🧭 Complete Guide Profile")
    name = st.text_input("Name")
    gender = st.radio("Gender", ["Male", "Female", "Other"])
    state = st.text_input("State you operate in")
    languages = st.text_input("Languages spoken (comma separated)")
    phone = st.text_input("Phone Number")

    if st.button("Submit Guide Info"):
        if not name or not state or not languages or not phone:
            st.error("Please fill in all fields.")
            return
            
        guide_data = {
            "username": st.session_state.username,
            "name": name,
            "gender": gender,
            "state": state,
            "languages": [lang.strip() for lang in languages.split(",")],
            "phno": phone
        }

        guides = []
        if os.path.exists("data1.json"):
            with open("data1.json", "r") as f:
                guides = json.load(f)
                
        # Check if this user already has a profile
        for i, guide in enumerate(guides):
            if guide.get("username") == st.session_state.username:
                guides[i] = guide_data
                with open("data1.json", "w") as f:
                    json.dump(guides, f, indent=4)
                st.success(f"Profile updated successfully, {name}!")
                return

        guides.append(guide_data)
        with open("data1.json", "w") as f:
            json.dump(guides, f, indent=4)
        st.success(f"Thank you {name}, your guide profile is complete!")

# --- Admin Panel ---
def admin_panel():
    if not st.session_state.logged_in or st.session_state.role != "Admin":
        st.warning("Admin access required.")
        return
        
    st.subheader("🛠️ Admin Panel")
    st.write(f"Welcome, {st.session_state.username}! Here you can manage all data.")

    tabs = st.tabs(["Users", "Tourists", "Guides", "Destinations"])
    
    with tabs[0]:
        st.write("### Registered Users:")
        try:
            with open("user_data.txt", "r") as f:
                users = f.readlines()
            
            if not users:
                st.info("No users registered yet.")
            else:
                for user in users:
                    user = user.strip()
                    if user:  # Skip empty lines
                        parts = user.split(":")
                        if len(parts) >= 3:
                            username, _, role = parts[0], parts[1], parts[2]
                            st.write(f"- **{username}** ({role})")
                        else:
                            # Handle malformed data
                            st.warning(f"Malformed user entry: {user}")
        except FileNotFoundError:
            st.error("User data file not found.")
            
    with tabs[1]:
        st.write("### Registered Tourists:")
        try:
            if os.path.exists("tourists.json"):
                with open("tourists.json", "r") as f:
                    tourists = json.load(f)
                
                if not tourists:
                    st.info("No tourists registered yet.")
                else:
                    for tourist in tourists:
                        st.write(f"- **{tourist['name']}** | Age: {tourist['age']} | State: {tourist['state']}")
            else:
                st.info("No tourists registered yet.")
        except Exception as e:
            st.error(f"Error loading tourist data: {e}")
            
    with tabs[2]:
        st.write("### Registered Guides:")
        try:
            if os.path.exists("data1.json"):
                with open("data1.json", "r") as f:
                    guides = json.load(f)
                
                if not guides:
                    st.info("No guides registered yet.")
                else:
                    for guide in guides:
                        st.write(f"- **{guide['name']}** | State: {guide['state']} | Languages: {', '.join(guide['languages'])} | Phone: {guide['phno']}")
            else:
                st.info("No guides registered yet.")
        except Exception as e:
            st.error(f"Error loading guide data: {e}")
            
    with tabs[3]:
        st.write("### Destinations:")
        try:
            if os.path.exists("data.json"):
                with open("data.json", "r") as f:
                    destinations = json.load(f)
                
                if not destinations:
                    st.info("No destinations added yet.")
                else:
                    for dest in destinations:
                        st.write(f"- **{dest['state']}** | Attractions: {', '.join(dest['attractions'])} | Cost: {dest['cost']}")
            else:
                st.info("No destinations added yet.")
        except Exception as e:
            st.error(f"Error loading destination data: {e}")
        
    # Add management functions
    st.divider()
    st.subheader("Manage Data")
    
    # User management
    with st.expander("Manage Users"):
        # Delete user
        st.write("#### Delete User")
        try:
            with open("user_data.txt", "r") as f:
                users = f.readlines()
            
            if users:
                user_list = []
                for user in users:
                    parts = user.strip().split(":")
                    if len(parts) >= 3:
                        user_list.append(parts[0])
                
                if user_list:
                    selected_user = st.selectbox("Select user to delete:", user_list)
                    if st.button("Delete User"):
                        new_users = []
                        for user in users:
                            parts = user.strip().split(":")
                            if len(parts) >= 3 and parts[0] != selected_user:
                                new_users.append(user)
                        
                        with open("user_data.txt", "w") as f:
                            f.writelines(new_users)
                        
                        st.success(f"User {selected_user} deleted successfully!")
                        st.rerun()
                else:
                    st.info("No valid users to delete.")
            else:
                st.info("No users available.")
        except FileNotFoundError:
            st.error("User data file not found.")
    
    # Tourist management
    with st.expander("Manage Tourists"):
        st.write("#### Delete Tourist")
        try:
            if os.path.exists("tourists.json"):
                with open("tourists.json", "r") as f:
                    tourists = json.load(f)
                
                if tourists:
                    tourist_names = [tourist["name"] for tourist in tourists]
                    selected_tourist = st.selectbox("Select tourist to delete:", tourist_names)
                    
                    if st.button("Delete Tourist"):
                        new_tourists = [t for t in tourists if t["name"] != selected_tourist]
                        
                        with open("tourists.json", "w") as f:
                            json.dump(new_tourists, f, indent=4)
                        
                        st.success(f"Tourist {selected_tourist} deleted successfully!")
                        st.rerun()
                else:
                    st.info("No tourists available.")
            else:
                st.info("No tourists registered yet.")
        except Exception as e:
            st.error(f"Error managing tourist data: {e}")
    
    # Guide management
    with st.expander("Manage Guides"):
        st.write("#### Delete Guide")
        try:
            if os.path.exists("data1.json"):
                with open("data1.json", "r") as f:
                    guides = json.load(f)
                
                if guides:
                    guide_names = [guide["name"] for guide in guides]
                    selected_guide = st.selectbox("Select guide to delete:", guide_names)
                    
                    if st.button("Delete Guide"):
                        new_guides = [g for g in guides if g["name"] != selected_guide]
                        
                        with open("data1.json", "w") as f:
                            json.dump(new_guides, f, indent=4)
                        
                        st.success(f"Guide {selected_guide} deleted successfully!")
                        st.rerun()
                else:
                    st.info("No guides available.")
            else:
                st.info("No guides registered yet.")
        except Exception as e:
            st.error(f"Error managing guide data: {e}")
    
    # Destination management
    with st.expander("Manage Destinations"):
        st.write("#### Delete Destination")
        try:
            if os.path.exists("data.json"):
                with open("data.json", "r") as f:
                    destinations = json.load(f)
                
                if destinations:
                    dest_names = [dest["state"] for dest in destinations]
                    selected_dest = st.selectbox("Select destination to delete:", dest_names)
                    
                    if st.button("Delete Destination"):
                        new_dests = [d for d in destinations if d["state"] != selected_dest]
                        
                        with open("data.json", "w") as f:
                            json.dump(new_dests, f, indent=4)
                        
                        st.success(f"Destination {selected_dest} deleted successfully!")
                        st.rerun()
                else:
                    st.info("No destinations available.")
            else:
                st.info("No destinations registered yet.")
        except Exception as e:
            st.error(f"Error managing destination data: {e}")
            
# --- Tourist Dashboard ---
def tourist_dashboard():
    if not st.session_state.logged_in or st.session_state.role != "Tourist":
        st.warning("Please login as a Tourist first.")
        return
        
    st.subheader("🌴 Tourist Dashboard")
    st.write("Explore destinations, find guides, and plan your trip!")

    # Check if profile is complete
    tourist_profile = None
    if os.path.exists("tourists.json"):
        with open("tourists.json", "r") as f:
            tourists = json.load(f)
            for tourist in tourists:
                if tourist.get("username") == st.session_state.username:
                    tourist_profile = tourist
                    break
    
    if not tourist_profile:
        st.warning("Please complete your tourist profile first.")
        register_tourist()
    else:
        st.write(f"Welcome back, {tourist_profile['name']}!")
        
        # View Destinations tab
        view_destinations()

# --- Guide Dashboard ---
def guide_dashboard():
    if not st.session_state.logged_in or st.session_state.role != "Guide":
        st.warning("Please login as a Guide first.")
        return
        
    st.subheader("🧭 Guide Dashboard")
    
    # Check if profile is complete
    guide_profile = None
    if os.path.exists("data1.json"):
        with open("data1.json", "r") as f:
            guides = json.load(f)
            for guide in guides:
                if guide.get("username") == st.session_state.username or guide.get("name") == st.session_state.username:
                    guide_profile = guide
                    break
    
    if not guide_profile:
        st.warning("Please complete your guide profile first.")
        register_guide()
    else:
        st.write(f"Welcome back, {guide_profile['name']}!")
        
        # Get all chats for this guide
        guide_chats = get_guide_chats(guide_profile['name'])
        
        if not guide_chats:
            st.info("You don't have any messages from tourists yet.")
        else:
            st.subheader("Your Conversations")
            
            # Display list of tourists who've messaged this guide
            tourist_names = list(guide_chats.keys())
            
            if "selected_tourist" not in st.session_state:
                st.session_state.selected_tourist = None
                
            # Create tabs for each tourist conversation
            tabs = st.tabs(tourist_names)
            
            for i, tourist_name in enumerate(tourist_names):
                with tabs[i]:
                    # Get chat ID
                    chat_id = f"{tourist_name}_{guide_profile['name'].replace(' ', '_')}"
                    
                    # Initialize chat messages in session state if not already present
                    if f"chat_{chat_id}" not in st.session_state:
                        st.session_state[f"chat_{chat_id}"] = guide_chats[tourist_name]
                    
                    # Display chat messages
                    if not st.session_state[f"chat_{chat_id}"]:
                        st.info(f"No messages with {tourist_name} yet.")
                    else:
                        for msg in st.session_state[f"chat_{chat_id}"]:
                            if msg["sender"] == "tourist":
                                message_container = st.container()
                                with message_container:
                                    col1, col2 = st.columns([1, 4])
                                    with col1:
                                        # Tourist icon
                                        st.markdown("👤")
                                    with col2:
                                        st.markdown(f"**{tourist_name}** - {msg['timestamp']}")
                                        st.markdown(f"{msg['content']}")
                                        st.markdown("---")
                            else:
                                message_container = st.container()
                                with message_container:
                                    col1, col2 = st.columns([4, 1])
                                    with col1:
                                        st.markdown(f"**You** - {msg['timestamp']}")
                                        st.markdown(f"{msg['content']}")
                                        st.markdown("---")
                                    with col2:
                                        # Guide icon
                                        st.markdown("🧭")
                    
                    # Input for reply
                    with st.form(key=f"guide_reply_form_{chat_id}", clear_on_submit=True):
                        reply = st.text_area("Reply to the tourist", key=f"guide_reply_{chat_id}")
                        submit_reply = st.form_submit_button("Send Reply")
                        
                        if submit_reply and reply:
                            # Add reply to chat history
                            new_reply = {
                                "sender": "guide",
                                "sender_name": guide_profile['name'],
                                "content": reply,
                                "timestamp": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            }
                            
                            if f"chat_{chat_id}" not in st.session_state:
                                st.session_state[f"chat_{chat_id}"] = []
                                
                            st.session_state[f"chat_{chat_id}"].append(new_reply)
                            
                            # Save chat to file
                            save_chat_to_file(chat_id, new_reply)
                            st.success("Reply sent!")
                            st.rerun()  # Make sure to use st.rerun() here


# --- Helper function to get all chats for a guide ---
def get_guide_chats(guide_name):
    guide_chats = {}
    
    if not os.path.exists("chats"):
        return guide_chats
        
    # Find all chat files for this guide
    guide_name_formatted = guide_name.replace(' ', '_')
    for filename in os.listdir("chats"):
        if filename.endswith(".json") and guide_name_formatted in filename:
            # Extract tourist name from filename
            tourist_name = filename.split(f"_{guide_name_formatted}.json")[0]
            
            # Load chat messages
            with open(f"chats/{filename}", "r") as f:
                try:
                    messages = json.load(f)
                    guide_chats[tourist_name] = messages
                except json.JSONDecodeError:
                    continue
                    
    return guide_chats

# --- View Destinations ---
def view_destinations():    
    if not st.session_state.logged_in:
        st.warning("Please login first to view destinations.")
        return
        
    state = st.text_input("Enter state to explore")
    if state:
        try:
            if not os.path.exists("data.json"):
                st.error("Destinations file not found.")
                return
                
            with open("data.json", "r") as f:
                destinations = json.load(f)

            found = False
            for dest in destinations:
                if dest["state"].lower() == state.lower():
                    found = True
                    st.markdown(f"### 🌄 {dest['state']}")
                    st.write("**Attractions:**", ", ".join(dest['attractions']))
                    st.write("**Cost:**", dest['cost'])
                    view_guides(state)
            if not found:
                st.warning("No destinations found for the entered state.")
        except FileNotFoundError:
            st.error("Destinations file not found.")
        except Exception as e:
            st.error(f"Error loading destinations: {e}")

# --- View Guides ---
def view_guides(state):
    st.markdown("#### 🧑‍✈️ Available Guides")
    try:
        if not os.path.exists("data1.json"):
            st.info("No guides available yet.")
            return
            
        with open("data1.json", "r") as f:
            guides = json.load(f)
            
        # Filter guides by state
        state_guides = [guide for guide in guides if guide["state"].lower() == state.lower()]
        
        if not state_guides:
            st.info("No guides found for this state.")
            return
            
        # Guide filtering options
        st.subheader("Filter Guides by Preferences")
        
        # Get all available languages from guides
        all_languages = set()
        for guide in state_guides:
            for lang in guide.get('languages', []):
                all_languages.add(lang.strip())
        
        # Language filter
        selected_languages = st.multiselect(
            "Filter by languages", 
            options=sorted(list(all_languages)),
            default=[]
        )
        
        # Gender filter
        gender_filter = st.radio("Filter by gender", ["All", "Male", "Female", "Other"], index=0)
        
        # Apply filters
        filtered_guides = state_guides
        
        # Filter by language if selections made
        if selected_languages:
            filtered_guides = [
                guide for guide in filtered_guides 
                if any(lang.strip() in selected_languages for lang in guide.get('languages', []))
            ]
            
        # Filter by gender if not "All"
        if gender_filter != "All":
            filtered_guides = [
                guide for guide in filtered_guides 
                if guide.get('gender', '') == gender_filter
            ]
            
        # Display filtered guides
        if not filtered_guides:
            st.warning("No guides match your preferences. Try adjusting your filters.")
        else:
            st.markdown("### Guides matching your preferences:")
            for guide in filtered_guides:
                with st.expander(f"**{guide['name']}** | Languages: {', '.join(guide.get('languages', []))}"):
                    st.write(f"**Gender:** {guide.get('gender', 'Not specified')}")
                    st.write(f"**State:** {guide.get('state', 'Not specified')}")
                    st.write(f"**Phone:** {guide.get('phno', 'Not available')}")
                    
                    # Generate a unique key based on guide name
                    button_key = f"select_{guide['name'].replace(' ', '_')}"
                    
                    if st.button(f"Chat with {guide['name']}", key=button_key):
                        st.session_state.selected_guide = guide
                        st.session_state.show_chat = True
                        st.rerun()
                        
    except FileNotFoundError:
        st.warning("Guide data not found.")
    except Exception as e:
        st.error(f"Error loading guide data: {str(e)}")
        st.write("Check if your guide data has the expected format.")

# --- Chat Between Tourist and Guide ---
def chat_with_guide():
    if not st.session_state.get("show_chat", False) or "selected_guide" not in st.session_state:
        return
        
    guide = st.session_state.selected_guide
    tourist_username = st.session_state.username
    
    # Create unique chat ID
    chat_id = f"{tourist_username}_{guide['name'].replace(' ', '_')}"
    
    # Initialize chat messages from file if available
    if f"chat_{chat_id}" not in st.session_state:
        chat_file = f"chats/{chat_id}.json"
        if os.path.exists(chat_file):
            try:
                with open(chat_file, "r") as f:
                    st.session_state[f"chat_{chat_id}"] = json.load(f)
            except json.JSONDecodeError:
                st.session_state[f"chat_{chat_id}"] = []
        else:
            st.session_state[f"chat_{chat_id}"] = []
    
    # Display chat header
    st.markdown(f"### 💬 Chat with {guide['name']}")
    st.write(f"Guide speaks: {', '.join(guide.get('languages', ['English']))}")
    
    # Chat container
    chat_container = st.container()
    
    # Display all messages in the chat
    with chat_container:
        if not st.session_state[f"chat_{chat_id}"]:
            st.info(f"Start chatting with {guide['name']}!")
        else:
            for msg in st.session_state[f"chat_{chat_id}"]:
                if msg["sender"] == "tourist":
                    message_container = st.container()
                    with message_container:
                        col1, col2 = st.columns([1, 4])
                        with col1:
                            # Tourist icon
                            st.markdown("👤")
                        with col2:
                            st.markdown(f"**You** - {msg['timestamp']}")
                            st.markdown(f"{msg['content']}")
                            st.markdown("---")
                else:
                    message_container = st.container()
                    with message_container:
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            st.markdown(f"**{guide['name']}** - {msg['timestamp']}")
                            st.markdown(f"{msg['content']}")
                            st.markdown("---")
                        with col2:
                            # Guide icon
                            st.markdown("🧭")
    
    # Input for new message
    with st.form(key=f"chat_form_{chat_id}", clear_on_submit=True):
        message = st.text_input("Type your message here", key=f"message_input_{chat_id}")
        submit_button = st.form_submit_button("Send")
        
        if submit_button and message:
            # Add message to chat history
            new_message = {
                "sender": "tourist",
                "sender_name": tourist_username,
                "content": message,
                "timestamp": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            }
            st.session_state[f"chat_{chat_id}"].append(new_message)
            
            # Save chat to file
            save_chat_to_file(chat_id, new_message)
            st.success("Message sent!")
            st.rerun()  # Make sure to use st.rerun() here

    # Option to go back to destinations view
    if st.button("Back to Destinations"):
        st.session_state.show_chat = False
        st.rerun()  # Make sure to use st.rerun() here

# --- Save chat messages to file ---
def save_chat_to_file(chat_id, message):
    # Create chats directory if it doesn't exist
    if not os.path.exists("chats"):
        os.makedirs("chats")
        
    chat_file = f"chats/{chat_id}.json"
    
    # Load existing messages
    messages = []
    if os.path.exists(chat_file):
        try:
            with open(chat_file, "r") as f:
                messages = json.load(f)
        except json.JSONDecodeError:
            # If file is corrupted, start fresh
            messages = []
    
    # Add new message
    messages.append(message)
    
    # Save updated messages
    with open(chat_file, "w") as f:
        json.dump(messages, f, indent=4)

# --- Main App Layout ---
def main():
    apply_custom_styles()
    
    # Initialize session state variables
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "role" not in st.session_state:
        st.session_state.role = None
    if "username" not in st.session_state:
        st.session_state.username = None
    if "nav" not in st.session_state:
        st.session_state.nav = "Home"
    if "show_chat" not in st.session_state:
        st.session_state.show_chat = False
    
    # Sidebar navigation based on login state
    st.sidebar.title("🧭 Navigation")
    
    if st.session_state.logged_in:
        # Logged in users see different navigation based on role
        if st.session_state.role == "Tourist":
            nav_options = ["Home", "Tourist Dashboard", "View Destinations", "Logout"]
        elif st.session_state.role == "Guide":
            nav_options = ["Home", "Guide Dashboard", "Logout"]
        elif st.session_state.role == "Admin":
            nav_options = ["Home", "Admin Dashboard", "Logout"]
        else:
            nav_options = ["Home", "Logout"]
            
        nav = st.sidebar.radio("Go to", nav_options, index=nav_options.index(st.session_state.nav) if st.session_state.nav in nav_options else 0)
    else:
        # Not logged in users see limited options
        nav_options = ["Home", "Login", "Register"]
        nav = st.sidebar.radio("Go to", nav_options, index=nav_options.index(st.session_state.nav) if st.session_state.nav in nav_options else 0)
    
    # Update navigation in session state
    st.session_state.nav = nav
    
    # Display user info if logged in
    if st.session_state.logged_in:
        st.sidebar.success(f"Logged in as: {st.session_state.username}")
        st.sidebar.info(f"Role: {st.session_state.role}")

    # Main content container
    with st.container():
        st.markdown("<div class='main-box'>", unsafe_allow_html=True)

        if nav == "Home":
               # Welcome heading
            st.markdown("""
            <div class="main-heading">
            <h2>🌍 Welcome to Tourist Guide Portal</h2>
            <div class="sub-quote">Travel far enough, and you'll find yourself.</div>
         </div>
             """, unsafe_allow_html=True)

    # Sidebar navigation tip
            st.markdown("""
        <div class="custom-info-box">
            🔍 <strong>Navigation Tip:</strong> Use the sidebar to navigate through the options and explore the portal.
        </div>
    """, unsafe_allow_html=True)

    # Login reminder if not logged in
            if not st.session_state.logged_in:
                 st.markdown("""
            <div class="custom-alert-box">
                🔐 <strong>Access Restricted:</strong> Please login or register to unlock all features of the Tourist Guide Portal.
            </div>
        """, unsafe_allow_html=True)

                
        elif nav == "Login":
            login()
            
        elif nav == "Register":
            register()
            
        elif nav == "Tourist Dashboard":
            tourist_dashboard()
            
        elif nav == "Guide Dashboard":
            guide_dashboard()
            
        elif nav == "Admin Dashboard":
            admin_panel()
            
        elif nav == "View Destinations":
            view_destinations()
            
        elif nav == "Logout":
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.role = None
            st.session_state.nav = "Home"
            st.success("You have been logged out.")
            st.rerun()

        # Show chat if a guide is selected
        
        if st.session_state.get("show_chat", False) and "selected_guide" in st.session_state:
                chat_with_guide()    

        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()