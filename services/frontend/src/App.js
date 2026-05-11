import { useState } from "react";

function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const question = input;

    const userMsg = { role: "user", content: question };
    const aiMsg = { role: "ai", content: "" };

    setMessages(prev => [...prev, userMsg, aiMsg]);

    setInput("");

    const response = await fetch("/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        session_id: "user_001",
        message: question
      })
    });

    if (!response.ok || !response.body) {
      console.error("Request failed");
      return;
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");

    let buffer = "";

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value, { stream: true });
      buffer += chunk;

      const parts = buffer.split("\n\n");

      buffer = parts.pop();

      for (let part of parts) {
        const data = part.replace("data: ", "").trim();

        if (!data || data === "[DONE]") continue;

        setMessages(prev => {
          const updated = [...prev];
          const last = { ...updated[updated.length - 1] };

          if (last.role === "ai") {
            last.content += data;
            updated[updated.length - 1] = last;
          }

          return updated;
        });
      }
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>My RAG Chat 🤖</h2>

      <div style={{ marginBottom: 20 }}>
        {messages.map((msg, i) => (
          <div key={i} style={{ margin: "8px 0" }}>
            <b>{msg.role}:</b> {msg.content}
          </div>
        ))}
      </div>

      <input
        value={input}
        onChange={e => setInput(e.target.value)}
        style={{ width: 300 }}
        onKeyDown={e => e.key === "Enter" && sendMessage()}
      />

      <button onClick={sendMessage} style={{ marginLeft: 8 }}>
        Send
      </button>
    </div>
  );
}

export default App;