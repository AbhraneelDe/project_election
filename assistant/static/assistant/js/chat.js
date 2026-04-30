/* chat.js — AI chat interface logic */

(function () {
  'use strict';

  const chatMessages  = document.getElementById('chatMessages');
  const chatForm      = document.getElementById('chatForm');
  const userInput     = document.getElementById('userInput');
  const sendBtn       = document.getElementById('sendBtn');
  const typingIndicator = document.getElementById('typingIndicator');
  const clearBtn      = document.getElementById('clearChatBtn');

  const API_URL    = window.CHAT_API_URL || '/api/chat/';
  const CSRF_TOKEN = window.CSRF_TOKEN  || '';

  // Conversation history stored in memory
  let history = [];

  /* ── Auto-resize textarea ── */
  userInput.addEventListener('input', () => {
    userInput.style.height = 'auto';
    userInput.style.height = Math.min(userInput.scrollHeight, 140) + 'px';
  });

  /* ── Submit on Enter (Shift+Enter = newline) ── */
  userInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      chatForm.dispatchEvent(new Event('submit'));
    }
  });

  /* ── Send message on form submit ── */
  chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const message = userInput.value.trim();
    if (!message) return;
    await sendMessage(message);
  });

  /* ── Suggestion chips ── */
  window.sendSuggestion = function (btn) {
    const q = btn.dataset.question;
    if (q) {
      userInput.value = q;
      chatForm.dispatchEvent(new Event('submit'));
    }
  };

  /* ── Clear chat ── */
  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      history = [];
      // Remove all messages except the welcome message
      const msgs = chatMessages.querySelectorAll('.message:not(#welcomeMessage)');
      msgs.forEach(m => m.remove());
      const welcome = document.getElementById('welcomeMessage');
      if (welcome) welcome.style.display = 'flex';
    });
  }

  /* ── Preload question from timeline page ── */
  const preload = sessionStorage.getItem('preloadQuestion');
  if (preload) {
    sessionStorage.removeItem('preloadQuestion');
    setTimeout(() => {
      userInput.value = preload;
      chatForm.dispatchEvent(new Event('submit'));
    }, 600);
  }

  /* ══ Core: Send message ══════════════════════════════════ */
  async function sendMessage(message) {
    setLoading(true);

    // Hide welcome message on first real send
    const welcome = document.getElementById('welcomeMessage');
    if (welcome) welcome.style.display = 'none';

    appendMessage('user', message);
    userInput.value = '';
    userInput.style.height = 'auto';
    scrollToBottom();

    showTyping(true);

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': CSRF_TOKEN,
        },
        body: JSON.stringify({ message, history }),
      });

      const data = await response.json();

      if (!response.ok) throw new Error(data.error || 'Server error');

      const reply = data.reply || 'Sorry, I could not generate a response.';
      history.push({ role: 'user', content: message });
      history.push({ role: 'assistant', content: reply });
      // Keep last 20 entries to avoid bloat
      if (history.length > 20) history = history.slice(-20);

      showTyping(false);
      appendMessage('assistant', reply);

    } catch (err) {
      showTyping(false);
      appendMessage('assistant', `⚠️ **Connection error**: ${err.message}. Please check that the server is running and try again.`);
    }

    setLoading(false);
    scrollToBottom();
  }

  /* ══ DOM Helpers ════════════════════════════════════════ */

  function appendMessage(role, text) {
    const isUser = role === 'user';
    const el = document.createElement('div');
    el.className = `message message--${role}`;
    el.setAttribute('role', 'article');
    el.setAttribute('aria-label', isUser ? 'Your message' : 'ElectionGuide response');

    el.innerHTML = `
      <div class="message-avatar" aria-hidden="true">${isUser ? '👤' : '🏛️'}</div>
      <div class="message-bubble">
        <div class="message-text">${formatText(text)}</div>
        <time class="message-time">${getTime()}</time>
      </div>`;

    chatMessages.appendChild(el);
    // Animate in
    el.style.opacity = '0';
    el.style.transform = 'translateY(10px)';
    requestAnimationFrame(() => {
      el.style.transition = 'opacity .3s ease, transform .3s ease';
      el.style.opacity = '1';
      el.style.transform = 'translateY(0)';
    });
  }

  function showTyping(show) {
    typingIndicator.hidden = !show;
    if (show) scrollToBottom();
  }

  function setLoading(loading) {
    sendBtn.disabled = loading;
    userInput.disabled = loading;
  }

  function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function getTime() {
    return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  }

  /* ── Markdown-lite formatter ── */
  function formatText(text) {
    return text
      // Bold **text**
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      // Numbered list: "1. item"
      .replace(/^(\d+)\.\s+(.+)$/gm, '<span class="md-step">$1. $2</span>')
      // Bullet: "- item" or "• item"
      .replace(/^[-•]\s+(.+)$/gm, '<span class="md-bullet">• $1</span>')
      // Newlines
      .replace(/\n\n/g, '</p><p style="margin-top:.5rem">')
      .replace(/\n/g, '<br/>');
  }

})();
