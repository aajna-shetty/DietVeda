// Diet Recommendations Logic

let currentDosha = localStorage.getItem('userDosha') || 'Vata';
let currentMeal = 'All';
let currentRecommendations = [];

document.addEventListener('DOMContentLoaded', function() {
    const doshaSelect = document.getElementById('dosha-select');
    if (doshaSelect) {
        doshaSelect.value = currentDosha;
        doshaSelect.addEventListener('change', function() {
            currentDosha = this.value;
            loadRecommendations();
        });
    }

    // Meal filter buttons
    const mealButtons = document.querySelectorAll('.meal-btn');
    mealButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            mealButtons.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            currentMeal = this.dataset.meal;
            filterRecommendations();
        });
    });

    // Download button
    const downloadBtn = document.getElementById('download-btn');
    if (downloadBtn) {
        downloadBtn.addEventListener('click', downloadPDF);
    }

    loadRecommendations();
});

async function loadRecommendations() {
    const container = document.getElementById('food-cards');
    showLoading(container);

    try {
        const response = await fetch('http://localhost:5000/get_diet', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ dosha: currentDosha, meal: currentMeal === 'All' ? '' : currentMeal })
        });

        const data = await response.json();
        currentRecommendations = data;
        displayRecommendations(data);
        
        if (data.length > 0) {
            document.getElementById('download-btn').style.display = 'block';
        }
    } catch (error) {
        console.error('Error:', error);
        container.innerHTML = '<p style="text-align: center; color: red;">Error loading recommendations. Please try again.</p>';
    }
}

function filterRecommendations() {
    if (currentMeal === 'All') {
        displayRecommendations(currentRecommendations);
    } else {
        const filtered = currentRecommendations.filter(item => 
            item.meal_type && item.meal_type.toLowerCase() === currentMeal.toLowerCase()
        );
        displayRecommendations(filtered);
    }
}

function displayRecommendations(recommendations) {
    const container = document.getElementById('food-cards');
    
    if (!recommendations || recommendations.length === 0) {
        container.innerHTML = '<p style="text-align: center; color: var(--text-medium); font-size: 1.2rem;">No recommendations found for this selection.</p>';
        return;
    }

    container.innerHTML = recommendations.map(item => `
        <div class="food-card">
            <div class="dish-header">
                <h3 class="dish-name">${item.dish_name || 'Unknown Dish'}</h3>
                ${item.season ? `<div class="season-tag">${getSeasonIcon(item.season)} ${item.season}</div>` : ''}
            </div>
            <div class="ingredients">
                <span class="ingredient-icon">🌿</span>
                <span class="ingredient-text">${item.ingredients || 'N/A'}</span>
            </div>
            <div class="food-details">
                ${item.taste_profile ? `<div class="taste-profile">✨ ${item.taste_profile}</div>` : ''}
                ${item.effect ? `<div class="effect-info">💚 ${item.effect}</div>` : ''}
            </div>
        </div>
    `).join('');
}

function getSeasonIcon(season) {
    const icons = {
        'Winter': '❄️',
        'Summer': '☀️',
        'Monsoon': '🌧️',
        'Spring': '🌸',
        'Autumn': '🍂'
    };
    return icons[season] || '🌿';
}

async function downloadPDF() {
    try {
        const meal = currentMeal === 'All' ? 'all' : currentMeal.toLowerCase();
        // Create a temporary link to trigger download
        const link = document.createElement('a');
        link.href = `http://localhost:5000/download/filtered/${encodeURIComponent(currentDosha)}/${encodeURIComponent(meal)}`;
        link.download = `dietveda_${currentDosha}_${meal}.pdf`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    } catch (error) {
        console.error('Error downloading PDF:', error);
        alert('Error downloading PDF. Please try again.');
    }
}

