import requests

BACKEND_URL = "http://127.0.0.1:5000"
AUTH_URL = f"{BACKEND_URL}/auth"
PROFILE_URL = f"{BACKEND_URL}/profile"

def register_user():
    print("\n--- Register ---")
    username = input("Username: ")
    password = input("Password: ")
    payload = {"username": username, "password": password}
    try:
        response = requests.post(f"{AUTH_URL}/register", json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        print("Registration successful!")
    except requests.exceptions.RequestException as e:
        print(f"Registration failed: {response.json().get('message', e)}")

def login_user():
    print("\n--- Login ---")
    username = input("Username: ")
    password = input("Password: ")
    payload = {"username": username, "password": password}
    try:
        response = requests.post(f"{AUTH_URL}/login", json=payload)
        response.raise_for_status()
        data = response.json()
        user_id = data.get('user_id')
        print("Login successful!")
        return user_id
    except requests.exceptions.RequestException as e:
        print(f"Login failed: {response.json().get('message', e)}")
        return None

def display_profile(user_id):
    if user_id:
        print("\n--- Profile ---")
        try:
            response = requests.get(f"{PROFILE_URL}/{user_id}")
            response.raise_for_status()
            profile_data = response.json()
            print(f"User ID: {profile_data.get('id')}")
            print(f"Username: {profile_data.get('username')}")
            print(f"Level: {profile_data.get('level')}")
            print(f"Experience: {profile_data.get('experience')}")
            print(f"Currency: {profile_data.get('currency')}")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching profile: {e}")
    else:
        print("Not logged in. Cannot display profile.")

def main():
    while True:
        print("\nPixel RPG - Command Line UI")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            register_user()
        elif choice == '2':
            user_id = login_user()
            if user_id:
                display_profile(user_id)
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()