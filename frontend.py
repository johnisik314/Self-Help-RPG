import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:5000"  # Base URL for all backend endpoints
AUTH_URL = f"{BACKEND_URL}/auth"
PROFILE_URL = f"{BACKEND_URL}/profile"

# Store the logged-in user's ID in Streamlit's session state
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = None

def register_user():
    st.subheader("Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        if username and password:
            payload = {"username": username, "password": password}
            response = requests.post(f"{AUTH_URL}/register", json=payload)
            if response.status_code == 201:
                st.success("Registration successful! You can now log in.")
            else:
                st.error(f"Registration failed: {response.json().get('message', 'Unknown error')}")
        else:
            st.warning("Please enter a username and password.")

def login_user():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username and password:
            payload = {"username": username, "password": password}
            response = requests.post(f"{AUTH_URL}/login", json=payload)
            if response.status_code == 200:
                st.session_state['user_id'] = response.json().get('user_id')
                st.success(f"Login successful! User ID: {st.session_state['user_id']}")
            else:
                st.error(f"Login failed: {response.json().get('message', 'Unknown error')}")
        else:
            st.warning("Please enter a username and password.")

def display_profile():
    if st.session_state['user_id']:
        st.subheader(f"Profile for User ID: {st.session_state['user_id']}")
        try:
            response = requests.get(f"{PROFILE_URL}/{st.session_state['user_id']}")
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
            profile_data = response.json()
            st.write(f"Username: {profile_data.get('username')}")
            st.write(f"Level: {profile_data.get('level')}")
            st.write(f"Experience: {profile_data.get('experience')}")
            st.write(f"Currency: {profile_data.get('currency')}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching profile: {e}")
    else:
        st.info("Please log in to view your profile.")

def main():
    st.title("Pixel RPG")
    choice = st.sidebar.radio("Select Action", ["Register", "Login", "Profile"])

    if choice == "Register":
        register_user()
    elif choice == "Login":
        login_user()
    elif choice == "Profile":
        display_profile()

if __name__ == "__main__":
    main()
    