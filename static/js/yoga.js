// Yoga Coach Logic

let dosha = localStorage.getItem('userDosha') || 'Vata';
let currentPoseIndex = 0;
let poses = [];
let timerInterval = null;
let remainingTime = 0;

document.addEventListener('DOMContentLoaded', function() {
    const doshaSelect = document.getElementById('dosha-select');
    if (doshaSelect) {
        doshaSelect.value = dosha;
        doshaSelect.addEventListener('change', function() {
            dosha = this.value;
            loadPoses();
        });
    }

    loadPoses();
});

async function loadPoses() {
    try {
        const response = await fetch(`http://localhost:5000/get_yoga?dosha=${dosha}`);
        const data = await response.json();
        poses = data;
        displayPoses();
    } catch (error) {
        console.error('Error loading poses:', error);
        // Fallback poses
        poses = getDefaultPoses();
        displayPoses();
    }
}

function getDefaultPoses() {
    return [
        { pose: 'Mountain Pose', duration: 60, url: 'https://www.youtube.com/watch?v=example1' },
        { pose: 'Warrior I', duration: 90, url: 'https://www.youtube.com/watch?v=example2' },
        { pose: 'Child\'s Pose', duration: 120, url: 'https://www.youtube.com/watch?v=example3' }
    ];
}

function displayPoses() {
    const container = document.getElementById('poses-container');
    
    container.innerHTML = poses.map((pose, index) => `
        <div class="pose-card">
            <h2 class="pose-name">${pose.pose}</h2>
            <p class="pose-sanskrit">${pose.pose.replace(/\s/g, '')}asana</p>
            
            <div class="mandala-timer" id="timer-${index}" style="display: none;">
                <span id="timer-value-${index}">0:00</span>
            </div>
            
            <div style="margin: 2rem 0;">
                <button class="btn-primary" onclick="startPose(${index})">Start Pose</button>
                <button class="btn-secondary" onclick="openVideo('${pose.url}')" style="margin-left: 1rem;">Watch Video</button>
            </div>
        </div>
    `).join('');
}

function startPose(index) {
    const pose = poses[index];
    if (!pose) return;
    
    remainingTime = pose.duration || 60;
    const timerElement = document.getElementById(`timer-${index}`);
    const timerValue = document.getElementById(`timer-value-${index}`);
    
    timerElement.style.display = 'flex';
    
    if (timerInterval) {
        clearInterval(timerInterval);
    }
    
    timerInterval = setInterval(() => {
        remainingTime--;
        const minutes = Math.floor(remainingTime / 60);
        const seconds = remainingTime % 60;
        timerValue.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
        
        if (remainingTime <= 0) {
            clearInterval(timerInterval);
            timerValue.textContent = 'Complete! 🎉';
            setTimeout(() => {
                timerElement.style.display = 'none';
            }, 3000);
        }
    }, 1000);
    
    // Auto-open video
    if (pose.url) {
        setTimeout(() => openVideo(pose.url), 1000);
    }
}

function openVideo(url) {
    window.open(url, '_blank');
}

