// Dosha Diagnosis Quiz Logic

const questions = [
    {
        icon: '🍽️',
        label: 'Digestion',
        options: ['fast', 'slow', 'moderate']
    },
    {
        icon: '😴',
        label: 'Sleep',
        options: ['light', 'deep', 'moderate']
    },
    {
        icon: '⚡',
        label: 'Energy',
        options: ['low', 'high', 'moderate']
    },
    {
        icon: '🌡️',
        label: 'Temperature Preference',
        options: ['cold', 'warm', 'moderate']
    },
    {
        icon: '😊',
        label: 'Mood',
        options: ['anxious', 'calm', 'irritable']
    },
    {
        icon: '👤',
        label: 'Body Frame',
        options: ['slim', 'broad', 'medium']
    }
];

let currentQuestion = 0;
let answers = {};

function initQuiz() {
    showQuestion(0);
}

function showQuestion(index) {
    if (index >= questions.length) {
        submitQuiz();
        return;
    }

    currentQuestion = index;
    const question = questions[index];
    const container = document.getElementById('quiz-container');
    
    container.innerHTML = `
        <div class="question-card">
            <span class="question-icon">${question.icon}</span>
            <div class="question-label">${question.label}</div>
            <div class="option-group">
                ${question.options.map(option => `
                    <button class="option-btn" onclick="selectOption('${question.label.toLowerCase().replace(' ', '_')}', '${option}')">
                        ${option.charAt(0).toUpperCase() + option.slice(1)}
                    </button>
                `).join('')}
            </div>
        </div>
    `;

    updateProgress();
}

function selectOption(key, value) {
    answers[key] = value;
    
    // Visual feedback
    const buttons = document.querySelectorAll('.option-btn');
    buttons.forEach(btn => btn.classList.remove('selected'));
    event.target.classList.add('selected');
    
    // Move to next question after a short delay
    setTimeout(() => {
        showQuestion(currentQuestion + 1);
    }, 500);
}

function updateProgress() {
    const progress = ((currentQuestion + 1) / questions.length) * 100;
    document.getElementById('progress-bar').style.width = progress + '%';
    document.getElementById('progress-text').textContent = `Question ${currentQuestion + 1} of ${questions.length}`;
}

async function submitQuiz() {
    // Map answers to API format
    const profile = {
        digestion: answers.digestion || 'moderate',
        sleep: answers.sleep || 'moderate',
        energy: answers.energy || 'moderate',
        temperature_preference: answers.temperature_preference || 'moderate',
        mood: answers.mood || 'calm',
        body_frame: answers.body_frame || 'medium'
    };

    showLoading(document.getElementById('quiz-container'));
    
    try {
        const response = await fetch('http://localhost:5000/predict_dosha', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(profile)
        });
        
        const result = await response.json();
        displayResults(result);
        
        // Save quiz result to analytics database
        if (result.dosha && result.confidence) {
            const confidenceNum = parseInt(result.confidence);
            await fetch('http://localhost:5000/save_quiz_score', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    dosha: result.dosha,
                    score: confidenceNum  // Use confidence as wellness score
                })
            });
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('quiz-container').innerHTML = 
            '<div class="question-card"><p style="color: red;">Error submitting quiz. Please try again.</p></div>';
    }
}

function displayResults(result) {
    document.getElementById('quiz-container').style.display = 'none';
    document.querySelector('.lotus-progress').style.display = 'none';
    
    const resultsCard = document.getElementById('results-card');
    resultsCard.style.display = 'block';
    
    const dosha = result.dosha || 'Vata';
    const confidence = result.confidence || '75%';
    const type = result.type || 'Single Constitution';
    
    // Set dosha mandala icon
    const mandalaIcons = {
        'Vata': '🌪️',
        'Pitta': '🔥',
        'Kapha': '🌊'
    };
    document.getElementById('dosha-mandala').textContent = mandalaIcons[dosha] || '🌿';
    
    document.getElementById('dosha-type').textContent = `${type} - ${dosha.toUpperCase()}`;
    document.getElementById('dosha-description').textContent = 
        `Your Ayurvedic constitution is primarily ${dosha}. This determines your optimal diet, lifestyle, and wellness practices.`;
    
    // Update confidence ring
    const confidenceNum = parseInt(confidence);
    const circumference = 2 * Math.PI * 70;
    const offset = circumference - (confidenceNum / 100) * circumference;
    document.getElementById('confidence-circle').style.strokeDashoffset = offset;
    document.getElementById('confidence-text').textContent = confidence;
    
    // Store dosha in localStorage for other pages
    localStorage.setItem('userDosha', dosha);
}

// Initialize quiz on page load
if (document.getElementById('quiz-container')) {
    initQuiz();
}

