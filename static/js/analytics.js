// Wellness Analytics Logic

document.addEventListener('DOMContentLoaded', function() {
    loadChart();
    loadInsights();
});

async function loadChart() {
    try {
        const response = await fetch('http://localhost:5000/analytics/graph');
        if (response.ok) {
            const blob = await response.blob();
            const url = URL.createObjectURL(blob);
            const img = document.getElementById('progress-chart');
            img.src = url;
            img.style.display = 'block';
            document.querySelector('.loading-spinner').style.display = 'none';
        } else {
            // Try to load from static file
            const img = document.getElementById('progress-chart');
            img.style.display = 'block';
            document.querySelector('.loading-spinner').style.display = 'none';
        }
    } catch (error) {
        console.error('Error loading chart:', error);
        document.querySelector('.loading-spinner').style.display = 'none';
    }
}

async function loadInsights() {
    try {
        const response = await fetch('http://localhost:5000/analytics/insights');
        const data = await response.json();
        
        const insights = data.insights || 'No insights available at this time.';
        displayInsights(insights);
    } catch (error) {
        console.error('Error loading insights:', error);
        displayInsights('Unable to load insights. Please try again later.');
    }
}

function displayInsights(insights) {
    const container = document.getElementById('insights-container');
    
    if (typeof insights === 'string') {
        container.innerHTML = `
            <div class="insight-item">
                <span class="insight-icon">✨</span>
                <p>${insights}</p>
            </div>
        `;
    } else if (Array.isArray(insights)) {
        container.innerHTML = insights.map(insight => {
            const icon = getInsightIcon(insight);
            return `
                <div class="insight-item">
                    <span class="insight-icon">${icon}</span>
                    <p>${insight}</p>
                </div>
            `;
        }).join('');
    } else {
        container.innerHTML = `
            <div class="insight-item">
                <span class="insight-icon">✨</span>
                <p>${JSON.stringify(insights)}</p>
            </div>
        `;
    }
}

function getInsightIcon(insight) {
    const text = insight.toLowerCase();
    if (text.includes('pitta')) return '🔥';
    if (text.includes('vata')) return '🌪️';
    if (text.includes('kapha')) return '🌊';
    if (text.includes('sattva') || text.includes('improving')) return '✨';
    if (text.includes('balance')) return '⚖️';
    return '🌿';
}

