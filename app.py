from flask import Flask, render_template, request, redirect, session, jsonify
import os
import jwt
import psycopg2

from dotenv import load_dotenv
from functools import wraps
from datetime import datetime

load_dotenv(".env.local")

app = Flask(__name__)
app.secret_key = "offline_chat_secret"

JWT_SECRET = "campuslan_jwt_secret"
DATABASE_URL = os.getenv("DATABASE_URL")

print("DATABASE_URL =", DATABASE_URL)


# =========================
# JWT HELPERS
# =========================

def create_token(username):

    return jwt.encode(
        {
            "username": username
        },
        JWT_SECRET,
        algorithm="HS256"
    )


def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        token = session.get("token")

        if not token:
            return jsonify({
                "error": "Token missing"
            }), 401

        try:

            data = jwt.decode(
                token,
                JWT_SECRET,
                algorithms=["HS256"]
            )

            request.username = data["username"]

        except Exception as e:

            return jsonify({
                "error": str(e)
            }), 401

        return f(*args, **kwargs)

    return decorated


# =========================
# DATABASE INITIALIZATION
# =========================

def init_db():

    conn = psycopg2.connect(DATABASE_URL)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(100) UNIQUE
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id SERIAL PRIMARY KEY,
        username VARCHAR(100),
        message TEXT,
        timestamp VARCHAR(20)
    )
    """)

    conn.commit()
    conn.close()


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

    conn = psycopg2.connect(DATABASE_URL)
    c = conn.cursor()

    c.execute(
       """
       INSERT INTO users(username)
       VALUES(%s)
       ON CONFLICT (username) DO NOTHING
       """,
       (username,)
    ) 

    c.execute("""
      INSERT INTO messages
      (username, message, timestamp)
      VALUES (%s, %s, %s)
    """, (
      "SYSTEM",
      f"{username} joined the chat",
      datetime.now().strftime("%H:%M:%S")
    ))

    conn.commit()
    conn.close()

    session["username"] = username

    token = create_token(username)
    session["token"] = token

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
        username=session["username"],
        token=session["token"]
    )


# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():

    if "username" in session:

        username = session["username"]

        conn = psycopg2.connect(DATABASE_URL)
        c = conn.cursor()

        c.execute("""
           INSERT INTO messages
           (username, message, timestamp)
           VALUES (%s, %s, %s)
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
@token_required
def send():

    username = request.username

    data = request.json

    conn = psycopg2.connect(DATABASE_URL)
    c = conn.cursor()

    c.execute("""
       INSERT INTO messages
       (username, message, timestamp)
       VALUES (%s, %s, %s)
    """, (
       username,
       data["message"],
       datetime.now().strftime("%H:%M:%S")
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "status": "success"
    })


# =========================
# GET MESSAGES
# =========================

@app.route("/messages")
@token_required
def messages():

    conn = psycopg2.connect(DATABASE_URL)
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
@token_required
def users():

    conn = psycopg2.connect(DATABASE_URL)
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
# CLEAR CHAT
# =========================

@app.route("/clear")
def clear_chat():

    conn = psycopg2.connect(DATABASE_URL)
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