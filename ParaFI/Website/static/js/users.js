document.getElementById('newUserForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const username = document.getElementById('newUsername').value;
    const password = document.getElementById('newPassword').value;

    fetch('/create-user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username: username, password: password })
    })
    .then(response => {
        if (!response.ok) throw new Error('Failed to create user');
        return response.json();
    })
    .then(data => {
        alert('User created successfully');
        window.location.reload();  // Reload the page to update the list of users
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to create user: ' + error.message);
    });
});

function editUser(index, username, password) {
    console.log(`Edit user called with index: ${index}, username: ${username}`);
    const usernameInput = document.getElementById(`username-${index}`);
    const passwordInput = document.getElementById(`password-${index}`);

    if (usernameInput.readOnly) {
        usernameInput.readOnly = false;
        passwordInput.readOnly = false;
        usernameInput.focus();
        console.log('Inputs are now editable');
    } else {
        // Save the edited values
        const newUsername = usernameInput.value;
        const newPassword = passwordInput.value;
        console.log(`Saving new values - Username: ${newUsername}, Password: ${newPassword}`);

        fetch(`/update-user`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ oldUsername: username, username: newUsername, password: newPassword })
        })
        .then(response => {
            if (!response.ok) throw new Error('Failed to update user');
            return response.json();
        })
        .then(data => {
            console.log(data.message);
            alert('Changes saved successfully');
            usernameInput.readOnly = true;
            passwordInput.readOnly = true;
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to save changes: ' + error.message);
        });
    }
}

function deleteUser(username) {
    if (confirm(`Are you sure you want to delete ${username}?`)) {
        fetch('/delete-user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username: username })
        })
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            alert(data.message);
            window.location.reload(); // Reload the page to refresh the list
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error: ' + error.message);
        });
    }
}
