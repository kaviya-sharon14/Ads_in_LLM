import { useState, useRef, useEffect } from "react";
import "./index.css";

import * as pdfjsLib from 'pdfjs-dist';
pdfjsLib.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjsLib.version}/pdf.worker.min.js`;

// --- Configuration & Helpers ---
const API_BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";
const generateId = () => Math.random().toString(36).substr(2, 9);
const SESSION_ID = "user_" + generateId();

// --- Database configuration removed as it's now handled by the backend ---

// --- Icons ---
const PlusIcon = () => <svg stroke="currentColor" fill="none" strokeWidth="2" viewBox="0 0 24 24" strokeLinecap="round" strokeLinejoin="round" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>;
const FolderIcon = () => <svg stroke="currentColor" fill="none" strokeWidth="2" viewBox="0 0 24 24" strokeLinecap="round" strokeLinejoin="round" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>;
const SettingsIcon = () => <svg stroke="currentColor" fill="none" strokeWidth="2" viewBox="0 0 24 24" strokeLinecap="round" strokeLinejoin="round" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>;
const ChatIcon = () => <svg stroke="currentColor" fill="none" strokeWidth="2" viewBox="0 0 24 24" strokeLinecap="round" strokeLinejoin="round" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>;
const EditIcon = () => <svg stroke="currentColor" fill="none" strokeWidth="2" viewBox="0 0 24 24" strokeLinecap="round" strokeLinejoin="round" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>;
const DeleteIcon = () => <svg stroke="currentColor" fill="none" strokeWidth="2" viewBox="0 0 24 24" strokeLinecap="round" strokeLinejoin="round" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>;
const SendIcon = () => <svg stroke="currentColor" fill="none" strokeWidth="2" viewBox="0 0 24 24" strokeLinecap="round" strokeLinejoin="round" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>;
const FileIcon = () => <svg stroke="currentColor" fill="none" strokeWidth="2" viewBox="0 0 24 24" strokeLinecap="round" strokeLinejoin="round" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"></path><polyline points="13 2 13 9 20 9"></polyline></svg>;
const CloseIcon = () => <svg stroke="currentColor" fill="none" strokeWidth="2" viewBox="0 0 24 24" strokeLinecap="round" strokeLinejoin="round" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>;

// --- Typewriter Component for realistic texting effect ---
const TypewriterText = ({ content, speed = 15, onComplete }) => {
  const [displayedText, setDisplayedText] = useState("");
  useEffect(() => {
    let i = 0;
    setDisplayedText("");
    const interval = setInterval(() => {
      setDisplayedText(content.slice(0, i));
      i++;
      if (i > content.length) {
        clearInterval(interval);
        if (onComplete) onComplete();
      }
    }, speed);
    return () => clearInterval(interval);
  }, [content, speed]);
  return <span className="msg-content-text">{displayedText}</span>;
};

function LoginScreen({ onLogin }) {
  const [email, setEmail] = useState("");
  const handleSubmit = (e) => {
    e.preventDefault();
    if (email.trim()) onLogin(email.trim());
  };
  return (
    <div className="auth-container">
      <div className="blobs">
        <div className="blob blob-1"></div>
        <div className="blob blob-2"></div>
      </div>
      <div className="auth-box glass-panel">
        <h1 className="gradient-text">Welcome to ADGENO</h1>
        <p style={{ marginBottom: "28px", color: "var(--text-secondary)", fontSize: "14px", lineHeight: "1.5" }}>
          Log in with your email to access your highly empathetic assistant.
        </p>
        <form onSubmit={handleSubmit}>
          <input
            type="email"
            placeholder="Enter your email address"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            autoFocus
          />
          <button type="submit">Experience AdGeno</button>
        </form>
      </div>
    </div>
  );
}

function App() {
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem('adgeno_user');
    return saved ? JSON.parse(saved) : null;
  });
  
  const [chats, setChats] = useState(() => {
    const saved = localStorage.getItem('adgeno_chats');
    return saved ? JSON.parse(saved) : [
      {
        id: generateId(),
        title: "New Chat",
        messages: [{ 
          role: "assistant", 
          content: "Hi! I'm here for you. How are you doing today? You can type to me, speak to me, or even upload a file if you need me to look at it.",
          isStreamed: true
        }]
      }
    ];
  });
  const [currentChatId, setCurrentChatId] = useState(() => {
    const saved = localStorage.getItem('adgeno_currentChatId');
    return saved ? JSON.parse(saved) : chats[0]?.id;
  });
  const [emotionalProfile, setEmotionalProfile] = useState(() => {
    const saved = localStorage.getItem('adgeno_emotionalProfile');
    return saved ? JSON.parse(saved) : [];
  });
  const [editingChatId, setEditingChatId] = useState(null);
  const [editingTitle, setEditingTitle] = useState("");

  useEffect(() => {
    localStorage.setItem('adgeno_user', JSON.stringify(user));
  }, [user]);

  useEffect(() => {
    localStorage.setItem('adgeno_chats', JSON.stringify(chats));
  }, [chats]);

  useEffect(() => {
    if (currentChatId) {
      localStorage.setItem('adgeno_currentChatId', JSON.stringify(currentChatId));
    }
  }, [currentChatId]);

  useEffect(() => {
    localStorage.setItem('adgeno_emotionalProfile', JSON.stringify(emotionalProfile));
  }, [emotionalProfile]);

  const [loading, setLoading] = useState(false);
  const [input, setInput] = useState("");

  // File upload state
  const [attachedFiles, setAttachedFiles] = useState([]);
  const fileInputRef = useRef(null);

  // Settings dropdown state
  const [showSettings, setShowSettings] = useState(false);

  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);

  const currentChat = chats.find(c => c.id === currentChatId) || chats[0];
  const messages = currentChat?.messages || [];

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const handleLogin = (email) => { setUser({ email, name: email.split("@")[0] }); };

  const handleLogout = () => {
    setUser(null);
    setShowSettings(false);
  };

  const adjustTextareaHeight = () => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "24px";
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`;
    }
  };

  const handleInputChange = (e) => {
    setInput(e.target.value);
    adjustTextareaHeight();
  };

  const updateCurrentChatMessages = (newMessages) => {
    setChats(prev => prev.map(chat =>
      chat.id === currentChatId ? { ...chat, messages: typeof newMessages === 'function' ? newMessages(chat.messages) : newMessages } : chat
    ));
  };

  const startNewChat = () => {
    const newChat = {
      id: generateId(),
      title: "New Chat",
      messages: [{ role: "assistant", content: "Hi! I am here to help. What's on your mind?", isStreamed: true }]
    };
    setChats(prev => [newChat, ...prev]);
    setCurrentChatId(newChat.id);
  };

  const deleteChat = (e, id) => {
    e.stopPropagation();
    const filtered = chats.filter(c => c.id !== id);
    if (filtered.length === 0) {
      const newChat = { id: generateId(), title: "New Chat", messages: [{ role: "assistant", content: "Hello again!", isStreamed: true }] };
      setChats([newChat]);
      setCurrentChatId(newChat.id);
    } else {
      setChats(filtered);
      if (currentChatId === id) setCurrentChatId(filtered[0].id);
    }
  };

  const startRename = (e, id, currentTitle) => {
    e.stopPropagation();
    setEditingChatId(id);
    setEditingTitle(currentTitle);
  };

  const submitRename = (id) => {
    if (editingTitle.trim()) {
      setChats(prev => prev.map(chat => chat.id === id ? { ...chat, title: editingTitle.trim() } : chat));
    }
    setEditingChatId(null);
    setEditingTitle("");
  };

  // --- File Upload Logic ---
  const handleFileChange = async (e) => {
    if (e.target.files && e.target.files.length > 0) {
      const filesArr = Array.from(e.target.files);
      const newFiles = [];
      
      for (const file of filesArr) {
        let extractedText = "";
        let isImage = false;
        let base64Url = null;
        
        if (file.name.endsWith(".txt")) {
          extractedText = await file.text();
        } else if (file.name.endsWith(".pdf")) {
          try {
            const arrayBuffer = await file.arrayBuffer();
            const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
            for (let i = 1; i <= pdf.numPages; i++) {
              const page = await pdf.getPage(i);
              const textContent = await page.getTextContent();
              const pageText = textContent.items.map(item => item.str).join(" ");
              extractedText += pageText + "\\n";
            }
          } catch(err) {
            console.error("PDF Read Error:", err);
            extractedText = "[Could not read PDF content]";
          }
        } else if (file.type.startsWith("image/")) {
          isImage = true;
          base64Url = await new Promise((resolve) => {
            const reader = new FileReader();
            reader.onloadend = () => resolve(reader.result);
            reader.readAsDataURL(file);
          });
        }

        newFiles.push({
          name: file.name,
          size: (file.size / 1024).toFixed(1) + ' KB',
          type: file.type,
          content: extractedText,
          isImage,
          base64Url
        });
      }
      setAttachedFiles(prev => [...prev, ...newFiles]);
    }
    // reset input so the same file could be selected again if removed
    e.target.value = null; 
  };

  const removeFile = (index) => {
    setAttachedFiles(prev => prev.filter((_, i) => i !== index));
  };

  // Emotional profile and memory extraction is now handled by backend state or removed from frontend for direct integration

  const sendMessage = async () => {
    if (!input.trim() && attachedFiles.length === 0) return;
    if (loading) return;
    
    let userMessageText = input.trim() || "[Sent an image/file]";
    const images = attachedFiles.filter(f => f.isImage).map(f => f.base64Url);
    const documents = attachedFiles.filter(f => !f.isImage);
    
    if (documents.length > 0) {
      const fileContents = documents.map(f => 
        f.content ? `\n--- File: ${f.name} ---\n${f.content}\n--- End File ---\n` : `\n[Attached File: ${f.name} (No content extracted)]\n`
      ).join("\n");
      userMessageText = `${fileContents}\n\n${userMessageText}`;
    }

    setInput("");
    setAttachedFiles([]);
    if (textareaRef.current) textareaRef.current.style.height = "24px";
    
    if (currentChat.title === "New Chat" && currentChat.messages.length <= 1) {
      setChats(prev => prev.map(chat => 
        chat.id === currentChatId ? { ...chat, title: input.substring(0, 30) + (input.length > 30 ? "..." : "New Chat") } : chat
      ));
    }

    updateCurrentChatMessages(prev => [...prev, { role: "user", content: input || "[Attached Media]", isStreamed: true }]);
    setLoading(true);

    try {
      const payload = {
        session_id: SESSION_ID,
        message: input.trim() || "[Sent a file/image]",
        images: images,
        file_context: documents.map(f => f.content).join("\n\n")
      };

      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      const data = await response.json();
      const aiResponse = data.response;

      updateCurrentChatMessages(prev => [
        ...prev,
        {
          role: "assistant",
          content: aiResponse,
          isStreamed: false
        }
      ]);
    } catch (error) {
      console.error(error);
      updateCurrentChatMessages(prev => [
        ...prev,
        { role: "assistant", content: "I'm having trouble connecting to the network right now. I hope you're doing okay!", isStreamed: false }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  if (!user) {
    return <LoginScreen onLogin={handleLogin} />;
  }

  return (
    <div className="app-layout">
      {/* Hidden File Picker */}
      <input
        type="file"
        multiple
        ref={fileInputRef}
        onChange={handleFileChange}
        style={{ display: 'none' }}
        accept=".pdf,.doc,.docx,.ppt,.pptx,.txt,.jpg,.jpeg,.png,.webp"
      />

      {/* Sidebar Layout */}
      <div className="sidebar glass-nav">
        <div className="sidebar-brand">AdGeno</div>

        <div className="sidebar-top-options">
          <button className="sidebar-menu-btn action-new-chat" onClick={startNewChat}>
            <PlusIcon /> <span style={{ fontWeight: 500 }}>New chat</span>
          </button>

          <button className="sidebar-menu-btn" onClick={() => fileInputRef.current.click()}>
            <FolderIcon /> File Explorer
          </button>
        </div>

        <div className="sidebar-section-title">Recent Conversations</div>

        <div className="chat-history">
          {chats.map(chat => (
            <div
              key={chat.id}
              className={`history-item ${chat.id === currentChatId ? 'active' : ''}`}
              onClick={() => setCurrentChatId(chat.id)}
            >
              <ChatIcon />
              <div className="history-title">
                {editingChatId === chat.id ? (
                  <input
                    autoFocus
                    className="rename-input"
                    value={editingTitle}
                    onChange={(e) => setEditingTitle(e.target.value)}
                    onBlur={() => submitRename(chat.id)}
                    onKeyDown={(e) => e.key === 'Enter' && submitRename(chat.id)}
                    onClick={(e) => e.stopPropagation()}
                  />
                ) : (
                  chat.title
                )}
              </div>

              {editingChatId !== chat.id && (
                <div className="history-actions" onClick={(e) => e.stopPropagation()}>
                  <button className="icon-btn" onClick={(e) => startRename(e, chat.id, chat.title)} title="Rename">
                    <EditIcon />
                  </button>
                  <button className="icon-btn" onClick={(e) => deleteChat(e, chat.id)} title="Delete">
                    <DeleteIcon />
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>

        <div className="sidebar-bottom-options">
          <div style={{ position: "relative" }}>
            <button className="sidebar-menu-btn" onClick={() => setShowSettings(!showSettings)}>
              <SettingsIcon /> Settings
            </button>

            {showSettings && (
              <div className="settings-dropdown popup-anim">
                <button className="dropdown-item" onClick={handleLogout}>
                  Switch Account
                </button>
                <button className="dropdown-item" onClick={handleLogout}>
                  Sign Out
                </button>
              </div>
            )}
          </div>

          <div className="user-profile">
            <div className="user-avatar gradient-bg">{user.name.charAt(0).toUpperCase()}</div>
            <div className="user-email">{user.email}</div>
          </div>
        </div>
      </div>

      {/* Main Chat Layout */}
      <div className="main-chat">
        <div className="bg-glow"></div>

        <div className="messages-container">
          {messages.map((msg, index) => (
            <div key={index} className={`message-row ${msg.role === "assistant" ? "ai" : "human"}`}>
              <div className="message-content">
                <div className={`message-avatar ${msg.role === "user" ? "user-av" : "ai-av"}`}>
                  {msg.role === "user" ? user.name.charAt(0).toUpperCase() : "AG"}
                </div>
                <div className="message-text">
                  {msg.role === "assistant" && !msg.isStreamed ? (
                    <TypewriterText
                      content={msg.content}
                      onComplete={() => {
                        updateCurrentChatMessages(prev => {
                          const updated = [...prev];
                          updated[index].isStreamed = true;
                          return updated;
                        });
                        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
                      }}
                    />
                  ) : (
                    <span className="msg-content-text">{msg.content}</span>
                  )}
                </div>
              </div>
            </div>
          ))}
          {loading && (
            <div className="message-row ai">
              <div className="message-content">
                <div className="message-avatar ai-av pulse-av">AG</div>
                <div className="message-text">
                  <div className="typing-indicator">
                    <span></span><span></span><span></span>
                  </div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} style={{ height: "60px", width: "100%" }} />
        </div>

        <div className="input-container">
          {/* Attached Files display area */}
          {attachedFiles.length > 0 && (
            <div className="attached-files-container">
              {attachedFiles.map((file, i) => (
                <div key={i} className="attached-file-pill">
                  {file.isAudio ? (
                    <audio src={file.url} controls style={{ height: "30px", width: "200px" }} />
                  ) : (
                    <>
                      <FileIcon />
                      <span className="file-name">{file.name}</span>
                    </>
                  )}
                  <button className="remove-file-btn" onClick={() => removeFile(i)}>
                    <CloseIcon />
                  </button>
                </div>
              ))}
            </div>
          )}

          <div className="input-box glass-input">
            <textarea
              ref={textareaRef}
              value={input}
              onChange={handleInputChange}
              onKeyDown={handleKeyDown}
              placeholder="Ask anything, AdGeno is here to help..."
              rows={1}
              style={{ height: "24px", paddingRight: "45px" }} // Adjusted padding for send button only
            />

            <div className="input-actions-right">

              <button
                className="send-btn"
                onClick={sendMessage}
                disabled={loading || (!input.trim() && attachedFiles.length === 0)}
              >
                <SendIcon />
              </button>
            </div>
          </div>
          <div className="legal-text">
            AdGeno delivers context-aware knowledge using advanced LLMs and streams real-time intent-based options naturally.
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;