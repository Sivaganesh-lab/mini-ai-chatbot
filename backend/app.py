# -------------------------------
# Mini AI Chatbot Backend
# -------------------------------
# Built with Flask + OpenRouter API (OpenAI-compatible)
# Features:
#   1. Knowledge Base for predefined professional Q&A
#   2. AI Fallback using OpenRouter (GPT models)
#   3. Chat history saved locally in a file
# -------------------------------

from flask import Flask, request, jsonify
from flask_cors import CORS
from difflib import SequenceMatcher
from openai import OpenAI
from dotenv import load_dotenv 
import re, json, os


# -------------------------------
# Flask app setup
# -------------------------------
app = Flask(__name__)
CORS(app)   # Enable frontend (React) → backend communication

#Load environment variables from .env file
load_dotenv()
# -------------------------------
# OpenRouter Client (OpenAI-compatible)
# NOTE: For real projects, NEVER hardcode your API key.
#       Instead, load it from an environment variable.
# -------------------------------
load_dotenv(dotenv_path="./.env")
print("DEBUG KEY:", os.getenv("OPENAI_API_KEY"))
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY")  # API KEY
)

# -------------------------------
# Knowledge Base (Predefined Q&A)
# -------------------------------
knowledge_base = {
    "How can I improve team productivity?": "Use daily stand-ups, set clear OKRs, and encourage time-blocking.",
    "Tips for remote work?": "Maintain a fixed schedule, use video check-ins, and set clear boundaries.",
    "How to prioritize tasks?": "Use the Eisenhower Matrix: urgent-important, not urgent-important, etc.",
    "How to manage startup funding?": "Track runway, maintain investor relations, and plan funding rounds early.",
    "How to build strong company culture?": "Encourage transparency, celebrate wins, and promote feedback culture.",
    "Best practices for time management?": "Use Pomodoro technique, batch similar tasks, and avoid multitasking.",
    "How to avoid burnout?": "Take breaks, delegate tasks, and set realistic goals.",
    "What’s the best way to run meetings?": "Keep them short, set an agenda, and assign clear next steps."
}

# Chat history file (simple JSON lines file)
HISTORY_FILE = "chat_history.json"

# -------------------------------
# Helper: Save Q&A to history file
# -------------------------------
def save_history(entry):
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

# -------------------------------
# API Endpoint: /ask
# - Accepts POST requests with a "question"
# - First tries to match in Knowledge Base
# - If no match → fallback to OpenRouter AI
# -------------------------------
@app.route("/ask", methods=["POST"])
def ask():
    # Get user input from frontend
    data = request.get_json()
    question = data.get("question", "").strip().lower()

    # Clean the question (remove punctuation)
    question_clean = re.sub(r'[^\w\s]', '', question)

    # Normalize KB keys (lowercase, no punctuation)
    kb_normalized = {
        re.sub(r'[^\w\s]', '', k.lower()): k for k in knowledge_base.keys()
    }

    # -------------------------------
    # Step 1: Try to match in Knowledge Base
    # -------------------------------
    best_match = None
    best_score = 0.0

    for k_norm, k_orig in kb_normalized.items():
        score = SequenceMatcher(None, question_clean, k_norm).ratio()
        if score > best_score:
            best_score = score
            best_match = k_orig

    # If match is good enough (>= 0.75 similarity), use KB answer
    if best_score >= 0.75:
        answer = knowledge_base[best_match]
        source = "Knowledge Base"
    else:
        # -------------------------------
        # Step 2: Fallback → Ask OpenRouter AI
        # -------------------------------
        try:
            completion = client.chat.completions.create(
                model="openai/gpt-4o-mini",   # Smart + cost-efficient
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers professional questions clearly."},
                    {"role": "user", "content": data.get("question", "")}
                ],
                max_tokens=150
            )
            answer = completion.choices[0].message.content
            source = "OpenAI"
        except Exception as e:
            answer = f"⚠️ Could not fetch AI response: {str(e)}"
            source = "Error"

    # Build response
    response = {
        "question": data.get("question", ""),
        "answer": answer,
        "source": source   # Helps frontend show if answer is from KB or AI
    }

    # Save chat history locally
    save_history(response)

    # Send response back to frontend
    return jsonify(response)

# -------------------------------
# Run the app
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
