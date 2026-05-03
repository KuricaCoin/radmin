const blurVideo = document.getElementById('blurVideo');
const normalVideo = document.getElementById('normalVideo');
const blurLayer = document.querySelector('.blur-layer');
const videoWrapper = document.getElementById('videoWrapper');
const radminTitle = document.getElementById('radminTitle');

let pulseStarted = false;
let animationFrameId = null;

function startPulse() {
    if (pulseStarted) return;
    pulseStarted = true;
    if (blurLayer) {
        blurLayer.style.animation = 'pulse 9s ease-in-out infinite';
    }
}

function stopPulse() {
    if (blurLayer) {
        blurLayer.style.animation = 'none';
    }
    pulseStarted = false;
}

function playBothVideos() {
    stopPulse();
    
    if (normalVideo) {
        normalVideo.currentTime = 0;
        const playPromise = normalVideo.play();
        if (playPromise !== undefined) {
            playPromise.catch(e => console.log("normal play error:", e));
        }
    }
    if (blurVideo) {
        blurVideo.currentTime = 0;
        const playPromise = blurVideo.play();
        if (playPromise !== undefined) {
            playPromise.catch(e => console.log("blur play error:", e));
        }
    }
}

function handleScrollBlur() {
    const scrollY = window.scrollY;
    const maxScroll = window.innerHeight * 1.5;
    let scrollPercent = Math.min(scrollY / maxScroll, 1);
    scrollPercent = Math.pow(scrollPercent, 0.8);
    
    const maxBlur = 25;
    const currentBlur = scrollPercent * maxBlur;
    
    const maxTitleBlur = 20;
    const currentTitleBlur = scrollPercent * maxTitleBlur;
    const minTitleOpacity = 0.3;
    const titleOpacity = Math.max(1 - scrollPercent * 0.7, minTitleOpacity);
    
    if (videoWrapper) {
        videoWrapper.style.filter = `blur(${currentBlur}px)`;
    }
    
    if (radminTitle) {
        radminTitle.style.filter = `blur(${currentTitleBlur}px)`;
        radminTitle.style.opacity = titleOpacity;
    }
    
    animationFrameId = requestAnimationFrame(handleScrollBlur);
}

if (normalVideo) {
    normalVideo.addEventListener('ended', () => {
        startPulse();
    });
    
    normalVideo.addEventListener('loadeddata', () => {
        if (normalVideo.readyState >= 2 && blurVideo && blurVideo.readyState >= 2) {
            playBothVideos();
        } else if (normalVideo.readyState >= 2) {
            playBothVideos();
        }
    });
    
    normalVideo.addEventListener('error', () => {
        startPulse();
    });
}

if (blurVideo) {
    blurVideo.addEventListener('loadeddata', () => {
        if (normalVideo && normalVideo.readyState >= 2) {
            playBothVideos();
        } else if (normalVideo && normalVideo.readyState >= 1) {
            playBothVideos();
        }
    });
    blurVideo.addEventListener('error', () => {});
}

setTimeout(() => {
    if (normalVideo && normalVideo.paused && !pulseStarted) {
        if (normalVideo.readyState >= 2) {
            playBothVideos();
        } else {
            startPulse();
        }
    } else if (normalVideo && normalVideo.paused && normalVideo.readyState < 2) {
        startPulse();
    }
}, 1200);

window.addEventListener('load', () => {
    setTimeout(() => {
        if (normalVideo && normalVideo.paused) {
            if (normalVideo.readyState >= 2 && blurVideo && blurVideo.readyState >= 2) {
                playBothVideos();
            } else if (normalVideo.readyState >= 2) {
                normalVideo.play().catch(e => console.log("autoplay blocked?", e));
                if(blurVideo) blurVideo.play().catch(e=>{});
            } else {
                startPulse();
            }
        }
    }, 100);
});

document.body.addEventListener('touchstart', () => {
    if (normalVideo && normalVideo.paused && !pulseStarted && normalVideo.currentTime === 0) {
        playBothVideos();
    }
}, { once: true });

const styleSheet = document.createElement("style");
styleSheet.textContent = `
    @keyframes pulse {
        0% {
            filter: blur(50px);
            opacity: 0.4;
            transform: scale(1.1);
        }
        50% {
            filter: blur(65px);
            opacity: 0.6;
            transform: scale(1.15);
        }
        100% {
            filter: blur(50px);
            opacity: 0.4;
            transform: scale(1.1);
        }
    }
    .blur-layer {
        animation: none;
    }
`;
document.head.appendChild(styleSheet);

const cards = document.querySelectorAll('.card');

function checkCards() {
    const windowHeight = window.innerHeight;
    const triggerBottom = windowHeight - 100;
    
    cards.forEach(card => {
        const cardTop = card.getBoundingClientRect().top;
        
        if (cardTop < triggerBottom) {
            card.classList.add('revealed');
        }
    });
}

window.addEventListener('scroll', checkCards);
window.addEventListener('load', checkCards);
setTimeout(checkCards, 500);

const pozorCard = document.getElementById('cardPozor');
if (pozorCard) {
    pozorCard.addEventListener('click', () => {
        window.open('https://t.me/radminvpnminecraftss', '_blank');
    });
}

handleScrollBlur();