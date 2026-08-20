const chatForm = document.getElementById("chatForm");
const messageInput = document.getElementById("messageInput");
const chatMessages = document.getElementById("chatMessages");
const sendButton = document.getElementById("sendButton");
const suggestions = document.querySelectorAll(".suggestion");

function scrollToLatest() {
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addMessage(text, sender, match = null) {
  const row = document.createElement("div");
  row.className = `message-row ${sender}-row`;

  if (sender === "bot") {
    const avatar = document.createElement("div");
    avatar.className = "mini-avatar";
    avatar.textContent = "E";
    row.appendChild(avatar);
  }

  const bubble = document.createElement("div");
  bubble.className = `message ${sender}-message`;
  bubble.textContent = text;
  row.appendChild(bubble);
  chatMessages.appendChild(row);

  if (match) {
    const note = document.createElement("p");
    note.className = "match-note";
    note.textContent = `Best FAQ match: ${match}`;
    chatMessages.appendChild(note);
  }
  scrollToLatest();
  return row;
}

function addTypingMessage() {
  const row = document.createElement("div");
  row.className = "message-row bot-row";
  row.id = "typingIndicator";
  row.innerHTML = '<div class="mini-avatar">E</div><div class="message bot-message typing">Finding the best answer...</div>';
  chatMessages.appendChild(row);
  scrollToLatest();
}

async function sendMessage(message) {
  const text = message.trim();
  if (!text) return;

  addMessage(text, "user");
  messageInput.value = "";
  sendButton.disabled = true;
  addTypingMessage();

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text })
    });
    const data = await response.json();
    document.getElementById("typingIndicator")?.remove();

    if (!response.ok) throw new Error(data.error || "Something went wrong.");
    addMessage(data.answer, "bot", data.matched_question);
  } catch (error) {
    document.getElementById("typingIndicator")?.remove();
    addMessage(error.message || "I could not process that message. Please try again.", "bot");
  } finally {
    sendButton.disabled = false;
    messageInput.focus();
  }
}

chatForm.addEventListener("submit", (event) => {
  event.preventDefault();
  sendMessage(messageInput.value);
});

suggestions.forEach((button) => {
  button.addEventListener("click", () => sendMessage(button.textContent));
});
