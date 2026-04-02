import { useState, useRef, useEffect } from 'react';
import { MessageCircle, X, Send, User, Bot, AlertCircle } from 'lucide-react';
import './ChatPanel.css';

export default function ChatPanel({ isOpen, onClose }) {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hi! I am your financial education tutor. How can I help you understand the stock market or investing today?' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isOpen]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMsg = input.trim();
    setInput('');
    const newMessages = [...messages, { role: 'user', content: userMsg }];
    setMessages(newMessages);
    setIsLoading(true);

    try {
      const apiUrl = import.meta.env.VITE_API_URL || '/api';
      const res = await fetch(`${apiUrl}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: newMessages })
      });

      if (!res.ok) {
        let errMsg = `API error: ${res.status}`;
        try {
          const errData = await res.json();
          if (errData.detail) errMsg = errData.detail;
        } catch(e) {}
        throw new Error(errMsg);
      }
      
      const data = await res.json();
      setMessages([...newMessages, { role: 'assistant', content: data.response }]);
    } catch (err) {
      setMessages([...newMessages, { 
        role: 'assistant', 
        content: `Sorry, I encountered an error. (${err.message})`,
        isError: true
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      {isOpen && <div className="chat-backdrop fade-in" onClick={onClose} />}
      <div className={`chat-panel glass-panel ${isOpen ? 'open' : ''}`}>
        <div className="chat-header">
          <div className="chat-title">
            <MessageCircle size={20} />
            <h2>Education Tutor</h2>
          </div>
          <button onClick={onClose} className="icon-btn">
            <X size={24} />
          </button>
        </div>

        <div className="chat-messages">
          {messages.map((msg, idx) => (
            <div key={idx} className={`chat-message ${msg.role}`}>
              <div className="message-avatar">
                {msg.role === 'assistant' ? <Bot size={18} /> : <User size={18} />}
              </div>
              <div className={`message-content ${msg.isError ? 'error-content' : ''}`}>
                {msg.isError && <AlertCircle size={14} className="inline-icon" />}
                {msg.content}
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="chat-message assistant loading">
              <div className="message-avatar"><Bot size={18} /></div>
              <div className="message-content">
                <span className="dot"></span>
                <span className="dot"></span>
                <span className="dot"></span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <form className="chat-input-area" onSubmit={handleSubmit}>
          <input
            type="text"
            value={input}
            onChange={e => setInput(e.target.value)}
            placeholder="Ask a financial question..."
            disabled={isLoading}
          />
          <button type="submit" disabled={!input.trim() || isLoading} className="send-btn">
            <Send size={18} />
          </button>
        </form>
      </div>
    </>
  );
}
