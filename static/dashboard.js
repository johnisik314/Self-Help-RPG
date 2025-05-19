document.addEventListener('DOMContentLoaded', function() {
    const profileBtn = document.getElementById('profile-btn');
    const questsBtn = document.getElementById('quests-btn');
    const newQuestBtn = document.getElementById('new-quest-btn'); // Get the "New Quest" button
    const contentArea = document.getElementById('content-area');
    // const activeQuestsArea = document.getElementById('active-quests-area'); // May not be directly used now
    // const newQuestsArea = document.getElementById('new-quests-area');   // May not be directly used now

    if (profileBtn) {
        profileBtn.addEventListener('click', function() {
            fetch('/profile')
                .then(response => response.text())
                .then(data => {
                    contentArea.innerHTML = data;
                });
        });
    }

    if (questsBtn) {
        questsBtn.addEventListener('click', function() {
            fetch('/quests_data')
                .then(response => response.text())
                .then(data => {
                    contentArea.innerHTML = data;
                });
        });
    }

    if (newQuestBtn) {
        newQuestBtn.addEventListener('click', function() {
            contentArea.innerHTML = ''; // Clear the content-area
            fetch('/new_quests_screen')
                .then(response => response.text())
                .then(data => {
                    contentArea.innerHTML = data; // Load the new quest screen
                });
        });
    }

    if (contentArea) {
        contentArea.addEventListener('click', function(event) {
            if (event.target && event.target.classList.contains('accept-quest-btn')) {
                const questId = event.target.dataset.questId;
                fetch(`/accept_quest/${questId}`)
                    .then(response => response.text())
                    .then(data => {
                        fetch('/quests_data')
                            .then(response => response.text())
                            .then(data => {
                                contentArea.innerHTML = data;
                            });
                    });
            } else if (event.target && event.target.classList.contains('complete-quest-btn')) {
                const questId = event.target.dataset.questId;
                fetch(`/complete_quest/${questId}`)
                    .then(response => response.json()) // Expect JSON response with updated user data
                    .then(updatedUserData => {
                        // Update the displayed profile information (basic example)
                        const levelElement = document.querySelector('#content-area p:nth-child(3)');
                        const experienceElement = document.querySelector('#content-area p:nth-child(4)');
                        const currencyElement = document.querySelector('#content-area p:nth-child(5)');
                        if (levelElement && updatedUserData && updatedUserData.level !== undefined) levelElement.textContent = `Level: ${updatedUserData.level}`;
                        if (experienceElement && updatedUserData && updatedUserData.experience !== undefined) experienceElement.textContent = `Experience: ${updatedUserData.experience}`;
                        if (currencyElement && updatedUserData && updatedUserData.currency !== undefined) currencyElement.textContent = `Currency: ${updatedUserData.currency}`;

                        // Directly trigger a click on the "Quests" button to reload the list
                        const questsButton = document.getElementById('quests-btn');
                        if (questsButton) {
                            questsButton.click();
                        }
                    });
            } else if (event.target && event.target.classList.contains('delete-quest-btn')) {
                const questId = event.target.dataset.questId;
                fetch(`/delete_quest/${questId}`)
                    .then(response => response.text())
                    .then(data => {
                        // Reload the quest list to remove the deleted quest
                        return fetch('/quests_data');
                    })
                    .then(response => response.text())
                    .then(data => {
                        contentArea.innerHTML = data;
                    });
            }
        });
    }
});