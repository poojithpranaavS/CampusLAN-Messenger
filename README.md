##CampusLAN Messenger

CampusLAN Messenger is an offline LAN-based chat application developed using Flask, SQLite, HTML, CSS, and JavaScript. It enables multiple users connected to the same local network (Wi-Fi, hotspot, or campus network) to communicate in real time without requiring an internet connection.

##Features
Real-time messaging across LAN
Multi-user chat support
User login system
Online users panel
Message history storage using SQLite
Mobile and desktop compatibility
Session management
Logout functionality
Works without internet access
Technologies Used
Python
Flask
SQLite
HTML5
CSS3
JavaScript

##Project Structure
CampusLAN-Messenger/
│
├── app.py
├── chat.db
│
├── templates/
│   ├── login.html
│   └── chat.html
│
├── static/
│   ├── style.css
│   └── chat.js
│
└── README.md

##Installation
  Clone the repository:
    git clone https://github.com/poojithpranaavS/CampusLAN-Messenger.git
    cd CampusLAN-Messenger
  
  Install Flask:
    pip install flask

  Run the application:
    python app.py

  The application will start on:
    http://127.0.0.1:5000

##LAN Access

To access the messenger from other devices connected to the same network:
 1. Find the host system's IP address.
 2. Run the Flask server.
 3. Open the following URL on another device:
      http://YOUR_LOCAL_IP:5000
    
