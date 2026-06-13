from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "offline_chat_secret"


# =========================
# DATABASE INITIALIZATION
# =========================

def init_db():

    conn = sqlite3.connect("chat.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        message TEXT,
        timestamp TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE
    )
    """)

    conn.commit()
    conn.close()


init_db()


# =========================
# LOGIN PAGE
# =========================

@app.route("/")
def login():
    return render_template("login.html")


# =========================
# JOIN CHAT
# =========================

@app.route("/join", methods=["POST"])
def join():

    username = request.form["username"].strip()

    if username == "":
        return redirect("/")

    conn = sqlite3.connect("chat.db")
    c = conn.cursor()

    c.execute(
        "INSERT OR IGNORE INTO users(username) VALUES(?)",
        (username,)
    )

    c.execute("""
        INSERT INTO messages
        (username, message, timestamp)
        VALUES (?, ?, ?)
    """, (
        "SYSTEM",
        f"{username} joined the chat",
        datetime.now().strftime("%H:%M:%S")
    ))

    conn.commit()
    conn.close()

    session["username"] = username

    return redirect("/chat")


# =========================
# CHAT PAGE
# =========================

@app.route("/chat")
def chat():

    if "username" not in session:
        return redirect("/")

    return render_template(
        "chat.html",
        username=session["username"]
    )


# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():

    if "username" in session:

        username = session["username"]

        conn = sqlite3.connect("chat.db")
        c = conn.cursor()

        c.execute("""
            INSERT INTO messages
            (username, message, timestamp)
            VALUES (?, ?, ?)
        """, (
            "SYSTEM",
            f"{username} left the chat",
            datetime.now().strftime("%H:%M:%S")
        ))

        conn.commit()
        conn.close()

    session.clear()

    return redirect("/")


# =========================
# SEND MESSAGE
# =========================

@app.route("/send", methods=["POST"])
def send():

    if "username" not in session:
        return jsonify({"error": "Unauthorized"})

    data = request.json

    conn = sqlite3.connect("chat.db")
    c = conn.cursor()

    c.execute("""
        INSERT INTO messages
        (username, message, timestamp)
        VALUES (?, ?, ?)
    """, (
        session["username"],
        data["message"],
        datetime.now().strftime("%H:%M:%S")
    ))

    conn.commit()
    conn.close()

    return jsonify({"status": "success"})


# =========================
# GET MESSAGES
# =========================

@app.route("/messages")
def messages():

    conn = sqlite3.connect("chat.db")
    c = conn.cursor()

    c.execute("""
        SELECT username, message, timestamp
        FROM messages
        ORDER BY id ASC
    """)

    rows = c.fetchall()

    conn.close()

    return jsonify(rows)


# =========================
# GET USERS
# =========================

@app.route("/users")
def users():

    conn = sqlite3.connect("chat.db")
    c = conn.cursor()

    c.execute("""
        SELECT DISTINCT username
        FROM messages
        WHERE username != 'SYSTEM'
        ORDER BY username
    """)

    users = c.fetchall()

    conn.close()

    return jsonify(users)


# =========================
# CLEAR CHAT (OPTIONAL)
# =========================

@app.route("/clear")
def clear_chat():

    conn = sqlite3.connect("chat.db")
    c = conn.cursor()

    c.execute("DELETE FROM messages")

    conn.commit()
    conn.close()

    return redirect("/chat")


# =========================
# RUN APP
# =========================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )