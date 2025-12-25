// Sattva Routine Tracker Logic

let habits = [];
let dosha = localStorage.getItem('userDosha') || 'Vata';

document.addEventListener('DOMContentLoaded', function() {
    const doshaSelect = document.getElementById('dosha-select');
    if (doshaSelect) {
        doshaSelect.value = dosha;
        doshaSelect.addEventListener('change', function() {
            dosha = this.value;
            loadHabits();
        });
    }

    const calculateBtn = document.getElementById('calculate-btn');
    if (calculateBtn) {
        calculateBtn.addEventListener('click', calculateScore);
    }

    loadHabits();
});

async function loadHabits() {
    try {
        const response = await fetch(`http://localhost:5000/get_routine?dosha=${dosha}`);
        const data = await response.json();
        
        habits = [
            ...(data.universal || []),
            ...(data.specific || [])
        ];
        
        displayHabits();
    } catch (error) {
        console.error('Error loading habits:', error);
        // Fallback to default habits
        habits = getDefaultHabits();
        displayHabits();
    }
}

function getDefaultHabits() {
    const universal = [
        ['Wake up before 6:00 AM (Brahma Muhurta)', 20],
        ['Tongue Scraping (Jivha Prakshalana)', 10],
        ['Drink Warm Copper Water', 10],
        ['No Screen Time 1hr before Bed', 15]
    ];
    
    const specific = {
        'Vata': [
            ['Self-Massage with Sesame Oil (Abhyanga)', 20],
            ['Eat a warm, cooked breakfast', 15],
            ['Bedtime by 10:00 PM', 20]
        ],
        'Pitta': [
            ['Cool shower or swim', 15],
            ['Avoid spicy/fried foods today', 20],
            ['Meditation for 10 mins', 20]
        ],
        'Kapha': [
            ['Dry Brushing (Garshana)', 15],
            ['Vigorous Exercise (Sweat it out)', 25],
            ['No napping during the day', 15]
        ]
    };
    
    return [...universal, ...(specific[dosha] || specific['Vata'])];
}

function displayHabits() {
    const container = document.getElementById('habits-container');
    
    container.innerHTML = habits.map((habit, index) => {
        const [text, points] = Array.isArray(habit) ? habit : [habit, 10];
        const icon = getHabitIcon(text);
        
        return `
            <div class="habit-item">
                <span class="habit-icon">${icon}</span>
                <input type="checkbox" class="habit-checkbox" id="habit-${index}" data-points="${points}">
                <label for="habit-${index}" class="habit-text">${text}</label>
                <span class="habit-points">+${points} pts</span>
            </div>
        `;
    }).join('');
}

function getHabitIcon(text) {
    if (text.includes('Wake') || text.includes('Brahma')) return '🌞';
    if (text.includes('Tongue')) return '👅';
    if (text.includes('Water')) return '💧';
    if (text.includes('Screen')) return '📱';
    if (text.includes('Massage') || text.includes('Abhyanga')) return '🫶';
    if (text.includes('breakfast') || text.includes('food')) return '🍽️';
    if (text.includes('Bedtime') || text.includes('sleep')) return '🌙';
    if (text.includes('shower') || text.includes('swim')) return '🚿';
    if (text.includes('Meditation')) return '🧘';
    if (text.includes('Brushing') || text.includes('Garshana')) return '🪮';
    if (text.includes('Exercise')) return '💪';
    if (text.includes('napping')) return '😴';
    return '🌿';
}

function calculateScore() {
    const checkboxes = document.querySelectorAll('.habit-checkbox');
    let totalScore = 0;
    let maxScore = 0;
    
    checkboxes.forEach(checkbox => {
        const points = parseInt(checkbox.dataset.points);
        maxScore += points;
        if (checkbox.checked) {
            totalScore += points;
        }
    });
    
    const percentage = Math.round((totalScore / maxScore) * 100);
    
    // Display score
    const scoreDisplay = document.getElementById('score-display');
    scoreDisplay.style.display = 'block';
    
    document.getElementById('score-value').textContent = percentage + '%';
    
    // Determine rank
    let rank = '';
    let rankClass = '';
    
    if (percentage >= 90) {
        rank = '🌟 Ayurvedic Yogi';
        rankClass = 'yogi';
    } else if (percentage >= 70) {
        rank = '🌿 Disciplined Seeker';
        rankClass = 'seeker';
    } else if (percentage >= 50) {
        rank = '🌱 Beginner';
        rankClass = 'beginner';
    } else {
        rank = '⚠️ Out of Balance';
        rankClass = 'unbalanced';
    }
    
    const rankBadge = document.getElementById('rank-badge');
    rankBadge.textContent = rank;
    rankBadge.className = 'rank-badge ' + rankClass;
    
    // Save to backend (if endpoint exists)
    // fetch('http://localhost:5000/save_score', { ... });
    
    // Scroll to score
    scoreDisplay.scrollIntoView({ behavior: 'smooth' });
}

