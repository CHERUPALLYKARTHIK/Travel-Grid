import json
import streamlit as st
from datetime import datetime

# Load data from JSON files
def load_data():
    with open("data.json", "r") as file:
        destinations = json.load(file)
    with open("data1.json", "r") as file:
        tourists_guides = json.load(file)
    return destinations, tourists_guides

# Save updated data to JSON files
def save_data(destinations, tourists_guides):
    with open("data.json", "w") as file:
        json.dump(destinations, file, indent=4)
    with open("data1.json", "w") as file:
        json.dump(tourists_guides, file, indent=4)

# Register Guide
def register_guide(tourists_guides):
    st.title("Guide Registration")
    
    guide_name = st.text_input("Enter Full Name")
    state = st.text_input("Enter State")
    languages = st.text_input("Enter Languages (comma separated)")
    phone = st.text_input("Enter Phone Number")
    
    if st.button("Register Guide"):
        guide_username = guide_name.lower().replace(" ", "_")
        if guide_username in tourists_guides:
            st.error("Guide already exists!")
        else:
            new_guide = {
                "name": guide_name,
                "state": state,
                "languages": [lang.strip() for lang in languages.split(",")],
                "phno": phone,
                "unavailable_dates": []
            }
            tourists_guides[guide_username] = new_guide
            save_data(load_data()[0], tourists_guides)
            st.success(f"Guide {guide_name} registered successfully!")

# Admin Login
def admin_login():
    st.title("Admin Login")
    admin_username = st.text_input("Enter Admin Username")
    admin_password = st.text_input("Enter Admin Password", type="password")
    
    if st.button("Login"):
        if admin_username == "admin" and admin_password == "admin123":  # Example admin credentials
            st.session_state.is_admin = True
            st.success("Logged in successfully as Admin!")
        else:
            st.error("Invalid credentials!")

# Admin Panel
def admin_panel(tourists_guides):
    st.title("Admin Panel")
    
    st.subheader("Manage Guide Profiles")
    for guide_username, profile in tourists_guides.items():
        st.write(f"{profile['name']} - {profile['state']}")
        st.write(f"Languages: {', '.join(profile['languages'])}")
        st.write(f"Phone: {profile['phno']}")
        
        # Option to mark guide as unavailable for certain days
        unavailable_dates = st.date_input(f"Unavailable dates for {profile['name']}", [])
        profile['unavailable_dates'] = unavailable_dates
        save_data(load_data()[0], tourists_guides)
        
        st.write("")

# Display Available Destinations
def display_destinations(destinations):
    st.title("Explore Destinations")
    state = st.text_input("Enter state name to explore destinations (leave blank for all)")
    
    st.subheader("Available Destinations")
    found = False
    for destination in destinations:
        if not state or destination["state"].lower() == state.lower():
            found = True
            st.write(f"State: {destination['state']}")
            st.write(f"Attractions: {', '.join(destination['attractions'])}")
            st.write(f"Approximate Cost: Rs. {destination['cost']}")
    
    if not found:
        st.write("No destinations found for the entered state.")
        
# Display and Select Guide
def display_and_select_guide(tourists_guides):
    st.title("Select Your Guide")
    state = st.text_input("Enter state to find guides")
    if state:
        st.write(f"Guides available in {state}:")
        available_guides = [guide for guide in tourists_guides.values() if guide['state'].lower() == state.lower()]
        
        if available_guides:
            selected_guide_name = st.selectbox("Select a guide", [guide['name'] for guide in available_guides])
            selected_guide = next(guide for guide in available_guides if guide['name'] == selected_guide_name)
            
            st.write(f"You selected {selected_guide['name']} as your guide.")
            
            unavailable_dates = selected_guide.get('unavailable_dates', [])
            date = st.date_input("Choose date for booking", datetime.today())
            
            if st.button("Book Guide"):
                if date in unavailable_dates:
                    st.error("The guide is not available on this date.")
                else:
                    st.success("Booking successful!")
                    # Mark guide as unavailable for the selected date
                    selected_guide['unavailable_dates'].append(date)
                    save_data(load_data()[0], tourists_guides)
        else:
            st.write("No guides available for this state.")

# Main App Layout
def main():
    destinations, tourists_guides = load_data()
    
    if 'is_admin' not in st.session_state:
        st.session_state.is_admin = False
    
    st.set_page_config(page_title="Tourist Guide System", page_icon="🗺️", layout="wide")
    
    # Custom CSS for a better UI
    st.markdown("""
        <style>
            .main {
                background-image: url('https://www.w3schools.com/w3images/forest.jpg');
                background-size: cover;
                color: #fff;
                font-family: Arial, sans-serif;
            }
            .stButton > button {
                background-color: #00aaff;
                color: white;
                border-radius: 8px;
                font-size: 16px;
                width: 100%;
                height: 40px;
            }
            .stButton > button:hover {
                background-color: #0099cc;
            }
            .stTitle {
                color: #fff;
                font-size: 32px;
            }
            .stTextInput, .stSelectbox {
                background-color: rgba(255, 255, 255, 0.7);
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
            }
            .stSelectbox, .stTextInput {
                margin-top: 10px;
            }
            .stButton {
                margin-top: 20px;
            }"""
        </style>
    , unsafe_allow_html=True)
    
    st.sidebar.title("Tourist Guide")
    app_mode = st.sidebar.selectbox("Select Mode", ["Admin", "Guide Registration", "View Destinations", "Select Guide"])
    
    if app_mode == "Admin":
        if not st.session_state.is_admin:
            admin_login()
        else:
            admin_panel(tourists_guides)
    
    elif app_mode == "Guide Registration":
        register_guide(tourists_guides)
    
    elif app_mode == "View Destinations":
        display_destinations(destinations)
    
    elif app_mode == "Select Guide":
        display_and_select_guide(tourists_guides)

if __name__ == "__main__":
    main()
