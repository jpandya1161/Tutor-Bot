document.getElementById('sendButton').addEventListener('click', function () {
    var userInput = document.getElementById('userInput').value;

    if (!userInput.trim()) return; // Prevent empty messages

    // Clear input field
    document.getElementById('userInput').value = '';

    // Send to chatbot
    fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input: userInput })
    })
    .then(response => response.json())
    .then(data => {
        // Show user message
        appendMessage(userInput, 'user-message');

        // If backend returned user's English translation, show it
        if (data.user_translation && data.user_translation.trim() !== "") {
            appendMessage(data.user_translation, 'user-translation');
        }

        // Show chatbot's French reply
        appendMessage(data.response, 'bot-message');

        // Show chatbot's English translation
        if (data.translation && data.translation.trim() !== "") {
            appendMessage(data.translation, 'bot-translation');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

let debounceTimer;
document.getElementById('userInput').addEventListener('input', function () {
    clearTimeout(debounceTimer);
    const userInput = this.value.trim();
    if (!userInput) {
        document.getElementById('suggestions').innerHTML = '';
        return;
    }

    debounceTimer = setTimeout(() => {
        checkGrammar(userInput);
        fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: userInput })
        })
        .then(response => response.json())
        .then(data => {
            const suggestionsBox = document.getElementById('suggestions');
            suggestionsBox.innerHTML = '';
        
            // English Predictions
            if (data.english && data.english.length > 0) {
                const englishHeader = document.createElement('h4');
                englishHeader.innerText = 'English Predictions';
                suggestionsBox.appendChild(englishHeader);
        
                data.english.forEach(suggestion => {
                    const el = document.createElement('div');
                    el.className = 'suggestion-item';
                    el.innerText = suggestion;
                    el.onclick = () => {
                        document.getElementById('userInput').value = suggestion;
                        suggestionsBox.innerHTML = '';
                    };
                    suggestionsBox.appendChild(el);
                });
            }
        
            // French Predictions
            if (data.french && data.french.length > 0) {
                const frenchHeader = document.createElement('h4');
                frenchHeader.innerText = 'French Predictions';
                suggestionsBox.appendChild(frenchHeader);
        
                data.french.forEach(suggestion => {
                    const el = document.createElement('div');
                    el.className = 'suggestion-item';
                    el.innerText = suggestion;
                    el.onclick = () => {
                        document.getElementById('userInput').value = suggestion;
                        suggestionsBox.innerHTML = '';
                    };
                    suggestionsBox.appendChild(el);
                });
            }
        
            if ((!data.english || data.english.length === 0) && (!data.french || data.french.length === 0)) {
                suggestionsBox.innerHTML = '<p>No suggestions available.</p>';
            }
        });        
    }, 400);  // ← this is the key
});

document.addEventListener("DOMContentLoaded", function () {
    const inputBox = document.getElementById("userInput");
    const moodBox = document.getElementById("mood-result");

    // Existing mood check
    if (inputBox && moodBox) {
        inputBox.addEventListener("input", function () {
            fetch("/analyze_mood", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ text: inputBox.value })
            })
            .then(response => response.json())
            .then(data => {
                moodBox.textContent = data.mood_result;
            });
        });
    }

    // Grammar check on input with debounce
    let grammarTimer;
    inputBox.addEventListener("input", function () {
        clearTimeout(grammarTimer);
        const message = inputBox.value.trim();

        grammarTimer = setTimeout(() => {
            if (message.length >= 3) {
                checkGrammar(message);
            } else {
                document.getElementById('suggestion-box').style.display = 'none';
            }
        }, 300);  // ⏱ debounce for performance
    });
});


function appendMoodAnalysis(text) {
    var moodbox = document.getElementById('moodbox');
    var moodElement = document.createElement('div');
    moodElement.className = 'mood-item'; // Use the same class as prediction items
    moodElement.innerText = text;
    moodbox.appendChild(moodElement);
    moodbox.scrollTop = moodbox.scrollHeight;
}

// Function to append messages to the chatbox
function appendMessage(text, className) {
    var chatbox = document.getElementById('chatbox');
    var messageElement = document.createElement('div');
    messageElement.className = className;
    messageElement.innerText = text;
    chatbox.appendChild(messageElement);
    chatbox.scrollTop = chatbox.scrollHeight;
}

function checkGrammar(message) {
    fetch('/check_grammar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        const grammarBox = document.getElementById('grammarbox');

        grammarBox.innerHTML = "<h4>Do you mean...</h4>";  // Reset heading

        if (data.correction && data.correction !== message) {
            const el = document.createElement('div');
            el.className = 'grammar-item';
            el.innerText = data.correction;
            el.onclick = () => {
                document.getElementById('userInput').value = data.correction;

                // Optionally: Clear other suggestions
                grammarBox.innerHTML = "<h4>Grammar Check</h4>";
                document.getElementById('suggestions').innerHTML = '';
            };
            grammarBox.appendChild(el);
        }
    });
}