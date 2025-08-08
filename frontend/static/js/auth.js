// Gestion de l'authentification
document.addEventListener('DOMContentLoaded', function() {
    initAuthTabs();
    initAuthForms();
    checkAuthStatus();
});

// Gestion des onglets (Connexion/Inscription)
function initAuthTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const authForms = document.querySelectorAll('.auth-form');
    
    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const targetTab = this.getAttribute('data-tab');
            
            // Retirer la classe active de tous les onglets
            tabBtns.forEach(b => b.classList.remove('active'));
            authForms.forEach(f => f.classList.remove('active'));
            
            // Ajouter la classe active à l'onglet cliqué
            this.classList.add('active');
            document.getElementById(`${targetTab}-form`).classList.add('active');
        });
    });
}

// Gestion des formulaires d'authentification
function initAuthForms() {
    const loginForm = document.getElementById('login-form-element');
    const registerForm = document.getElementById('register-form-element');
    
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
    
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }
}

// Vérifier le statut d'authentification
function checkAuthStatus() {
    const isLoggedIn = localStorage.getItem('isLoggedIn');
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    
    if (isLoggedIn === 'true' && user.id) {
        updateNavbarForLoggedInUser(user);
    }
}

// Mettre à jour la navbar pour l'utilisateur connecté
function updateNavbarForLoggedInUser(user) {
    const loginBtn = document.querySelector('.btn-login');
    if (loginBtn) {
        loginBtn.textContent = `Bonjour ${user.first_name || user.username}`;
        loginBtn.onclick = () => window.location.href = '/profile/';
    }
}

// Gestion de la connexion
async function handleLogin(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const loginData = Object.fromEntries(formData);
    
    // Validation
    if (!validateLoginForm(loginData)) {
        return;
    }
    
    // Afficher l'indicateur de chargement
    const submitBtn = e.target.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Connexion en cours...';
    submitBtn.disabled = true;
    
    try {
        // Appel à l'API Django pour la connexion
        const response = await fetch('/api/auth/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify({
                username: loginData.email,
                password: loginData.password
            })
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            showSuccess('Connexion réussie ! Redirection...');
            
            // Stocker les informations utilisateur
            localStorage.setItem('user', JSON.stringify(data.user));
            localStorage.setItem('isLoggedIn', 'true');
            localStorage.setItem('token', data.token);
            
            // Mettre à jour la navbar
            updateNavbarForLoggedInUser(data.user);
            
            // Redirection vers la page d'accueil
            setTimeout(() => {
                window.location.href = '/';
            }, 1500);
        } else {
            showError(data.message || 'Email ou mot de passe incorrect');
        }
        
    } catch (error) {
        showError('Erreur lors de la connexion. Veuillez réessayer.');
        console.error('Erreur login:', error);
        
    } finally {
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    }
}

// Gestion de l'inscription
async function handleRegister(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const registerData = Object.fromEntries(formData);
    
    // Validation
    if (!validateRegisterForm(registerData)) {
        return;
    }
    
    // Afficher l'indicateur de chargement
    const submitBtn = e.target.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Inscription en cours...';
    submitBtn.disabled = true;
    
    try {
        // Appel à l'API Django pour l'inscription
        const response = await fetch('/api/auth/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify({
                username: registerData.email,
                email: registerData.email,
                password: registerData.password,
                first_name: registerData.firstname,
                last_name: registerData.lastname
            })
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            showSuccess('Inscription réussie ! Vous pouvez maintenant vous connecter.');
            e.target.reset();
            
            // Basculer vers l'onglet de connexion
            document.querySelector('[data-tab="login"]').click();
            
        } else {
            showError(data.message || 'Erreur lors de l\'inscription');
        }
        
    } catch (error) {
        showError('Erreur lors de l\'inscription. Veuillez réessayer.');
        console.error('Erreur register:', error);
        
    } finally {
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    }
}

// Validation du formulaire de connexion
function validateLoginForm(data) {
    const errors = [];
    
    if (!data.email || !isValidEmail(data.email)) {
        errors.push('Veuillez entrer une adresse email valide');
    }
    
    if (!data.password || data.password.length < 6) {
        errors.push('Le mot de passe doit contenir au moins 6 caractères');
    }
    
    if (errors.length > 0) {
        showError(errors.join('\n'));
        return false;
    }
    
    return true;
}

// Validation du formulaire d'inscription
function validateRegisterForm(data) {
    const errors = [];
    
    if (!data.firstname || data.firstname.trim().length < 2) {
        errors.push('Le prénom doit contenir au moins 2 caractères');
    }
    
    if (!data.lastname || data.lastname.trim().length < 2) {
        errors.push('Le nom doit contenir au moins 2 caractères');
    }
    
    if (!data.email || !isValidEmail(data.email)) {
        errors.push('Veuillez entrer une adresse email valide');
    }
    
    if (!data.password || data.password.length < 6) {
        errors.push('Le mot de passe doit contenir au moins 6 caractères');
    }
    
    if (data.password !== data.confirm_password) {
        errors.push('Les mots de passe ne correspondent pas');
    }
    
    if (!data.terms) {
        errors.push('Vous devez accepter les conditions d\'utilisation');
    }
    
    if (errors.length > 0) {
        showError(errors.join('\n'));
        return false;
    }
    
    return true;
}

// Validation d'email
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Obtenir le token CSRF
function getCSRFToken() {
    const token = document.querySelector('meta[name="csrf-token"]');
    return token ? token.getAttribute('content') : '';
}

// Fonction pour afficher les messages de succès
function showSuccess(message) {
    const successDiv = document.createElement('div');
    successDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #00C851;
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        z-index: 10001;
        max-width: 400px;
        box-shadow: 0 4px 12px rgba(0, 200, 81, 0.3);
        animation: slideInRight 0.3s ease-out;
    `;
    successDiv.textContent = message;
    
    document.body.appendChild(successDiv);
    
    setTimeout(() => {
        successDiv.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => {
            successDiv.remove();
        }, 300);
    }, 5000);
}

// Fonction pour afficher les messages d'erreur
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #ff4444;
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        z-index: 10001;
        max-width: 400px;
        box-shadow: 0 4px 12px rgba(255, 68, 68, 0.3);
        animation: slideInRight 0.3s ease-out;
        white-space: pre-line;
    `;
    errorDiv.textContent = message;
    
    document.body.appendChild(errorDiv);
    
    setTimeout(() => {
        errorDiv.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => {
            errorDiv.remove();
        }, 300);
    }, 5000);
}

// Fonction de déconnexion
function logout() {
    localStorage.removeItem('user');
    localStorage.removeItem('isLoggedIn');
    localStorage.removeItem('token');
    window.location.href = '/';
}

// Animations CSS pour les notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(100%);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideOutRight {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(100%);
        }
    }
`;
document.head.appendChild(style); 