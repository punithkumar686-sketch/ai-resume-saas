from flask import request, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def register():
    data = request.json
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    hashed = generate_password_hash(data['password'])

    c.execute("INSERT INTO users (email, password) VALUES (?, ?)",
              (data['email'], hashed))
    conn.commit()
    conn.close()

    return jsonify({"message": "Registered"})

def login():
    data = request.json
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    user = c.execute("SELECT * FROM users WHERE email=?",
                     (data['email'],)).fetchone()

    if user and check_password_hash(user[2], data['password']):
        return jsonify({"user_id": user[0], "credits": user[3], "premium": user[4]})

    return jsonify({"error": "Invalid login"})
