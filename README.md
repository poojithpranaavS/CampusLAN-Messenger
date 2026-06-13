## 📌 Project Overview

Campus LAN Messenger is a lightweight chat platform designed for campus environments where users can join a common chat room and exchange messages in real time without an internet connection or a cellular data.

The application uses JWT-based authentication to secure API endpoints and Neon PostgreSQL for persistent cloud-based message storage.

## ✨ Features
🔐 JWT Authentication
- Secure token-based authentication
- Protected API endpoints
- User verification before accessing chat services
💬 Real-Time Chat
- Send and receive messages instantly
- Auto-refresh message updates
- Common chat room for all users
👥 User Management
- Join using a username
- Online users list
- Join/leave system notifications
🗄 Persistent Cloud Storage
- Messages stored in Neon PostgreSQL
- Data persists across refreshes and deployments
- Cloud-hosted database integration
🌐 Cloud Deployment
- Hosted on Vercel
- Accessible from anywhere
- Automatic deployment through GitHub

## 🛠 Tech Stack
- Technology	Purpose
- Flask	Backend Framework
- HTML	Structure
- CSS	Styling
- JavaScript	Frontend Functionality
- JWT	Authentication
- PostgreSQL	Database
- Neon	Cloud Database Provider
- Vercel	Deployment Platform
- Git & GitHub	Version Control

## 📂 Project Structure

```text
CampusLAN-Messenger/
│
├── app.py
├── requirements.txt
├── vercel.json
├── README.md
│
├── templates/
│   ├── login.html
│   └── chat.html
│
├── static/
│   ├── style.css
│   ├── login.css
│   └── chat.js
```

## 🔑 Authentication Flow
- User enters a username.
- Flask generates a JWT token.
- Token is stored in the session.
- Protected routes verify the JWT.
- Authorized users can send and receive messages.

## 🗃 Database Schema
  # Users Table
     CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE
   );
  # Messages Table 
     CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100),
    message TEXT,
    timestamp VARCHAR(20)
   );

## ⚙ Installation & Setup
   # Clone Repository
     git clone https://github.com/poojithpranaavS/CampusLAN-Messenger.git
     cd CampusLAN-Messenger
   # Create Virtual Environment
     python -m venv venv
 # Activate Environment
   # Windows:
     venv\Scripts\activate
   # Linux / Mac:
     source venv/bin/activate
 # Install Dependencies
    pip install -r requirements.txt

## 🔧 Environment Variables
  Create a file named:
     .env.local
  Add:
     DATABASE_URL=YOUR_NEON_DATABASE_URL

## ▶ Running Locally
    python app.py
   Open:
     http://127.0.0.1:5000

## ☁ Deployment
 # Backend Hosting
   * Vercel
 # Database
   * Neon PostgreSQL
 # Deployment Workflow
       GitHub
         ↓
       Vercel
         ↓
     Neon PostgreSQL

## 🔒 Security Features
- JWT Authentication
- Protected API Routes
- Secure Session Handling
- Environment Variable Configuration
- Rotated Database Credentials
- Cloud Database Security

## 🎯 Future Enhancements
- Private Messaging
- Group Chats
- File Sharing
- Message Reactions
- User Profiles
- WebSocket-based Real-Time Communication
- End-to-End Encryption

## 👨‍💻 Developer

 # Poojith Pranaav

 # Campus LAN Messenger – Secure Cloud-Based Chat Application

## 📜 License

  # This project is developed for educational and academic purposes.
