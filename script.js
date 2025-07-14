// Disappearing header functionality
document.addEventListener('DOMContentLoaded', function() {
    // Retro animation functions
    function createRetroOverlay(className, barClassName) {
        const overlay = document.createElement('div');
        overlay.className = className;
        
        // Create 12 bars for the animation
        for (let i = 0; i < 12; i++) {
            const bar = document.createElement('div');
            bar.className = barClassName;
            overlay.appendChild(bar);
        }
        
        return overlay;
    }
    
    function triggerRetroAnimation() {
        const body = document.body;
        body.classList.add('animating');
        
        const overlay = createRetroOverlay('retro-overlay', 'retro-bar');
        document.body.appendChild(overlay);
        
        // Remove overlay after animation completes
        setTimeout(() => {
            if (overlay.parentNode) {
                overlay.parentNode.removeChild(overlay);
            }
            body.classList.remove('animating');
        }, 1200); // Slightly longer than animation duration
    }
    
    function triggerModeSwitchAnimation() {
        const body = document.body;
        body.classList.add('animating');
        
        const overlay = createRetroOverlay('mode-switch-overlay', 'mode-switch-bar');
        document.body.appendChild(overlay);
        
        // Remove overlay after animation completes
        setTimeout(() => {
            if (overlay.parentNode) {
                overlay.parentNode.removeChild(overlay);
            }
            body.classList.remove('animating');
        }, 800); // Slightly longer than animation duration
    }
    
    // Trigger initial page load animation
    setTimeout(() => {
        triggerRetroAnimation();
    }, 100);
    
    // Set current date
    function setCurrentDate() {
        const dateElement = document.querySelector('.date');
        if (dateElement) {
            const today = new Date();
            const options = { 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric' 
            };
            const formattedDate = today.toLocaleDateString('en-US', options);
            dateElement.textContent = formattedDate;
        }
    }
    
    // Initialize current date
    setCurrentDate();
    
    const header = document.getElementById('main-header');
    let lastScrollTop = 0;
    let scrollThreshold = 50; // Minimum scroll distance before hiding header
    
    // Function to handle scroll events
    function handleScroll() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Only hide/show header if we've scrolled more than the threshold
        if (Math.abs(scrollTop - lastScrollTop) > scrollThreshold) {
            if (scrollTop > lastScrollTop && scrollTop > 100) {
                // Scrolling down - hide header
                header.classList.add('hidden');
            } else {
                // Scrolling up - show header
                header.classList.remove('hidden');
            }
            lastScrollTop = scrollTop;
        }
    }
    
    // Add scroll event listener with throttling for better performance
    let ticking = false;
    function requestTick() {
        if (!ticking) {
            requestAnimationFrame(function() {
                handleScroll();
                ticking = false;
            });
            ticking = true;
        }
    }
    
    window.addEventListener('scroll', requestTick);
    
    // Show header when at the top of the page
    window.addEventListener('scroll', function() {
        if (window.pageYOffset === 0) {
            header.classList.remove('hidden');
        }
    });
    
    // Smooth scrolling for navigation links
    document.querySelectorAll('.nav-menu a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const headerHeight = header.offsetHeight;
                const targetPosition = target.offsetTop - headerHeight - 10;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
                
                // Show header when navigating
                header.classList.remove('hidden');
            }
        });
    });
    
    // Add retro newspaper sound effects (optional)
    function addRetroEffects() {
        // Add click sound for navigation
        document.querySelectorAll('.nav-menu a').forEach(link => {
            link.addEventListener('click', function() {
                // Create a subtle click effect
                this.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    this.style.transform = 'scale(1)';
                }, 100);
            });
        });
        
        // Add page load effect
        document.body.style.opacity = '0';
        setTimeout(() => {
            document.body.style.transition = 'opacity 0.5s ease-in';
            document.body.style.opacity = '1';
        }, 100);
    }
    
    // Initialize retro effects
    addRetroEffects();
    
    // Add touch support for mobile devices
    let touchStartY = 0;
    let touchEndY = 0;
    
    document.addEventListener('touchstart', function(e) {
        touchStartY = e.changedTouches[0].screenY;
    });
    
    document.addEventListener('touchend', function(e) {
        touchEndY = e.changedTouches[0].screenY;
        handleTouchSwipe();
    });
    
    function handleTouchSwipe() {
        const swipeThreshold = 50;
        const diff = touchStartY - touchEndY;
        
        if (Math.abs(diff) > swipeThreshold) {
            if (diff > 0) {
                // Swipe up - hide header
                header.classList.add('hidden');
            } else {
                // Swipe down - show header
                header.classList.remove('hidden');
            }
        }
    }
    
    // Add keyboard navigation support
    document.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowUp' || e.key === 'ArrowDown') {
            // Show header when using arrow keys
            header.classList.remove('hidden');
        }
    });
    
    // Performance optimization: pause scroll listener when page is not visible
    document.addEventListener('visibilitychange', function() {
        if (document.hidden) {
            window.removeEventListener('scroll', requestTick);
        } else {
            window.addEventListener('scroll', requestTick);
        }
    });
});

