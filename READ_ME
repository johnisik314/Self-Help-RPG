## Documentation

### User Authentication

- **Registration (`/register`):** Allows new users to create an account by providing a username and password. User credentials (username and a hashed password) are stored in the `site.db` SQLite database using Flask-SQLAlchemy.
- **Login (`/login`):** Authenticates existing users by verifying their username and password against the data in `site.db`. Upon successful login, the user's ID is stored in a session.

### Quests System

- **Quest Data:** Quest definitions (name, description, rewards) are loaded from the `quests.xlsx` file using the pandas library.
- **New Quests (`/new_quests`):** Fetches a random selection of quests from the Excel file and renders them in `new_quests_partial.html`.
- **Accepting Quests (`/accept_quest/<quest_id>`):** When a user clicks "Accept," the `quest_id` is added to the `active_quests` list within the user's data in `user_data.json`.
- **Active Quests (`/quests_data`):** Retrieves the user's active quest IDs from `user_data.json`, fetches the corresponding quest details from `quests.xlsx`, and renders them in `quests_list_partial.html`.
- **Completing Quests (`/complete_quest/<quest_id>`):** When a user clicks "Completed":
    - The rewards (gold and XP) from the completed quest are added to the user's data in `user_data.json`.
    - The `quest_id` is moved from the `active_quests` list to the `completed_quests` list in `user_data.json`.
    - The completed quest details are saved to `completed_quests.json`.
    - The user's level is checked and potentially increased based on accumulated XP.
- **Deleting Quests (`/delete_quest/<quest_id>`):** When a user clicks "X," the `quest_id` is removed from the `active_quests` list in `user_data.json`.

### Profile Management

- **Profile Display (`/profile`):** Fetches the user's data from `user_data.json` and displays their username, level, experience, and currency.
- **Dashboard (`/dashboard`):** The main user interface displaying a summary of the user's profile and navigation buttons.

### Leveling System

- Experience points (XP) are awarded upon completing quests.
- A base experience threshold is defined for leveling up (currently 100 XP for level 2).
- The experience required for each subsequent level increases by 5%.
- The `complete_quest` route checks for level-ups after awarding XP and updates the user's level in `user_data.json`.

### Data Storage

- **`user_data.json`:** Stores dynamic user-specific information, including level, experience, currency, and lists of active and completed quest IDs.
- **`quests.xlsx`:** Contains the static definitions for all available quests in the game.
- **`site.db`:** An SQLite database used by Flask-SQLAlchemy to store user authentication details (usernames and hashed passwords).
- **`completed_quests.json`:** Stores a history of all quests completed by users, including the user ID and the quest details.

### Frontend Interaction

- **`dashboard.html`:** The main layout with buttons to navigate to different sections.
- **JavaScript (`static/dashboard.js`):** Handles dynamic fetching of content for different sections (profile, quests) and interacts with the backend to accept and complete/delete quests without full page reloads.
- **HTML Partials (`templates/*.html`):** Smaller HTML snippets loaded into the `content-area` of `dashboard.html` to display specific data (e.g., profile information, lists of quests).

## Future Enhancements

- **Bingo Feature:** Implement a bingo board with self-improvement tasks.
- **To-Do List:** Allow users to create and manage their own custom tasks.
- **More Complex Quest Types:** Introduce quests with different requirements and mechanics.
- **Skill System:** Implement skills that can be improved with experience and affect gameplay.
- **Inventory System:** Allow users to acquire and manage virtual items.
- **User Interface Improvements:** Enhance the visual design and user experience.
- **Database Migration:** Transition from JSON and Excel to a more robust database system (e.g., PostgreSQL, MySQL).
- **More Sophisticated Leveling Curve:** Implement a more nuanced experience point progression.

## Contributing

Contributions to the Self-Help RPG project are welcome! If you have suggestions, bug reports, or would like to contribute code, please:

1.  Fork the repository on GitHub.
2.  Create a new branch for your changes (`git checkout -b feature/your-feature` or `git checkout -b bugfix/your-fix`).
3.  Commit your changes (`git commit -am 'Add some feature'`).
4.  Push to the branch (`git push origin feature/your-feature`).
5.  Create a pull request on GitHub.

Please follow any existing code style and conventions.

## Copyright Notice

© 2025 John Isik. All Rights Reserved.

This project and its contents are proprietary and protected by copyright law. No part of this project may be used, reproduced, distributed, or modified in any form or by any means without the express written permission of the copyright holder.

Any unauthorized use, reproduction, distribution, or modification of this project may result in legal action.

For inquiries regarding permission to use this project, please contact johnisik314@gmail.com.
