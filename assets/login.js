// Tab switching
function showTab(tabName) {
    // Update tab buttons
    document.querySelectorAll('.auth-tab').forEach(tab => {
        tab.classList.remove('active');
    });
    event.target.classList.add('active');

    // Update form visibility
    document.querySelectorAll('.auth-form').forEach(form => {
        form.classList.remove('active');
    });
    document.getElementById(`${tabName}-form`).classList.add('active');

    // Clear any error messages
    clearErrors();
    hideSuccessMessage();
}

// Password toggle
function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    const button = input.nextElementSibling;

    if (input.type === 'password') {
        input.type = 'text';
        button.textContent = 'Hide';
    } else {
        input.type = 'password';
        button.textContent = 'Show';
    }
}

// Form validation
function validateEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function validateUsername(username) {
    return username.length >= 3 && username.length <= 20 && /^[a-zA-Z0-9_]+$/.test(username);
}

function validatePassword(password) {
    return password.length >= 8;
}

function showError(inputId, message) {
    const input = document.getElementById(inputId);
    const error = document.getElementById(`${inputId}-error`);

    input.classList.add('error');
    error.textContent = message;
    error.classList.add('show');
}

function clearErrors() {
    document.querySelectorAll('.form-input').forEach(input => {
        input.classList.remove('error');
    });
    document.querySelectorAll('.error-message').forEach(error => {
        error.classList.remove('show');
    });
}

function showSuccessMessage(message) {
    const successDiv = document.getElementById('success-message');
    successDiv.textContent = message;
    successDiv.classList.add('show');
}

function hideSuccessMessage() {
    document.getElementById('success-message').classList.remove('show');
}

function setLoading(buttonId, isLoading) {
    const button = document.getElementById(buttonId);
    if (isLoading) {
        button.classList.add('loading');
        button.disabled = true;
    } else {
        button.classList.remove('loading');
        button.disabled = false;
    }
}

// Login form submission
document.getElementById('login-form').addEventListener('submit', function(e) {
    e.preventDefault();
    clearErrors();

    const username = document.getElementById('login-username').value.trim();
    const password = document.getElementById('login-password').value;

    let isValid = true;

    if (!username) {
        showError('login-username', 'Username or email is required');
        isValid = false;
    }

    if (!password) {
        showError('login-password', 'Password is required');
        isValid = false;
    }

    if (isValid) {
        setLoading('login-btn', true);

        // Simulate API call
        setTimeout(() => {
            setLoading('login-btn', false);

            // Here you would integrate with your Django login view
            console.log('Login attempt:', { username, password });

            // Simulate successful login
            if (username === 'admin' && password === 'password') {
                window.location.href = '/'; // Redirect to main page
            } else {
                showError('login-password', 'Invalid username or password');
            }
        }, 1500);
    }
});

// Register form submission
document.getElementById('register-form').addEventListener('submit', function(e) {
    e.preventDefault();
    clearErrors();

    const fullname = document.getElementById('register-fullname').value.trim();
    const username = document.getElementById('register-username').value.trim();
    const email = document.getElementById('register-email').value.trim();
    const password = document.getElementById('register-password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    const agreeTerms = document.getElementById('agree-terms').checked;

    let isValid = true;

    if (!fullname) {
        showError('register-fullname', 'Full name is required');
        isValid = false;
    }

    if (!validateUsername(username)) {
        showError('register-username', 'Username must be 3-20 characters and contain only letters, numbers, and underscores');
        isValid = false;
    }

    if (!validateEmail(email)) {
        showError('register-email', 'Please enter a valid email address');
        isValid = false;
    }

    if (!validatePassword(password)) {
        showError('register-password', 'Password must be at least 8 characters long');
        isValid = false;
    }

    if (password !== confirmPassword) {
        showError('confirm-password', 'Passwords do not match');
        isValid = false;
    }

    if (!agreeTerms) {
        alert('You must agree to the Terms of Service and Privacy Policy');
        isValid = false;
    }

    if (isValid) {
        setLoading('register-btn', true);

        // Simulate API call
        setTimeout(() => {
            setLoading('register-btn', false);

            // Here you would integrate with your Django registration view
            console.log('Registration attempt:', { fullname, username, email, password });

            // Simulate successful registration
            showSuccessMessage('Account created successfully! You can now log in.');
            document.getElementById('register-form').reset();

            // Switch to login tab after a delay
            setTimeout(() => {
                showTab('login');
                document.querySelector('.auth-tab').click();
            }, 2000);
        }, 1500);
    }
});

// Real-time validation
document.getElementById('register-username').addEventListener('input', function() {
    const username = this.value.trim();
    if (username && !validateUsername(username)) {
        showError('register-username', 'Username must be 3-20 characters and contain only letters, numbers, and underscores');
    } else {
        document.getElementById('register-username-error').classList.remove('show');
        this.classList.remove('error');
    }
});

document.getElementById('register-email').addEventListener('input', function() {
    const email = this.value.trim();
    if (email && !validateEmail(email)) {
        showError('register-email', 'Please enter a valid email address');
    } else {
        document.getElementById('register-email-error').classList.remove('show');
        this.classList.remove('error');
    }
});

document.getElementById('confirm-password').addEventListener('input', function() {
    const password = document.getElementById('register-password').value;
    const confirmPassword = this.value;

    if (confirmPassword && password !== confirmPassword) {
        showError('confirm-password', 'Passwords do not match');
    } else {
        document.getElementById('confirm-password-error').classList.remove('show');
        this.classList.remove('error');
    }
});

// Forgot password
function showForgotPassword() {
    const email = prompt('Enter your email address to reset your password:');
    if (email && validateEmail(email)) {
        alert('Password reset link has been sent to your email!');
        // Here you would integrate with your Django password reset view
        console.log('Password reset for:', email);
    } else if (email) {
        alert('Please enter a valid email address.');
    }
}

// Social login buttons (placeholder)
document.querySelectorAll('.social-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        const provider = this.textContent.includes('Google') ? 'Google' : 'Facebook';
        alert(`${provider} login is not implemented yet. Please use the regular login form.`);
    });
});

// Back to home
document.querySelector('.back-to-home').addEventListener('click', function(e) {
    e.preventDefault();
    window.location.href = '/'; // Django home URL
});

// Focus first input on page load
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('login-username').focus();
});