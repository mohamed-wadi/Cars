// Configuration de l'API
const API_BASE_URL = 'http://127.0.0.1:8000/api';

// Fonction pour faire défiler vers le catalogue
function scrollToCatalogue() {
    document.getElementById('catalogue').scrollIntoView({ 
        behavior: 'smooth' 
    });
}

// Fonction pour charger les voitures depuis l'API
async function loadCars() {
    const carsContainer = document.getElementById('cars-container');
    
    // Afficher un indicateur de chargement
    carsContainer.innerHTML = '<div class="loading">Chargement des voitures...</div>';
    
    try {
        const response = await fetch(`${API_BASE_URL}/cars/`);
        if (!response.ok) {
            throw new Error('Erreur lors du chargement des voitures');
        }
        
        const cars = await response.json();
        
        if (cars.length === 0) {
            carsContainer.innerHTML = `
                <div style="text-align: center; padding: 2rem; color: #666;">
                    <h3>Aucune voiture disponible pour le moment</h3>
                    <p>Revenez plus tard pour découvrir notre flotte</p>
                </div>
            `;
            return;
        }
        
        // Générer les cartes de voitures
        const carsHTML = cars.map(car => `
            <div class="car-card">
                <div class="car-image">
                    ${car.image ? `<img src="${car.image}" alt="${car.brand} ${car.model}" style="width: 100%; height: 100%; object-fit: cover;">` : '🚗'}
                </div>
                <div class="car-info">
                    <h3 class="car-title">${car.brand} ${car.model}</h3>
                    <div class="car-price">${car.price_per_day}€ / jour</div>
                    <p class="car-description">${car.description || 'Véhicule de qualité disponible à la location.'}</p>
                    <button class="btn-reserve" onclick="reserveCar(${car.id})">
                        Réserver cette voiture
                    </button>
                </div>
            </div>
        `).join('');
        
        carsContainer.innerHTML = carsHTML;
        
    } catch (error) {
        console.error('Erreur:', error);
        carsContainer.innerHTML = `
            <div style="text-align: center; padding: 2rem; color: #666;">
                <h3>Erreur de chargement</h3>
                <p>Impossible de charger les voitures. Veuillez réessayer plus tard.</p>
                <button onclick="loadCars()" style="margin-top: 1rem; padding: 0.5rem 1rem; background: #FF6600; color: white; border: none; border-radius: 5px; cursor: pointer;">
                    Réessayer
                </button>
            </div>
        `;
    }
}

// Fonction pour réserver une voiture
function reserveCar(carId) {
    // Vérifier si l'utilisateur est connecté
    const isLoggedIn = checkIfUserIsLoggedIn();
    
    if (!isLoggedIn) {
        alert('Veuillez vous connecter pour réserver une voiture.');
        // Ici on pourrait rediriger vers la page de connexion
        return;
    }
    
    // Ouvrir un modal de réservation ou rediriger vers la page de réservation
    openReservationModal(carId);
}

// Fonction pour vérifier si l'utilisateur est connecté
function checkIfUserIsLoggedIn() {
    // Pour l'instant, on retourne false
    // Plus tard, on pourra vérifier les tokens d'authentification
    return false;
}

