// Dark mode toggle functionality
document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;
    
    // Check if user has saved theme preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        body.setAttribute('data-theme', savedTheme);
        updateToggleButton(savedTheme);
    }
    
    // Toggle button click handler
    themeToggle.addEventListener('click', function() {
        const currentTheme = body.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        body.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateToggleButton(newTheme);
    });
    
    function updateToggleButton(theme) {
        if (theme === 'dark') {
            themeToggle.textContent = 'Light Mode';
        } else {
            themeToggle.textContent = 'Dark Mode';
        }
    }
    
    // Auto-refresh temperature data every 2 minutes (optional)
    if (window.location.pathname === '/') {
        setInterval(function() {
            fetch('/api/temperature')
                .then(response => response.json())
                .then(data => {
                    // Update temperature display without full page reload
                    updateTemperatureDisplay(data);
                })
                .catch(error => {
                    console.log('Could not fetch temperature update:', error);
                });
        }, 120000); // 2 minutes
    }
    
    function updateTemperatureDisplay(data) {
        // Simple update of temperature reading
        const tempElement = document.querySelector('.temp-reading');
        if (tempElement && data.temperature) {
            let statusBadge = '';
            if (data.status === 'alert') {
                statusBadge = '<span class="alert-badge">ALERT</span>';
            } else if (data.status === 'good') {
                statusBadge = '<span class="ok-badge">GOOD</span>';
            }
            
            tempElement.innerHTML = `${data.temperature}°F ${statusBadge}`;
        }
        
        // Update last check time
        const timeElement = document.querySelector('.time-reading');
        if (timeElement && data.last_check) {
            const checkTime = new Date(data.last_check);
            timeElement.textContent = checkTime.toLocaleString();
        }
        
        // Update alert count
        const alertElement = document.querySelector('.alert-count');
        if (alertElement) {
            alertElement.textContent = data.alerts_today;
        }
    }
});