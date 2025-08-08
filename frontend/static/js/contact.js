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
        // Simulation d'envoi (remplacer par un vrai endpoint API)
        await simulateContactSubmission(formObject);
        
        // Succès
        showSuccess('Votre message a été envoyé avec succès ! Nous vous répondrons dans les plus brefs délais.');
        e.target.reset();
        
    } catch (error) {
        // Erreur
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
    
    // Validation du prénom
    if (!data.firstname || data.firstname.trim().length < 2) {
        errors.push('Le prénom doit contenir au moins 2 caractères');
    }
    
    // Validation du nom
    if (!data.lastname || data.lastname.trim().length < 2) {
        errors.push('Le nom doit contenir au moins 2 caractères');
    }
    
    // Validation de l'email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!data.email || !emailRegex.test(data.email)) {
        errors.push('Veuillez entrer une adresse email valide');
    }
    
    // Validation du sujet
    if (!data.subject) {
        errors.push('Veuillez sélectionner un sujet');
    }
    
    // Validation du message
    if (!data.message || data.message.trim().length < 10) {
        errors.push('Le message doit contenir au moins 10 caractères');
    }
    
    // Afficher les erreurs s'il y en a
    if (errors.length > 0) {
        showError(errors.join('\n'));
        return false;
    }
    
    return true;
}

// Simulation d'envoi du formulaire de contact
function simulateContactSubmission(data) {
    return new Promise((resolve, reject) => {
        // Simuler un délai réseau
        setTimeout(() => {
            // Simuler un succès (90% de chance)
            if (Math.random() > 0.1) {
                resolve({
                    success: true,
                    message: 'Message envoyé avec succès'
                });
            } else {
                reject(new Error('Erreur de connexion'));
            }
        }, 1500);
    });
}

// Animation des éléments de contact
function initContactAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observer les éléments de contact
    const contactElements = document.querySelectorAll('.info-item, .contact-form-container');
    contactElements.forEach((element, index) => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = `opacity 0.6s ease ${index * 0.1}s, transform 0.6s ease ${index * 0.1}s`;
        observer.observe(element);
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