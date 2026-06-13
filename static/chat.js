async function loadMessages() {

    let response = await fetch("/messages");

    let data = await response.json();

    let box = document.getElementById("messages");

    if (!box) return;

    box.innerHTML = "";

    const currentUser =
        document.querySelector(".header").innerText
        .replace("Welcome, ", "")
        .trim();

    if (!Array.isArray(data)) {
        console.error("Messages Error:", data);
        return;
    }

    data.forEach(msg => {

        let username = msg[0];
        let message = msg[1];
        let timestamp = msg[2];

        let messageClass;

        if (username === "SYSTEM") {
            messageClass = "system-message";
        }
        else if (username === currentUser) {
            messageClass = "my-message";
        }
        else {
            messageClass = "other-message";
        }

        box.innerHTML += `
            <div class="${messageClass}">
                <div class="msg-user">${username}</div>
                <div>${message}</div>
                <small>${timestamp}</small>
            </div>
        `;
    });

    box.scrollTop = box.scrollHeight;
}


async function sendMessage() {

    let input = document.getElementById("messageInput");

    if (!input) return;

    let text = input.value.trim();

    if (text === "") return;

    let response = await fetch("/send", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            message: text
        })
    });

    let result = await response.json();

    if (result.error) {
        console.error(result.error);
        return;
    }

    input.value = "";

    loadMessages();
}


async function loadUsers() {

    let response = await fetch("/users");

    let users = await response.json();

    let box = document.getElementById("usersList");

    if (!box) return;

    box.innerHTML = "";

    if (!Array.isArray(users)) {
        console.error("Users Error:", users);
        return;
    }

    let countElement = document.getElementById("userCount");

    if (countElement) {
        countElement.innerText = `Online Users (${users.length})`;
    }

    users.forEach(user => {

        let username =
            Array.isArray(user)
            ? user[user.length - 1]
            : user;

        box.innerHTML += `
            <div class="user">
                🟢 ${username}
            </div>
        `;
    });
}


const messageInput = document.getElementById("messageInput");

if (messageInput) {

    messageInput.addEventListener("keypress", function(e) {

        if (e.key === "Enter") {
            sendMessage();
        }

    });

}


setInterval(loadMessages, 1000);
setInterval(loadUsers, 2000);

loadMessages();
loadUsers();