from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import os
import random
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    # Add other user-related fields as needed

USER_DATA_JSON_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'user_data.json')
EXCEL_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'quests.xlsx')

def get_all_quests_from_excel():
    try:
        df = pd.read_excel(EXCEL_FILE_PATH)
        return df.to_dict('records')
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Error reading Excel: {e}")
        return []

def get_user_data_from_json(user_id):
    try:
        with open(USER_DATA_JSON_FILE, 'r') as f:
            users_data = json.load(f)
            for user_data in users_data:
                if user_data['user_id'] == user_id:
                    # Ensure 'active_quests' and 'completed_quests' keys exist
                    if 'active_quests' not in user_data:
                        user_data['active_quests'] = []
                    if 'completed_quests' not in user_data:
                        user_data['completed_quests'] = []
                    return user_data
            return None
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None
    except Exception as e:
        print(f"Error reading user data JSON: {e}")
        return None

def save_user_data_to_json(user_data):
    try:
        with open(USER_DATA_JSON_FILE, 'r') as f:
            users_data = json.load(f)
    except FileNotFoundError:
        users_data = []
    except json.JSONDecodeError:
        users_data = []
    except Exception as e:
        print(f"Error reading user data JSON: {e}")
        return

    updated = False
    for i, existing_user in enumerate(users_data):
        if existing_user['user_id'] == user_data['user_id']:
            users_data[i] = user_data
            updated = True
            break
    if not updated:
        users_data.append(user_data)

    try:
        with open(USER_DATA_JSON_FILE, 'w') as f:
            json.dump(users_data, f, indent=4)
        print(f"Saved user data for user {user_data['user_id']} to {USER_DATA_JSON_FILE}")
    except Exception as e:
        print(f"Error saving user data JSON: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        from werkzeug.security import generate_password_hash
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return render_template('register.html', error='Username and password are required')

        with app.app_context():  # Ensure we're in the Flask app context
            if User.query.filter_by(username=username).first():
                return render_template('register.html', error='User with that username already exists')

            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password_hash=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            # Initialize user data in JSON
            user_data = {'user_id': new_user.id, 'username': new_user.username, 'level': 1, 'experience': 0, 'currency': 0, 'active_quests': [], 'completed_quests': []}
            save_user_data_to_json(user_data)

            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        from werkzeug.security import check_password_hash
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return render_template('login.html', error='Username and password are required')

        with app.app_context():
            user_from_db = User.query.filter_by(username=username).first()

            if user_from_db and check_password_hash(user_from_db.password_hash, password):
                session['user_id'] = user_from_db.id
                user_data = get_user_data_from_json(user_from_db.id)
                if not user_data:
                    user_data = {'user_id': user_from_db.id, 'username': user_from_db.username, 'level': 1, 'experience': 0, 'currency': 0, 'active_quests': [],'completed_quests': []}
                    save_user_data_to_json(user_data)
                return render_template('dashboard.html', user=user_data)
            else:
                return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/dashboard/<int:user_id>')
def dashboard(user_id):
    user_data = get_user_data_from_json(user_id)
    if user_data:
        return render_template('dashboard.html', user=user_data)
    else:
        return redirect(url_for('index'))

@app.route('/profile')
def profile():
    user_id = session.get('user_id')
    user_data = get_user_data_from_json(user_id)
    if user_data:
        return render_template('profile.html', user=user_data)
    else:
        return redirect(url_for('index')) # Or handle error appropriately

@app.route('/quests_data')
def quests_data():
    user_id = session.get('user_id')
    user_data = get_user_data_from_json(user_id)
    if user_data:
        active_quest_ids = user_data.get('active_quests', [])
        all_quests = get_all_quests_from_excel()
        active_quests_data = [quest for quest in all_quests if quest['Quest ID'] in active_quest_ids]
        return render_template('quests_list_partial.html', quests=active_quests_data)
    else:
        return render_template('quests_list_partial.html', quests=[])

@app.route('/new_quests')
def new_quests():
    all_quests = get_all_quests_from_excel()
    if len(all_quests) >= 3:
        random_quests = random.sample(all_quests, 3)
        return render_template('new_quests_partial.html', new_quests=random_quests)
    else:
        return render_template('new_quests_partial.html', new_quests=[])

@app.route('/accept_quest/<int:quest_id>')
def accept_quest(quest_id):
    user_id = session.get('user_id')
    user_data = get_user_data_from_json(user_id)
    if user_data:
        if quest_id not in user_data['active_quests']:
            user_data['active_quests'].append(quest_id)
            save_user_data_to_json(user_data)
    return quests_data()

@app.route('/complete_quest/<int:quest_id>')
def complete_quest(quest_id):
    user_id = session.get('user_id')
    user_data = get_user_data_from_json(user_id)
    all_quests = get_all_quests_from_excel()
    base_level_up_threshold = 100  # Experience needed to reach level 2
    level_up_increase_rate = 0.05  # 5% increase per level
    completed_quest = None

    if user_data and 'active_quests' in user_data:
        if quest_id in user_data['active_quests']:
            quest_to_complete = next((q for q in all_quests if q['Quest ID'] == quest_id), None)
            if quest_to_complete:
                # Award rewards
                user_data['currency'] += quest_to_complete.get('Gold Reward', 0)
                user_data['experience'] += quest_to_complete.get('XP Reward', 0)
                # Check for level up
                while True:
                    required_experience_for_next_level = int(base_level_up_threshold * (1 + level_up_increase_rate)**(user_data['level'] - 1))
                    if user_data['experience'] >= required_experience_for_next_level:
                        user_data['level'] += 1
                        # You can choose to subtract the required amount or keep the accumulated excess XP
                        user_data['experience'] -= required_experience_for_next_level
                    else:
                        break  # Not enough XP to level up
                # Move to completed quests
                user_data['completed_quests'].append(quest_id)
                user_data['active_quests'].remove(quest_id)
                save_user_data_to_json(user_data)
                
                return jsonify(user_data) # Return updated user data for potential frontend update
    return jsonify(user_data) # Return current user data if quest not found or couldn't be completed

@app.route('/delete_quest/<int:quest_id>')
def delete_quest(quest_id):
    user_id = session.get('user_id')
    user_data = get_user_data_from_json(user_id)
    if user_data and 'active_quests' in user_data:
        if quest_id in user_data['active_quests']:
            user_data['active_quests'].remove(quest_id)
            save_user_data_to_json(user_data)
    return "Quest Deleted" # Simple response

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist
    app.run(debug=True)