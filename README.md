
```markdown
# 🤖 Mini AI Chatbot

A simple web-based AI chatbot that answers professional questions.  
Built with **React (frontend)** + **Flask (backend)** + **Hugging Face API** fallback.

---

## 🚀 Features
- React frontend with chat UI
- Flask backend with REST API (`/ask`)
- Knowledge base of 8+ professional Q&A pairs
- Hugging Face fallback for unmatched questions
- Chat history (last 10 Q&A shown)

---

## 📂 Project Structure

```
mini-ai-chatbot/
│── backend/ # Flask backend
│ ├── app.py
│ ├── requirements.txt
│ ├── Chat_history.json
│ └── .env
│
│── frontend/ # React frontend
│ ├── public/
│ ├── src/
│ │ ├── App.js
│ │ ├── App.css
│ │ └── ...
│ ├── package.json
│ └── README.md
│
│── README.md # Project guide
│── .gitignore


````

---

## ⚙️ Setup Instructions

### 1️⃣ Backend Setup
```bash
cd backend
pip install -r requirements.txt
set FLASK_APP=app.py
set FLASK_ENV=development
set HUGGINGFACE_API_KEY=your_hf_token_here
python app.py
````

Runs on: **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

### 2️⃣ Frontend Setup

```bash
cd frontend
npm install
npm start
```

Runs on: **[http://localhost:3000](http://localhost:3000)**

---

## 🎯 Usage

1. Ask predefined questions (e.g., *"How to manage startup funding?"*) → returns from knowledge base.
2. Ask new questions (e.g., *"What is blockchain?"*) → OpenAI API answer.
3. Last 10 Q&A shown in chat.

---

## 🙋 Assumptions

* OPENAI free API has slow first response (cold start).
* Requires internet for AI fallback.
* Knowledge base can be extended easily.