// Weather API integration
document.addEventListener('DOMContentLoaded', function() {
    // Weather API (Open-Meteo example, no API key required)
    function updateWeather() {
        // Waterloo, ON coordinates
        const lat = 43.4643;
        const lon = -80.5204;
        const url = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current_weather=true&daily=temperature_2m_max,temperature_2m_min,weathercode&timezone=America%2FToronto`;

        fetch(url)
            .then(response => response.json())
            .then(data => {
                const weatherInfo = document.getElementById('weather-info');
                if (!weatherInfo || !data.current_weather) return;

                const temp = Math.round(data.current_weather.temperature);
                const code = data.current_weather.weathercode;
                const max = Math.round(data.daily.temperature_2m_max[0]);
                const min = Math.round(data.daily.temperature_2m_min[0]);

                // Simple weather code mapping
                const conditions = {
                    0: "Clear",
                    1: "Mainly Clear",
                    2: "Partly Cloudy",
                    3: "Overcast",
                    45: "Fog",
                    48: "Depositing Rime Fog",
                    51: "Light Drizzle",
                    53: "Drizzle",
                    55: "Dense Drizzle",
                    61: "Light Rain",
                    63: "Rain",
                    65: "Heavy Rain",
                    71: "Light Snow",
                    73: "Snow",
                    75: "Heavy Snow",
                    80: "Rain Showers",
                    81: "Rain Showers",
                    82: "Violent Rain Showers",
                    95: "Thunderstorm"
                };

                weatherInfo.querySelector('.temp').textContent = `${temp}°C`;
                weatherInfo.querySelector('.condition').textContent = conditions[code] || "Unknown";
                weatherInfo.querySelector('.forecast').textContent = `High: ${max}°C | Low: ${min}°C`;
            })
            .catch(() => {
                const weatherInfo = document.getElementById('weather-info');
                if (weatherInfo) {
                    weatherInfo.querySelector('.temp').textContent = "N/A";
                    weatherInfo.querySelector('.condition').textContent = "Unavailable";
                    weatherInfo.querySelector('.forecast').textContent = "";
                }
            });
    }

    updateWeather();
});

// Desktop Mode Toggle Functionality
document.addEventListener('DOMContentLoaded', function() {
    const desktopToggle = document.getElementById('desktop-toggle');
    const body = document.body;
    
    // Retro animation functions for mode switching
    function createRetroOverlay(className, barClassName) {
        const overlay = document.createElement('div');
        overlay.className = className;
        
        // Create 12 bars for the animation
        for (let i = 0; i < 12; i++) {
            const bar = document.createElement('div');
            bar.className = barClassName;
            overlay.appendChild(bar);
        }
        
        return overlay;
    }
    
    function triggerModeSwitchAnimation() {
        const body = document.body;
        body.classList.add('animating');
        
        const overlay = createRetroOverlay('mode-switch-overlay', 'mode-switch-bar');
        document.body.appendChild(overlay);
        
        // Remove overlay after animation completes
        setTimeout(() => {
            if (overlay.parentNode) {
                overlay.parentNode.removeChild(overlay);
            }
            body.classList.remove('animating');
        }, 800); // Slightly longer than animation duration
    }
    
    // Check if desktop mode preference is stored
    const isDesktopMode = localStorage.getItem('shadweb-desktop-mode') === 'true';
    
    // Apply desktop mode if previously enabled
    if (isDesktopMode) {
        body.classList.add('desktop-mode');
    }
    
    function updateToggleButton(isDesktopMode) {
        if (!desktopToggle) return;
        
        const toggleIcon = desktopToggle.querySelector('.toggle-icon');
        const toggleText = desktopToggle.querySelector('.toggle-text');
        
        if (isDesktopMode) {
            toggleIcon.textContent = '💻';
            toggleText.textContent = 'Mobile Mode';
        } else {
            toggleIcon.textContent = '📱';
            toggleText.textContent = 'Desktop Mode';
        }
    }
    
    // Initialize button state
    updateToggleButton(isDesktopMode);
    
    // Desktop mode toggle functionality
    if (desktopToggle) {
        desktopToggle.addEventListener('click', function() {
            const isCurrentlyDesktop = body.classList.contains('desktop-mode');
            
            // Trigger mode switch animation first
            triggerModeSwitchAnimation();
            
            // Delay the actual mode switch to allow animation to start
            setTimeout(() => {
                if (isCurrentlyDesktop) {
                    // Switch to mobile mode
                    body.classList.remove('desktop-mode');
                    localStorage.setItem('shadweb-desktop-mode', 'false');
                    updateToggleButton(false);
                } else {
                    // Switch to desktop mode
                    body.classList.add('desktop-mode');
                    localStorage.setItem('shadweb-desktop-mode', 'true');
                    updateToggleButton(true);
                }
                
                // Add a subtle transition effect
                body.style.transition = 'all 0.3s ease';
                setTimeout(() => {
                    body.style.transition = '';
                }, 300);
            }, 100); // Small delay to let animation start
        });
    }
    

    
    // Auto-detect screen size and suggest desktop mode for large screens
    function checkScreenSize() {
        const isLargeScreen = window.innerWidth >= 1200;
        const hasUsedDesktopMode = localStorage.getItem('shadweb-desktop-mode') !== null;
        
        if (isLargeScreen && !hasUsedDesktopMode && desktopToggle) {
            // Show a subtle hint for large screens
            setTimeout(() => {
                desktopToggle.style.animation = 'pulse 2s ease-in-out';
                setTimeout(() => {
                    desktopToggle.style.animation = '';
                }, 2000);
            }, 3000);
        }
    }
    
    // Check screen size on load and resize
    checkScreenSize();
    window.addEventListener('resize', checkScreenSize);
});

// Add pulse animation for the hint
const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
`;
document.head.appendChild(style);