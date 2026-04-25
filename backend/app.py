from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import sqlite3
from db import init_db
from auth import register, login
from payments import create_checkout
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

app = Flask(__name__)
CORS(app)

init_db()

client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

@app.route("/register", methods=["POST"])
def reg():
    return register()

@app.route("/login", methods=["POST"])
def log():
    return login()

@app.route("/pay", methods=["GET"])
def pay():
    return create_checkout()

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    user_id = data["user_id"]

    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    user = c.execute("SELECT credits, premium FROM users WHERE id=?",
                     (user_id,)).fetchone()

    if user[0] <= 0 and user[1] == 0:
        return jsonify({"error": "No credits left"})

    prompt = f"""
    Create ATS resume:
    Name: {data['name']}
    Skills: {data['skills']}
    Experience: {data['experience']}
    Job: {data['job']}
    """

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    output = res.choices[0].message.content

    if user[1] == 0:
        c.execute("UPDATE users SET credits = credits - 1 WHERE id=?", (user_id,))
        conn.commit()

    conn.close()

    return jsonify({"resume": output})


@app.route("/download", methods=["POST"])
def download_pdf():
    data = request.json
    doc = SimpleDocTemplate("resume.pdf")
    styles = getSampleStyleSheet()

    content = [Paragraph(data["text"], styles["Normal"])]
    doc.build(content)

    return jsonify({"message": "PDF created"})
    

if __name__ == "__main__":
    app.run()
