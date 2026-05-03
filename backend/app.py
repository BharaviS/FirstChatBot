from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from groq import Groq

import os

load_dotenv()
app = Flask(__name__)
CORS(app)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route("/")
def home():
    return jsonify({"message": "Backend is working ✅"})

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    messages = data.get("messages", [])

    if not messages:
        return jsonify({"reply": "Please send a message first."})

    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages,
        max_completion_tokens=300
    )

    reply = completion.choices[0].message.content

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)