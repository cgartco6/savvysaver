// Check authentication
if (localStorage.getItem('authenticated') !== 'true' && !window.location.pathname.endsWith('login.html')) {
    window.location.href = 'login.html';
}

// Logout functionality
document.getElementById('logoutBtn').addEventListener('click', function(e) {
    e.preventDefault();
    localStorage.removeItem('authenticated');
    window.location.href = 'login.html';
});

// Refresh button
document.getElementById('refreshBtn').addEventListener('click', function() {
    alert('Data refreshed!');
    // In a real application, this would fetch new data from the server
});

// Export button
document.getElementById('exportBtn').addEventListener('click', function() {
    alert('Data exported to Excel format!');
    // In a real application, this would generate and download an Excel file
});

// Initialize charts
function initCharts() {
    // Signups Growth Chart
    const signupsCtx = document.getElementById('signupsChart').getContext('2d');
    const signupsChart = new Chart(signupsCtx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'],
            datasets: [{
                label: 'Monthly Signups',
                data: [12, 19, 15, 24, 22, 31, 45, 52, 68, 87],
                borderColor: '#3498db',
                backgroundColor: 'rgba(52, 152, 219, 0.1)',
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                }
            }
        }
    });
    
    // Province Chart
    const provinceCtx = document.getElementById('provinceChart').getContext('2d');
    const provinceChart = new Chart(provinceCtx, {
        type: 'doughnut',
        data: {
            labels: ['Gauteng', 'Western Cape', 'KZN', 'Eastern Cape', 'Other'],
            datasets: [{
                data: [35, 28, 15, 12, 10],
                backgroundColor: [
                    '#e74c3c',
                    '#3498db',
                    '#2ecc71',
                    '#f39c12',
                    '#9b59b6'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                }
            }
        }
    });
}

// Initialize charts when page loads
document.addEventListener('DOMContentLoaded', initCharts);
