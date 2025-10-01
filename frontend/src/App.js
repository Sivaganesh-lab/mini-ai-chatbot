import React, { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [chat, setChat] = useState([]);

  // Load chat history when page loads
  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/history");
        const data = await response.json();
        setChat(data);
      } catch (error) {
        console.error("Error loading history:", error);
      }
    };
    fetchHistory();
  }, []);

  // Ask a new question
  const askQuestion = async () => {
    if (!question.trim()) return;

    try {
      const response = await fetch("http://127.0.0.1:5000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });

      const data = await response.json();
      setChat((prev) => [...prev, { q: question, a: data.answer, source: data.source }]);
      setQuestion("");
    } catch (error) {
      setChat((prev) => [
        ...prev,
        { q: question, a: "⚠️ Error: Could not connect to backend.", source: "Error" },
      ]);
    }
  };

  return (
    <div className="App">
      <h1 className="title">✨ Mini AI Chatbot 🤖 ✨</h1>

      {/* Chat history */}
      <div className="chat-box">
        {chat.map((c, i) => (
          <div key={i} className="chat-message">
            <p className="user-msg"><b>You:</b> {c.q}</p>
            <p className="bot-msg">
              <b>Bot:</b> {c.a} <br />
              <span className="answer-source">[{c.source}]</span>
            </p>
          </div>
        ))}
      </div>

      {/* Input area */}
      <div className="input-area">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="💬 Ask me anything..."
        />
        <button onClick={askQuestion}>Send 🚀</button>
      </div>
    </div>
  );
}

export default App;
