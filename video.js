const blurVideo = document.getElementById('blurVideo');
const normalVideo = document.getElementById('normalVideo');
const blurLayer = document.querySelector('.blur-layer');

let pulseStarted = false;

function startPulse() {
    if (pulseStarted) return;
    pulseStarted = true;
    blurLayer.style.animation = 'pulse 9s ease-in-out infinite';
}

function stopPulse() {
    blurLayer.style.animation = 'none';
    pulseStarted = false;
}

function playBothVideos() {
    stopPulse();
    
    normalVideo.currentTime = 0;
    blurVideo.currentTime = 0;
    
    normalVideo.play();
    blurVideo.play();
}

normalVideo.addEventListener('ended', () => {
    startPulse();
});

normalVideo.addEventListener('loadeddata', () => {
    playBothVideos();
});

blurVideo.addEventListener('loadeddata', () => {
    if (normalVideo.readyState >= 2) {
        playBothVideos();
    }
});

setTimeout(() => {
    if (normalVideo.paused) {
        playBothVideos();
    }
}, 1000);