// Fonction pour ouvrir le modal de réservation
function openReservationModal(carId) {
    // Créer un modal simple pour la réservation
    const modal = document.createElement('div');
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
    `;
    
    modal.innerHTML = `
        <div style="
            background: white;
            padding: 2rem;
            border-radius: 15px;
            max-width: 500px;
            width: 90%;
            text-align: center;
        ">
            <h3 style="color: #FF6600; margin-bottom: 1rem;">Réservation</h3>
            <p style="margin-bottom: 1rem;">Fonctionnalité de réservation en cours de développement.</p>
            <p style="margin-bottom: 2rem;">Pour l'instant, veuillez utiliser l'interface d'administration Django.</p>
            <button onclick="this.parentElement.parentElement.remove()" style="
                background: #FF6600;
                color: white;
                border: none;
                padding: 0.8rem 1.5rem;
                border-radius: 25px;
                cursor: pointer;
                font-weight: 500;
            ">
                Fermer
            </button>
        </div>
    `;
    
    document.body.appendChild(modal);
}

// Fonction pour charger les services depuis l'API
async function loadServices() {
    try {
        const response = await fetch(`${API_BASE_URL}/services/`);
        if (response.ok) {
            const services = await response.json();
            console.log('Services disponibles:', services);
        }
    } catch (error) {
        console.error('Erreur lors du chargement des services:', error);
    }
}

// Fonction pour charger les agences depuis l'API
async function loadAgencies() {
    const agencyStart = document.getElementById('agency-start');
    const agencyEnd = document.getElementById('agency-end');
    try {
        const response = await fetch(`${API_BASE_URL}/agencies/`);
        if (!response.ok) throw new Error('Erreur lors du chargement des agences');
        const agencies = await response.json();
        agencyStart.innerHTML = '<option value="">Sélectionner</option>' + agencies.map(a => `<option value="${a.id}">${a.name} - ${a.city}</option>`).join('');
        agencyEnd.innerHTML = '<option value="">Sélectionner</option>' + agencies.map(a => `<option value="${a.id}">${a.name} - ${a.city}</option>`).join('');
    } catch (e) {
        agencyStart.innerHTML = '<option value="">Erreur</option>';
        agencyEnd.innerHTML = '<option value="">Erreur</option>';
    }
}

// Fonction pour gérer la navigation smooth
function initSmoothScrolling() {
    const navLinks = document.querySelectorAll('nav a[href^="#"]');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                targetSection.scrollIntoView({ 
                    behavior: 'smooth' 
                });
            }
        });
    });
}

// Fonction pour animer les éléments au scroll
function initScrollAnimations() {
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
    
    // Observer les cartes de services et de voitures
    const cards = document.querySelectorAll('.service-card, .car-card');
    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });
}

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    console.log('Aymen Car\'s - Site de location de voitures');
    
    // Charger les données
    loadCars();
    loadServices();
    loadAgencies();
    
    // Initialiser les interactions
    initSmoothScrolling();
    
    // Initialiser les animations après un délai
    setTimeout(initScrollAnimations, 500);
    
    // Gestionnaire pour le bouton de connexion
    const loginBtn = document.querySelector('.btn-login');
    if (loginBtn) {
        loginBtn.addEventListener('click', function() {
            alert('Page de connexion en cours de développement. Utilisez l\'admin Django pour l\'instant.');
        });
    }

    const filterForm = document.getElementById('filter-form');
    if (filterForm) {
        filterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            // Récupérer les valeurs du formulaire
            const agencyStart = document.getElementById('agency-start').value;
            const agencyEnd = document.getElementById('agency-end').value;
            const dateStart = document.getElementById('date-start').value;
            const timeStart = document.getElementById('time-start').value;
            const dateEnd = document.getElementById('date-end').value;
            const timeEnd = document.getElementById('time-end').value;
            const promoCode = document.getElementById('promo-code').value;
            const age = document.getElementById('age').value;

            // Pour l'instant, on filtre juste les voitures par agence de départ (exemple)
            // Plus tard, on pourra appeler un endpoint filtré côté backend
            loadCarsFiltered({ agencyStart, agencyEnd, dateStart, timeStart, dateEnd, timeEnd, promoCode, age });
        });
    }
});

// Fonction utilitaire pour formater les prix
function formatPrice(price) {
    return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'EUR'
    }).format(price);
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
        padding: 1rem;
        border-radius: 5px;
        z-index: 10001;
        max-width: 300px;
    `;
    errorDiv.textContent = message;
    
    document.body.appendChild(errorDiv);
    
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
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
        padding: 1rem;
        border-radius: 5px;
        z-index: 10001;
        max-width: 300px;
    `;
    successDiv.textContent = message;
    
    document.body.appendChild(successDiv);
    
    setTimeout(() => {
        successDiv.remove();
    }, 5000);
} 

// Fonction de filtrage (exemple, à améliorer côté backend)
async function loadCarsFiltered(filters) {
    const carsContainer = document.getElementById('cars-container');
    carsContainer.innerHTML = '<div class="loading">Filtrage en cours...</div>';
    try {
        const response = await fetch(`${API_BASE_URL}/cars/`);
        if (!response.ok) throw new Error('Erreur lors du chargement des voitures');
        let cars = await response.json();
        // Exemple de filtrage côté client (par agence de départ, à remplacer par un vrai filtrage backend)
        if (filters.agencyStart) {
            cars = cars.filter(car => car.agency_start === parseInt(filters.agencyStart));
        }
        // Affichage (identique à loadCars)
        if (cars.length === 0) {
            carsContainer.innerHTML = `<div style="text-align: center; padding: 2rem; color: #666;"><h3>Aucune voiture trouvée</h3></div>`;
            return;
        }
        const carsHTML = cars.map(car => `
            <div class="car-card">
                <div class="car-image">
                    ${car.image ? `<img src="${car.image}" alt="${car.brand} ${car.model}" style="width: 100%; height: 100%; object-fit: cover;">` : '🚗'}
                </div>
                <div class="car-info">
                    <h3 class="car-title">${car.brand} ${car.model}</h3>
                    <div class="car-price">${car.price_per_day}€ / jour</div>
                    <p class="car-description">${car.description || 'Véhicule de qualité disponible à la location.'}</p>
                    <button class="btn-reserve" onclick="reserveCar(${car.id})">Réserver cette voiture</button>
                </div>
            </div>
        `).join('');
        carsContainer.innerHTML = carsHTML;
    } catch (e) {
        carsContainer.innerHTML = `<div style="text-align: center; padding: 2rem; color: #666;">Erreur de filtrage</div>`;
    }
} 