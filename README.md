# 🚗 Aymen Car's - Site de Location de Voitures Complet

Un site web moderne et complet de location de voitures développé avec Django (backend) et HTML/CSS/JavaScript (frontend).

## 🌟 Fonctionnalités Complètes

### 🎯 **Pages et Interface**
- ✅ **Page d'accueil** avec design moderne et responsive
- ✅ **Page de contact** avec formulaire et carte Google Maps
- ✅ **Page de connexion/inscription** avec onglets et validation
- ✅ **Système de navigation** fluide et intuitif
- ✅ **Design responsive** pour tous les appareils

### 🚗 **Gestion des Voitures**
- ✅ **Catalogue dynamique** avec 10 voitures pré-configurées
- ✅ **Images haute qualité** téléchargées automatiquement
- ✅ **Système de filtrage** par marque, prix, disponibilité
- ✅ **Recherche avancée** dans le catalogue

### 📅 **Système de Réservation Complet**
- ✅ **Formulaire de réservation** avec tous les champs nécessaires
- ✅ **Sélection d'agences** de départ et retour
- ✅ **Gestion des dates et heures** de réservation
- ✅ **Calcul automatique des prix** (voiture + services)
- ✅ **Codes promo** (exemple: WELCOME10 = 10% de réduction)
- ✅ **Validation de l'âge** du conducteur
- ✅ **Gestion des services** additionnels

### 🏢 **Gestion des Agences**
- ✅ **8 agences** pré-configurées dans toute la France
- ✅ **API complète** pour récupérer les agences
- ✅ **Sélection dynamique** dans les formulaires

### 👤 **Système d'Authentification**
- ✅ **Connexion/Inscription** avec validation
- ✅ **Gestion des sessions** utilisateur
- ✅ **Protection des routes** privées
- ✅ **Interface d'administration** Django

### 🔧 **Backend Django Avancé**
- ✅ **API REST complète** avec Django REST Framework
- ✅ **Modèles de données** optimisés
- ✅ **Calculs automatiques** de prix
- ✅ **Validation des données** côté serveur
- ✅ **Gestion des réservations** (création, annulation, historique)

### 🎨 **Design et UX**
- ✅ **Couleurs orange** selon le cahier des charges
- ✅ **Animations fluides** et transitions
- ✅ **Notifications** de succès/erreur
- ✅ **Loading states** pour toutes les actions
- ✅ **Interface moderne** et professionnelle

## 🛠️ Technologies Utilisées

### **Backend**
- **Django 5.2.4** - Framework web Python
- **Django REST Framework** - API REST
- **SQLite** - Base de données (développement)
- **Pillow** - Gestion des images

### **Frontend**
- **HTML5** - Structure sémantique
- **CSS3** - Styles modernes avec variables CSS
- **JavaScript ES6+** - Interactions dynamiques
- **Google Fonts** - Typographie Roboto
- **Unsplash** - Images libres de droits

### **Outils**
- **Git** - Versioning
- **Python venv** - Environnement virtuel
- **PowerShell** - Terminal Windows

## 📁 Structure du Projet

```
aymen_cars/
├── backend/                 # Projet Django
│   ├── backend/            # Configuration Django
│   │   ├── settings.py     # Configuration complète
│   │   ├── urls.py         # Routes principales
│   │   └── wsgi.py
│   ├── core/               # Application principale
│   │   ├── models.py       # Modèles: Car, Service, Reservation, Agency
│   │   ├── views.py        # Vues API et pages
│   │   ├── serializers.py  # Serializers DRF
│   │   ├── admin.py        # Admin Django
│   │   └── urls.py         # Routes API
│   ├── manage.py
│   └── db.sqlite3          # Base de données
├── frontend/               # Frontend
│   ├── templates/
│   │   ├── mainPage.html   # Page d'accueil
│   │   ├── contact.html    # Page de contact
│   │   └── login.html      # Page d'authentification
│   └── static/
│       ├── css/
│       │   ├── style.css   # Styles principaux
│       │   ├── contact.css # Styles contact
│       │   └── auth.css    # Styles authentification
│       ├── js/
│       │   ├── main.js     # JavaScript principal
│       │   ├── contact.js  # JavaScript contact
│       │   └── auth.js     # JavaScript authentification
│       └── images/         # Images du site
├── media/                  # Fichiers uploadés
│   └── cars/              # Images des voitures
├── venv/                   # Environnement virtuel Python
├── add_cars.py            # Script d'ajout de voitures
├── add_agencies.py        # Script d'ajout d'agences
└── README.md
```

## 🚀 Installation et Lancement

### **Prérequis**
- Python 3.8+
- pip (gestionnaire de paquets Python)

### **Installation Rapide**

1. **Cloner le projet**
```bash
git clone <url-du-repo>
cd aymen_cars
```

2. **Créer et activer l'environnement virtuel**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Installer les dépendances**
```bash
cd backend
pip install django djangorestframework pillow requests
```

4. **Configurer la base de données**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Créer un superutilisateur**
```bash
python manage.py createsuperuser
```

