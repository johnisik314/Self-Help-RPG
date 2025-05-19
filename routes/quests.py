from flask import Blueprint, jsonify, request
import pandas as pd
import os

quests_bp = Blueprint('quests', __name__, url_prefix='/quests')

# Path to your Excel file
EXCEL_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'quests.xlsx')

def get_all_quests():
    """Reads all quests from the Excel file."""
    try:
        df = pd.read_excel(EXCEL_FILE_PATH)
        # Convert DataFrame to a list of dictionaries, handling NaN values
        quests = df.fillna('').to_dict('records')
        return quests
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None

def get_quest_by_id(quest_id):
    """Retrieves a specific quest from the Excel file by its ID."""
    quests = get_all_quests()
    if quests:
        for quest in quests:
            if quest.get('id') == quest_id:
                return quest
    return None

# --- API Endpoints (You will need to fill in the logic for each) ---

@quests_bp.route('/new', methods=['GET'])
def get_new_quests():
    """Returns three random quests."""
    quests = get_all_quests()
    if quests:
        import random
        if len(quests) >= 3:
            random_quests = random.sample(quests, 3)
            return jsonify(random_quests)
        else:
            return jsonify({"message": "Not enough quests available"}), 404
    else:
        return jsonify({"message": "Could not load quests"}), 500

@quests_bp.route('', methods=['POST'])
def add_quest_to_user():
    """Adds a selected quest to the user's active quest list."""
    data = request.get_json()
    quest_template_id = data.get('quest_template_id')
    # --- Your logic here:
    # 1. Get the logged-in user (you'll need to implement user identification).
    # 2. Retrieve the quest details from the Excel file based on quest_template_id.
    # 3. Store this quest as active for the user (you'll need a way to manage active quests, e.g., in memory or a temporary file).
    # 4. Return a success or error message.
    return jsonify({"message": "Adding quest to user - Logic to be implemented"}), 200

@quests_bp.route('', methods=['GET'])
def get_user_quests():
    """Returns the list of active quests for the logged-in user."""
    # --- Your logic here:
    # 1. Get the logged-in user.
    # 2. Retrieve the list of their active quests.
    # 3. For each active quest ID, fetch the full details from the Excel file.
    # 4. Return the list of active quests with their details.
    return jsonify({"message": "Getting user quests - Logic to be implemented"}), 200

@quests_bp.route('/<int:user_quest_id>', methods=['DELETE'])
def delete_user_quest(user_quest_id):
    """Deletes a specific quest from the user's active quest list."""
    # --- Your logic here:
    # 1. Get the logged-in user.
    # 2. Identify the active quest to delete based on user_quest_id (this ID needs to be managed by your active quest system).
    # 3. Remove the quest from the user's active quest list.
    # 4. Return a success or error message.
    return jsonify({"message": f"Deleting user quest {user_quest_id} - Logic to be implemented"}), 200

@quests_bp.route('/<int:user_quest_id>/complete', methods=['POST'])
def complete_user_quest(user_quest_id):
    """Marks a user's quest as complete and awards rewards."""
    # --- Your logic here:
    # 1. Get the logged-in user.
    # 2. Identify the completed active quest based on user_quest_id.
    # 3. Retrieve the quest details and rewards from the Excel file.
    # 4. Award XP and gold to the user (you'll need to update the user model/data).
    # 5. Check for level up.
    # 6. Remove the quest from the user's active quest list.
    # 7. Return a success message with the rewards and level up info.
    return jsonify({"message": f"Completing user quest {user_quest_id} - Logic to be implemented"}), 200