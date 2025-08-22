// Login form submission
document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    // Simple authentication (in a real application, this would be handled by a server)
    if (username === 'admin' && password === 'admin123') {
        // Store authentication status
        localStorage.setItem('authenticated', 'true');
        // Redirect to dashboard
        window.location.href = 'dashboard.html';
    } else {
        alert('Invalid username or password. Try admin/admin123 for demo.');
    }
});

// Check if user is already authenticated
if (localStorage.getItem('authenticated') === 'true' && window.location.pathname.endsWith('login.html')) {
    window.location.href = 'dashboard.html';
}
