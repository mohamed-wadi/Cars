// Configuration de l'API
const API_BASE_URL = 'http://127.0.0.1:8000/api';

// CSRF helper
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}
const CSRF_TOKEN = getCookie('csrftoken');

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
async function reserveCar(carId) {
    // Vérifier si l'utilisateur est connecté (localStorage + fallback serveur)
    let isLoggedIn = checkIfUserIsLoggedIn();
    if (!isLoggedIn) {
        try {
            const res = await fetch('/api/auth/status/', { credentials: 'same-origin' });
            const data = await res.json();
            if (data && data.authenticated) {
                // Mettre à jour localStorage pour les prochains clics
                localStorage.setItem('isLoggedIn', 'true');
                localStorage.setItem('user', JSON.stringify(data.user));
                isLoggedIn = true;
            }
        } catch {}
    }
    if (!isLoggedIn) {
        window.location.href = '/login/';
        return;
    }
    openReservationModal(carId);
}

// Fonction pour vérifier si l'utilisateur est connecté
function checkIfUserIsLoggedIn() {
    try {
        const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
        const user = JSON.parse(localStorage.getItem('user') || '{}');
        return isLoggedIn && !!user?.id;
    } catch { return false; }
}

// Modal réservation minimal (créé dynamiquement si absent)
function ensureReservationModal() {
    if (document.getElementById('reserve-modal')) return;
    const modal = document.createElement('div');
    modal.id = 'reserve-modal';
    modal.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,.45);display:none;align-items:center;justify-content:center;z-index:1000;';
    modal.innerHTML = `
      <div style="width:95%;max-width:720px;background:#fff;border-radius:10px;box-shadow:0 10px 30px rgba(0,0,0,.2);overflow:hidden;">
        <div style="padding:1rem 1.25rem;border-bottom:1px solid #eee;display:flex;justify-content:space-between;align-items:center;">
          <h4 style="margin:0;color:#2c3e50">Réserver la voiture</h4>
          <button id="reserve-close" style="background:none;border:none;font-size:1.3rem;cursor:pointer;">×</button>
        </div>
        <form id="reserve-form" style="padding:1.25rem;">
          <input type="hidden" id="reserve-car-id" />
          <div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem;">
            <div>
              <label>Agence départ</label>
              <select id="reserve-agency-start" required></select>
            </div>
            <div>
              <label>Agence retour</label>
              <select id="reserve-agency-end" required></select>
            </div>
            <div>
              <label>Date départ</label>
              <input id="reserve-start-date" type="date" required />
            </div>
            <div>
              <label>Heure départ</label>
              <input id="reserve-start-time" type="time" required />
            </div>
            <div>
              <label>Date retour</label>
              <input id="reserve-end-date" type="date" required />
            </div>
            <div>
              <label>Heure retour</label>
              <input id="reserve-end-time" type="time" required />
            </div>
            <div>
              <label>Âge conducteur</label>
              <input id="reserve-age" type="number" min="18" max="99" required />
            </div>
            <div>
              <label>Code promo</label>
              <input id="reserve-promo" type="text" placeholder="(optionnel)" />
            </div>
          </div>
          <div style="display:flex;gap:.5rem;justify-content:flex-end;margin-top:1rem;">
            <button type="button" id="reserve-cancel" style="padding:.5rem .8rem">Annuler</button>
            <button type="submit" style="padding:.5rem .8rem;background:#FF6600;color:#fff;border:none;border-radius:6px;cursor:pointer;">Confirmer</button>
          </div>
          <div id="reserve-notice" style="margin-top:.5rem;font-size:.9rem;color:#2e7d32;display:none;"></div>
        </form>
      </div>`;
    document.body.appendChild(modal);
    document.getElementById('reserve-close').onclick = () => (modal.style.display = 'none');
    document.getElementById('reserve-cancel').onclick = () => (modal.style.display = 'none');
    document.getElementById('reserve-form').onsubmit = submitReservation;
}

async function openReservationModal(carId) {
    ensureReservationModal();
    document.getElementById('reserve-car-id').value = carId;
    // Précharger les agences
    try {
        const res = await fetch(`${API_BASE_URL}/agencies/`);
        const agencies = await res.json();
        const opts = ['<option value="">Sélectionner</option>'].concat(agencies.map(a => `<option value="${a.id}">${a.name} - ${a.city}</option>`));
        document.getElementById('reserve-agency-start').innerHTML = opts.join('');
        document.getElementById('reserve-agency-end').innerHTML = opts.join('');
    } catch {}
    document.getElementById('reserve-notice').style.display = 'none';
    document.getElementById('reserve-modal').style.display = 'flex';
}

