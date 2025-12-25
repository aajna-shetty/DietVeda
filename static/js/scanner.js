// Tongue Scanner Logic

let video = null;
let stream = null;
let scanning = false;
let scanInterval = null;

document.addEventListener('DOMContentLoaded', function() {
    video = document.getElementById('videoElement');
    const startBtn = document.getElementById('start-scan-btn');
    const stopBtn = document.getElementById('stop-scan-btn');
    const scanBox = document.getElementById('scan-box');
    const diagnosisOverlay = document.getElementById('diagnosis-overlay');

    if (startBtn) {
        startBtn.addEventListener('click', startScanning);
    }

    if (stopBtn) {
        stopBtn.addEventListener('click', stopScanning);
    }
});

async function startScanning() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
        
        document.getElementById('start-scan-btn').style.display = 'none';
        document.getElementById('stop-scan-btn').style.display = 'inline-block';
        document.getElementById('scan-box').style.display = 'block';
        document.getElementById('diagnosis-overlay').style.display = 'block';
        
        scanning = true;
        
        // Position scan box in center
        const box = document.getElementById('scan-box');
        const videoRect = video.getBoundingClientRect();
        const boxSize = 200;
        box.style.width = boxSize + 'px';
        box.style.height = boxSize + 'px';
        box.style.left = (videoRect.width / 2 - boxSize / 2) + 'px';
        box.style.top = (videoRect.height / 2 - boxSize / 2) + 'px';
        
        // Start analyzing
        scanInterval = setInterval(analyzeTongue, 100);
    } catch (error) {
        console.error('Error accessing webcam:', error);
        alert('Could not access webcam. Please check permissions.');
    }
}

function stopScanning() {
    scanning = false;
    
    if (scanInterval) {
        clearInterval(scanInterval);
    }
    
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
    
    if (video) {
        video.srcObject = null;
    }
    
    document.getElementById('start-scan-btn').style.display = 'inline-block';
    document.getElementById('stop-scan-btn').style.display = 'none';
    document.getElementById('scan-box').style.display = 'none';
    document.getElementById('diagnosis-overlay').style.display = 'none';
}

function analyzeTongue() {
    if (!video || !scanning) return;
    
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.drawImage(video, 0, 0);
    
    // Get center region (simulating the scan box)
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const boxSize = 200;
    
    const imageData = ctx.getImageData(
        centerX - boxSize / 2,
        centerY - boxSize / 2,
        boxSize,
        boxSize
    );
    
    // Calculate average RGB
    let r = 0, g = 0, b = 0;
    const pixels = imageData.data;
    for (let i = 0; i < pixels.length; i += 4) {
        r += pixels[i];
        g += pixels[i + 1];
        b += pixels[i + 2];
    }
    
    const pixelCount = pixels.length / 4;
    r = Math.floor(r / pixelCount);
    g = Math.floor(g / pixelCount);
    b = Math.floor(b / pixelCount);
    
    // Update display
    document.getElementById('r-value').textContent = r;
    document.getElementById('g-value').textContent = g;
    document.getElementById('b-value').textContent = b;
    
    // Diagnose
    let diagnosis = '';
    let className = '';
    
    if (r > 160 && g < 120 && b < 120) {
        diagnosis = '🔥 High Pitta – Redness detected';
        className = 'pitta';
    } else if (r > 180 && g > 180 && b > 180) {
        diagnosis = '❄️ Kapha Ama – White coating found';
        className = 'kapha';
    } else if (r > 130 && g < 140) {
        diagnosis = '🌸 Healthy Pink — Balanced Agni';
        className = 'healthy';
    } else {
        diagnosis = '⚠️ Adjust Lighting';
        className = '';
    }
    
    const label = document.getElementById('diagnosis-label');
    label.textContent = diagnosis;
    label.className = 'diagnosis-label ' + className;
}

