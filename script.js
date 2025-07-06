// Disappearing header functionality
document.addEventListener('DOMContentLoaded', function() {
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