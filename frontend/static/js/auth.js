// Gestion de l'authentification
document.addEventListener('DOMContentLoaded', function() {
    initAuthTabs();
    initAuthForms();
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
        // Simulation de connexion (remplacer par un vrai endpoint API)
        const response = await simulateLogin(loginData);
        
        if (response.success) {
            showSuccess('Connexion réussie ! Redirection...');
            // Stocker les informations utilisateur
            localStorage.setItem('user', JSON.stringify(response.user));
            localStorage.setItem('isLoggedIn', 'true');
            
            // Redirection vers la page d'accueil
            setTimeout(() => {
                window.location.href = '/';
            }, 1500);
        } else {
            showError(response.message);
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
        // Simulation d'inscription (remplacer par un vrai endpoint API)
        const response = await simulateRegister(registerData);
        
        if (response.success) {
            showSuccess('Inscription réussie ! Vous pouvez maintenant vous connecter.');
            e.target.reset();
            
            // Basculer vers l'onglet de connexion
            document.querySelector('[data-tab="login"]').click();
            
        } else {
            showError(response.message);
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

// Simulation de connexion
function simulateLogin(data) {
    return new Promise((resolve) => {
        setTimeout(() => {
            // Simulation d'une connexion réussie
            if (data.email === 'admin@aymencars.com' && data.password === 'admin123') {
                resolve({
                    success: true,
                    user: {
                        id: 1,
                        email: data.email,
                        first_name: 'Admin',
                        last_name: 'User'
                    }
                });
            } else {
                resolve({
                    success: false,
                    message: 'Email ou mot de passe incorrect'
                });
            }
        }, 1500);
    });
}

// Simulation d'inscription
function simulateRegister(data) {
    return new Promise((resolve) => {
        setTimeout(() => {
            // Simulation d'une inscription réussie
            resolve({
                success: true,
                user: {
                    id: Math.floor(Math.random() * 1000),
                    email: data.email,
                    first_name: data.firstname,
                    last_name: data.lastname
                }
            });
        }, 1500);
    });
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