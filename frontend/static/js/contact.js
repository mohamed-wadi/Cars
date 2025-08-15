// Gestion du formulaire de contact
document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.getElementById('contact-form');
    
    if (contactForm) {
        contactForm.addEventListener('submit', handleContactSubmit);
    }
    
    // Animation des éléments au scroll
    initContactAnimations();
});

// Gestion de la soumission du formulaire de contact
async function handleContactSubmit(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const formObject = Object.fromEntries(formData);
    
    // Validation côté client
    if (!validateContactForm(formObject)) {
        return;
    }
    
    // Afficher un indicateur de chargement
    const submitBtn = e.target.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Envoi en cours...';
    submitBtn.disabled = true;
    
    try {
        // Construction du payload attendu par l'API
        const payload = {
            name: `${formObject.firstname} ${formObject.lastname}`.trim(),
            email: formObject.email,
            phone: formObject.phone || '',
            subject: formObject.subject,
            message: formObject.message
        };
        
        const res = await fetch('/api/contact/submit/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }, // endpoint CSRF-exempt côté serveur
            body: JSON.stringify(payload),
            credentials: 'same-origin'
        });
        
        if (!res.ok) {
            throw new Error('Erreur API');
        }
        
        const data = await res.json();
        if (data && data.success) {
            showSuccess('Votre message a été envoyé avec succès !');
            e.target.reset();
        } else {
            throw new Error('Réponse invalide');
        }
        
    } catch (error) {
        showError('Erreur lors de l\'envoi du message. Veuillez réessayer.');
        console.error('Erreur contact:', error);
        
    } finally {
        // Restaurer le bouton
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    }
}

// Validation du formulaire de contact
function validateContactForm(data) {
    const errors = [];
    
    if (!data.firstname || data.firstname.trim().length < 2) {
        errors.push('Le prénom doit contenir au moins 2 caractères');
    }
    if (!data.lastname || data.lastname.trim().length < 2) {
        errors.push('Le nom doit contenir au moins 2 caractères');
    }
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!data.email || !emailRegex.test(data.email)) {
        errors.push('Veuillez entrer une adresse email valide');
    }
    if (!data.subject) {
        errors.push('Veuillez sélectionner un sujet');
    }
    if (!data.message || data.message.trim().length < 10) {
        errors.push('Le message doit contenir au moins 10 caractères');
    }
    
    if (errors.length > 0) {
        showError(errors.join('\n'));
        return false;
    }
    return true;
}

// Animation des éléments de contact
function initContactAnimations() {
    const observerOptions = { threshold: 0.1, rootMargin: '0px 0px -50px 0px' };
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    const contactElements = document.querySelectorAll('.info-item, .contact-form-container');
    contactElements.forEach((element, index) => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = `opacity 0.6s ease ${index * 0.1}s, transform 0.6s ease ${index * 0.1}s`;
        observer.observe(element);
    });
}

// Notifications (succès/erreur)
function showSuccess(message) {
    const successDiv = document.createElement('div');
    successDiv.style.cssText = `
        position: fixed; top: 20px; right: 20px; background: #00C851; color: white;
        padding: 1rem 1.5rem; border-radius: 8px; z-index: 10001; max-width: 400px;
        box-shadow: 0 4px 12px rgba(0, 200, 81, 0.3); animation: slideInRight 0.3s ease-out;`;
    successDiv.textContent = message;
    document.body.appendChild(successDiv);
    setTimeout(() => {
        successDiv.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => { successDiv.remove(); }, 300);
    }, 3000);
}
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.style.cssText = `
        position: fixed; top: 20px; right: 20px; background: #ff4444; color: white;
        padding: 1rem 1.5rem; border-radius: 8px; z-index: 10001; max-width: 400px;
        box-shadow: 0 4px 12px rgba(255, 68, 68, 0.3); animation: slideInRight 0.3s ease-out; white-space: pre-line;`;
    errorDiv.textContent = message;
    document.body.appendChild(errorDiv);
    setTimeout(() => {
        errorDiv.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => { errorDiv.remove(); }, 300);
    }, 5000);
}

// Animations CSS pour les notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight { from { opacity: 0; transform: translateX(100%);} to { opacity: 1; transform: translateX(0);} }
    @keyframes slideOutRight { from { opacity: 1; transform: translateX(0);} to { opacity: 0; transform: translateX(100%);} }
`;
document.head.appendChild(style); 