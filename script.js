// Disappearing header functionality
document.addEventListener('DOMContentLoaded', function() {
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