async function submitReservation(e) {
    e.preventDefault();
    const car_id = parseInt(document.getElementById('reserve-car-id').value, 10);
    const agency_start_id = parseInt(document.getElementById('reserve-agency-start').value, 10);
    const agency_end_id = parseInt(document.getElementById('reserve-agency-end').value, 10);
    const start_date = document.getElementById('reserve-start-date').value;
    const start_time = document.getElementById('reserve-start-time').value;
    const end_date = document.getElementById('reserve-end-date').value;
    const end_time = document.getElementById('reserve-end-time').value;
    const promo_code = document.getElementById('reserve-promo').value || '';
    const driver_age = parseInt(document.getElementById('reserve-age').value || '18', 10);

    const payload = {
        car_id,
        agency_start_id,
        agency_end_id,
        start_date,
        start_time,
        end_date,
        end_time,
        driver_age,
        promo_code
    };
    const res = await fetch(`${API_BASE_URL}/reservations/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN || '' },
        credentials: 'same-origin',
        body: JSON.stringify(payload)
    });
    const notice = document.getElementById('reserve-notice');
    if (res.ok) {
        notice.textContent = 'Réservation créée avec succès !';
        notice.style.display = 'block';
        // Fermer après un court délai
        setTimeout(() => { document.getElementById('reserve-modal').style.display = 'none'; }, 800);
    } else {
        notice.textContent = 'Erreur lors de la création de la réservation';
        notice.style.color = '#c62828';
        notice.style.display = 'block';
    }
}

// Fonction pour charger les services depuis l'API
async function loadServices() {
    try {
        const response = await fetch(`${API_BASE_URL}/services/`);
        if (response.ok) {
            const services = await response.json();
            // Services disponibles chargés
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
    // Charger les données
    loadCarsWithFiltering();
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
            window.location.href = '/login/';
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

// Advanced filtering functionality
let allCars = [];
let allBrands = [];

// Load all cars and extract brands
async function loadCarsWithFiltering() {
    const carsContainer = document.getElementById('cars-container');
    carsContainer.innerHTML = '<div class="loading">Chargement des voitures...</div>';
    
    try {
        const response = await fetch(`${API_BASE_URL}/cars/`);
        if (!response.ok) throw new Error('Erreur lors du chargement des voitures');
        
        allCars = await response.json();
        
        // Extract unique brands for filter
        allBrands = [...new Set(allCars.map(car => car.brand))].sort();
        populateBrandFilter();
        
        displayCars(allCars);
        
    } catch (error) {
        console.error('Erreur:', error);
        carsContainer.innerHTML = `
            <div style="text-align: center; padding: 2rem; color: #666;">
                <h3>Erreur de chargement</h3>
                <p>Impossible de charger les voitures. Veuillez réessayer plus tard.</p>
                <button onclick="loadCarsWithFiltering()" style="margin-top: 1rem; padding: 0.5rem 1rem; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer;">
                    Réessayer
                </button>
            </div>
        `;
    }
}

// Populate brand filter dropdown
function populateBrandFilter() {
    const brandFilter = document.getElementById('brand-filter');
    if (brandFilter) {
        brandFilter.innerHTML = '<option value="">Toutes les marques</option>' +
            allBrands.map(brand => `<option value="${brand}">${brand}</option>`).join('');
    }
}

// Apply advanced filters
function applyAdvancedFilters() {
    const searchQuery = document.getElementById('search-query')?.value.toLowerCase() || '';
    const brandFilter = document.getElementById('brand-filter')?.value || '';
    const fuelFilter = document.getElementById('fuel-filter')?.value || '';
    const transmissionFilter = document.getElementById('transmission-filter')?.value || '';
    const minPrice = parseFloat(document.getElementById('min-price')?.value) || 0;
    const maxPrice = parseFloat(document.getElementById('max-price')?.value) || Infinity;
    const seatsFilter = document.getElementById('seats-filter')?.value || '';
    const sortBy = document.getElementById('sort-by')?.value || 'price_asc';
    
    let filteredCars = allCars.filter(car => {
        // Search query filter
        if (searchQuery && !car.brand.toLowerCase().includes(searchQuery) &&
            !car.model.toLowerCase().includes(searchQuery) &&
            !car.description.toLowerCase().includes(searchQuery)) {
            return false;
        }
        
        // Brand filter
        if (brandFilter && car.brand !== brandFilter) {
            return false;
        }
        
        // Fuel type filter
        if (fuelFilter && car.fuel_type !== fuelFilter) {
            return false;
        }
        
        // Transmission filter
        if (transmissionFilter && car.transmission !== transmissionFilter) {
            return false;
        }
        
        // Price range filter
        if (car.price_per_day < minPrice || car.price_per_day > maxPrice) {
            return false;
        }
        
        // Seats filter
        if (seatsFilter && car.seats !== parseInt(seatsFilter)) {
            return false;
        }
        
        return true;
    });
    
    // Sort filtered cars
    filteredCars = sortCars(filteredCars, sortBy);
    
    displayCars(filteredCars);
}

// Sort cars based on criteria
function sortCars(cars, sortBy) {
    switch (sortBy) {
        case 'price_asc':
            return cars.sort((a, b) => a.price_per_day - b.price_per_day);
        case 'price_desc':
            return cars.sort((a, b) => b.price_per_day - a.price_per_day);
        case 'brand':
            return cars.sort((a, b) => a.brand.localeCompare(b.brand));
        case 'year_desc':
            return cars.sort((a, b) => b.year - a.year);
        case 'rating':
            // For now, sort by brand as we don't have ratings calculated yet
            return cars.sort((a, b) => a.brand.localeCompare(b.brand));
        default:
            return cars;
    }
}

// Clear all filters
function clearFilters() {
    document.getElementById('search-query').value = '';
    document.getElementById('brand-filter').value = '';
    document.getElementById('fuel-filter').value = '';
    document.getElementById('transmission-filter').value = '';
    document.getElementById('min-price').value = '';
    document.getElementById('max-price').value = '';
    document.getElementById('seats-filter').value = '';
    document.getElementById('sort-by').value = 'price_asc';
    
    displayCars(allCars);
}

// Display cars with enhanced information
function displayCars(cars) {
    const carsContainer = document.getElementById('cars-container');
    
    if (cars.length === 0) {
        carsContainer.innerHTML = `
            <div style="text-align: center; padding: 3rem; color: #666;">
                <h3>Aucune voiture trouvée</h3>
                <p>Essayez de modifier vos critères de recherche</p>
                <button onclick="clearFilters()" class="btn-primary">Effacer les filtres</button>
            </div>
        `;
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
                <div class="car-specs" style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; margin: 0.5rem 0; font-size: 0.9rem; color: #666;">
                    <div>⛽ ${getFuelTypeDisplay(car.fuel_type)}</div>
                    <div>⚙️ ${getTransmissionDisplay(car.transmission)}</div>
                    <div>👥 ${car.seats} places</div>
                    <div>📅 ${car.year}</div>
                </div>
                <p class="car-description">${car.description || 'Véhicule de qualité disponible à la location.'}</p>
                <div style="display: flex; gap: 0.5rem; margin-top: 1rem;">
                    <button class="btn-reserve" onclick="reserveCar(${car.id})" style="flex: 1;">
                        Réserver
                    </button>
                    <button onclick="viewCarDetails(${car.id})" style="padding: 0.5rem; background: #6c757d; color: white; border: none; border-radius: 5px; cursor: pointer;">
                        Détails
                    </button>
                </div>
            </div>
        </div>
    `).join('');
    
    carsContainer.innerHTML = carsHTML;
    
    // Re-initialize animations for new cards
    setTimeout(initScrollAnimations, 100);
}

// Helper functions for display
function getFuelTypeDisplay(fuelType) {
    const fuelTypes = {
        'essence': 'Essence',
        'diesel': 'Diesel',
        'hybrid': 'Hybride',
        'electric': 'Électrique'
    };
    return fuelTypes[fuelType] || fuelType;
}

function getTransmissionDisplay(transmission) {
    const transmissions = {
        'manual': 'Manuelle',
        'automatic': 'Automatique'
    };
    return transmissions[transmission] || transmission;
}

// View car details function
function viewCarDetails(carId) {
    const car = allCars.find(c => c.id === carId);
    if (!car) return;
    
    alert(`Détails du véhicule:
    
${car.brand} ${car.model} (${car.year})
Prix: ${car.price_per_day}€/jour
Carburant: ${getFuelTypeDisplay(car.fuel_type)}
Transmission: ${getTransmissionDisplay(car.transmission)}
Places: ${car.seats}
Kilométrage: ${car.mileage} km

${car.description}`);
}

// Function for basic filtering (existing functionality)
async function loadCarsFiltered(filters) {
    // For now, just apply advanced filters
    applyAdvancedFilters();
}