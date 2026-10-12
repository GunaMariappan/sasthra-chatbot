import { useEffect, useRef, useState } from "react";
import { sendChatMessage } from "../api";

const WELCOME_MESSAGE = {
  role: "bot",
  text: "Hi! Ask me anything about Sasthra products.",
};

export default function ChatPage({ token, onLogout }) {
  const [messages, setMessages] = useState([WELCOME_MESSAGE]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function handleSend(event) {
    event.preventDefault();
    const text = input.trim();
    if (!text || loading) return;

    setMessages((prev) => [...prev, { role: "user", text }]);
    setInput("");
    setLoading(true);

    try {
      const data = await sendChatMessage(text, token);
      setMessages((prev) => [...prev, { role: "bot", text: data.answer }]);
    } catch (err) {
      if (err.status === 401) {
        onLogout("Your session expired. Please log in again.");
        return;
      }
      setMessages((prev) => [...prev, { role: "error", text: err.message }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="chat-page">
      <header className="chat-header">
        <h1>Sasthra Product Assistant</h1>
        <button type="button" className="link-button" onClick={() => onLogout()}>
          Logout
        </button>
      </header>

      <main className="chat-messages">
        {messages.map((message, index) => (
          <div key={index} className={`bubble ${message.role}`}>
            {message.text}
          </div>
        ))}
        {loading && <div className="bubble bot typing">Typing...</div>}
        <div ref={bottomRef} />
      </main>

      <form className="chat-input" onSubmit={handleSend}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about Sasthra products..."
          maxLength={500}
        />
        <button type="submit" disabled={loading || !input.trim()}>
          Send
        </button>
      </form>
    </div>
  );
}