6. **Ajouter les données de test**
```bash
cd ..
python add_cars.py
python add_agencies.py
```

7. **Lancer le serveur**
```bash
cd backend
python manage.py runserver
```

### **Accès aux Interfaces**

- **🌐 Site principal** : http://127.0.0.1:8000/
- **📞 Page contact** : http://127.0.0.1:8000/contact/
- **🔐 Page connexion** : http://127.0.0.1:8000/login/
- **🔧 Admin Django** : http://127.0.0.1:8000/admin/
- **📡 API Cars** : http://127.0.0.1:8000/api/cars/
- **📡 API Agencies** : http://127.0.0.1:8000/api/agencies/
- **📡 API Services** : http://127.0.0.1:8000/api/services/
- **📡 API Reservations** : http://127.0.0.1:8000/api/reservations/

## 📊 Modèles de Données

### **Car (Voiture)**
- `brand` : Marque du véhicule
- `model` : Modèle du véhicule
- `price_per_day` : Prix par jour
- `image` : Image du véhicule
- `description` : Description détaillée
- `available` : Disponibilité

### **Agency (Agence)**
- `name` : Nom de l'agence
- `address` : Adresse complète
- `city` : Ville
- `country` : Pays
- `phone` : Numéro de téléphone

### **Service**
- `name` : Nom du service
- `description` : Description du service
- `price` : Prix du service

### **Reservation**
- `user` : Utilisateur qui réserve
- `car` : Voiture réservée
- `agency_start` : Agence de départ
- `agency_end` : Agence de retour
- `start_date` : Date de début
- `start_time` : Heure de début
- `end_date` : Date de fin
- `end_time` : Heure de fin
- `services` : Services additionnels
- `promo_code` : Code promo
- `driver_age` : Âge du conducteur
- `total_price` : Prix total calculé
- `status` : Statut de la réservation
- `created_at` : Date de création

## 🎨 Design et Couleurs

### **Palette de couleurs**
- **Orange principal** : #FF6600
- **Orange secondaire** : #FFA040
- **Orange foncé** : #E55A00
- **Orange clair** : #FFE6CC

### **Typographie**
- **Police principale** : Roboto (Google Fonts)
- **Poids** : 300, 400, 500, 700

## 🔧 Configuration

### **Ajouter des voitures**
```bash
python add_cars.py
```

### **Ajouter des agences**
```bash
python add_agencies.py
```

### **Via l'admin Django**
1. Aller sur http://127.0.0.1:8000/admin/
2. Se connecter avec le superutilisateur
3. Gérer voitures, agences, services, réservations

## 📡 API Endpoints

### **Voitures**
- `GET /api/cars/` : Liste des voitures disponibles
- `GET /api/cars/search/?q=bmw&min_price=50&max_price=100` : Recherche filtrée

### **Agences**
- `GET /api/agencies/` : Liste des agences

### **Services**
- `GET /api/services/` : Liste des services

### **Réservations**
- `GET /api/reservations/` : Réservations de l'utilisateur connecté
- `POST /api/reservations/` : Créer une réservation
- `GET /api/reservations/upcoming/` : Réservations à venir
- `GET /api/reservations/past/` : Réservations passées
- `POST /api/reservations/{id}/cancel/` : Annuler une réservation

## 🚀 Fonctionnalités Avancées

### **Système de Réservation**
- Calcul automatique des prix
- Validation des dates
- Gestion des codes promo
- Vérification de l'âge du conducteur
- Sélection d'agences de départ/retour

### **Recherche et Filtrage**
- Recherche par marque/modèle
- Filtrage par prix
- Filtrage par disponibilité
- Tri par différents critères

### **Authentification**
- Connexion/Inscription
- Validation des formulaires
- Gestion des sessions
- Protection des routes

### **Notifications**
- Messages de succès/erreur
- Animations fluides
- Feedback utilisateur

## 📝 TODO / Améliorations Futures

- [ ] **Système de paiement** (Stripe, PayPal)
- [ ] **Notifications email** automatiques
- [ ] **Système de notation** et avis
- [ ] **Application mobile** (React Native)
- [ ] **Mode sombre**
- [ ] **Multilingue** (FR/EN)
- [ ] **Système de fidélité**
- [ ] **Gestion des assurances**
- [ ] **Intégration GPS** pour les agences
- [ ] **Chat en ligne** pour le support

## 🤝 Contribution

1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## 👨‍💻 Auteur

**Aymen Car's** - Projet de location de voitures complet

---

## 🎉 **Projet Terminé !**

Le projet Aymen Car's est maintenant **100% fonctionnel** avec toutes les fonctionnalités demandées :

✅ **Backend Django complet** avec API REST  
✅ **Frontend moderne** avec toutes les pages  
✅ **Système de réservation** avancé  
✅ **Authentification** complète  
✅ **Gestion des agences** et voitures  
✅ **Design responsive** et professionnel  
✅ **Base de données** avec données de test  

**Prêt pour la production !** 🚀 