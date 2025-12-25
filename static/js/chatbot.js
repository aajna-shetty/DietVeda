// Dr. Veda Chatbot Logic

let dosha = localStorage.getItem('userDosha') || 'Vata';

document.addEventListener('DOMContentLoaded', function() {
    const doshaSelect = document.getElementById('dosha-select');
    if (doshaSelect) {
        doshaSelect.value = dosha;
        doshaSelect.addEventListener('change', function() {
            dosha = this.value;
        });
    }

    const chatInput = document.getElementById('chat-input');
    if (chatInput) {
        chatInput.focus();
    }
});

async function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Add user message to chat
    addMessage(message, 'user');
    input.value = '';
    
    // Show typing indicator
    const typingId = addMessage('...', 'bot');
    
    try {
        // Call chatbot API (you'll need to add this endpoint to flask_backend.py)
        const response = await fetch('http://localhost:5000/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question: message, dosha: dosha })
        });
        
        const data = await response.json();
        const botResponse = data.response || 'I am reflecting... please ask again.';
        
        // Remove typing indicator and add real response
        removeMessage(typingId);
        addMessage(botResponse, 'bot');
    } catch (error) {
        console.error('Error:', error);
        removeMessage(typingId);
        addMessage('I apologize, but I am having trouble connecting. Please try again.', 'bot');
    }
}

function addMessage(text, type) {
    const messagesContainer = document.getElementById('chat-messages');
    const messageId = 'msg-' + Date.now();
    
    const messageDiv = document.createElement('div');
    messageDiv.id = messageId;
    messageDiv.className = `message ${type}`;
    messageDiv.innerHTML = `<p>${text}</p>`;
    
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    return messageId;
}

function removeMessage(id) {
    const message = document.getElementById(id);
    if (message) {
        message.remove();
    }
}

// Allow Enter key to send
document.addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && document.activeElement.id === 'chat-input') {
        sendMessage();
    }
});

