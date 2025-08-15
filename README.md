# 🚗 Aymen Car's - Site de Location de Voitures Complet

Un site web moderne et complet de location de voitures développé avec Django (backend) et HTML/CSS/JavaScript (frontend).

## 🌟 Fonctionnalités Complètes

### 🎯 **Pages et Interface**
- ✅ **Page d'accueil** avec design moderne et responsive
- ✅ **Page de contact** avec formulaire et carte Google Maps
- ✅ **Page de connexion/inscription** complète avec validation
- ✅ **Page de profil utilisateur** avec gestion des réservations
- ✅ **Dashboard admin frontend** complet avec tous les CRUD
- ✅ **Système de navigation** fluide et intuitif
- ✅ **Design responsive** pour tous les appareils

### 🚗 **Gestion des Voitures**
- ✅ **Catalogue dynamique** avec 14 voitures pré-configurées
- ✅ **Images haute qualité** téléchargées automatiquement
- ✅ **Système de filtrage** par marque, prix, disponibilité
- ✅ **Recherche avancée** dans le catalogue
- ✅ **Informations détaillées** : année, kilométrage, carburant, transmission

### 📅 **Système de Réservation Complet**
- ✅ **Formulaire de réservation** avec tous les champs nécessaires
- ✅ **Sélection d'agences** de départ et retour
- ✅ **Gestion des dates et heures** de réservation
- ✅ **Calcul automatique des prix** (voiture + services)
- ✅ **Codes promo** (exemple: WELCOME10 = 10% de réduction)
- ✅ **Validation de l'âge** du conducteur
- ✅ **Gestion des services** additionnels
- ✅ **Statuts de réservation** (en attente, confirmée, annulée, terminée)

### 🏢 **Gestion des Agences**
- ✅ **15 agences** pré-configurées dans toute la France
- ✅ **API complète** pour récupérer les agences
- ✅ **Sélection dynamique** dans les formulaires
- ✅ **Informations complètes** : adresse, téléphone, email, horaires

### 👤 **Système d'Authentification Avancé**
- ✅ **Rôles utilisateur** : Client et Administrateur
- ✅ **Inscription clients** uniquement (admins via Django)
- ✅ **Connexion sécurisée** avec validation
- ✅ **Gestion des sessions** utilisateur
- ✅ **Protection des routes** privées
- ✅ **Profils utilisateur** avec informations détaillées

### 🔧 **Dashboard Admin Frontend Complet**
- ✅ **Interface moderne** avec sidebar et navigation
- ✅ **Vue d'ensemble** avec statistiques en temps réel
- ✅ **Gestion des voitures** (CRUD complet)
- ✅ **Gestion des réservations** (voir, modifier, annuler)
- ✅ **Gestion des agences** (CRUD complet)
- ✅ **Gestion des utilisateurs** (CRUD complet)
- ✅ **Gestion des services** (CRUD complet)
- ✅ **Messages de contact** (gestion complète)
- ✅ **Interface intuitive** avec recherche et filtrage

### 🎨 **Design et UX**
- ✅ **Palette orange** selon le cahier des charges
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
│   │   ├── models.py       # Modèles: Car, Service, Reservation, Agency, UserProfile, Contact
│   │   ├── views.py        # Vues API et pages
│   │   ├── serializers.py  # Serializers DRF
│   │   ├── admin.py        # Admin Django avancé
│   │   └── urls.py         # Routes API
│   ├── manage.py
│   └── db.sqlite3          # Base de données
├── frontend/               # Frontend
│   ├── templates/
│   │   ├── mainPage.html   # Page d'accueil
│   │   ├── contact.html    # Page de contact
│   │   ├── login.html      # Page d'authentification
│   │   ├── profile.html    # Page de profil utilisateur
│   │   └── dashboard.html  # Dashboard admin frontend
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
├── create_admin.py        # Script de création d'admin
├── ADMIN_GUIDE.md         # Guide d'utilisation de l'admin
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
cd ..
python create_admin.py
```

6. **Ajouter les données de test**
```bash
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
- **👤 Page profil** : http://127.0.0.1:8000/profile/
- **📊 Dashboard Admin** : http://127.0.0.1:8000/dashboard/
- **🔧 Admin Django** : http://127.0.0.1:8000/admin/
- **📡 API Cars** : http://127.0.0.1:8000/api/cars/
- **📡 API Agencies** : http://127.0.0.1:8000/api/agencies/
- **📡 API Services** : http://127.0.0.1:8000/api/services/
- **📡 API Reservations** : http://127.0.0.1:8000/api/reservations/
- **📡 API Contacts** : http://127.0.0.1:8000/api/contacts/

## 🔧 **Interface d'Administration**

### **Accès Admin**
- **URL** : http://127.0.0.1:8000/admin/
- **Username** : admin
- **Password** : admin123

### **Dashboard Frontend**
- **URL** : http://127.0.0.1:8000/dashboard/
- **Username** : admin
- **Password** : admin123

### **Fonctionnalités Admin**
- ✅ **Gestion des voitures** (ajouter, modifier, supprimer)
- ✅ **Gestion des agences** (15 agences pré-configurées)
- ✅ **Gestion des services** (assurance, GPS, etc.)
- ✅ **Gestion des réservations** (voir toutes les réservations)
- ✅ **Gestion des utilisateurs** (créer, modifier, supprimer)
- ✅ **Messages de contact** (gestion complète)
- ✅ **Interface intuitive** avec recherche et filtrage

### **Guide d'Utilisation**
Consultez le fichier `ADMIN_GUIDE.md` pour un guide complet d'utilisation de l'admin Django.

## 📊 Modèles de Données

### **UserProfile (Profil Utilisateur)**
- `user` : Relation OneToOne avec User Django
- `role` : Rôle (client/admin)
- `phone` : Numéro de téléphone
- `address` : Adresse complète
- `birth_date` : Date de naissance

### **Car (Voiture)**
- `brand` : Marque du véhicule
- `model` : Modèle du véhicule
- `price_per_day` : Prix par jour
- `image` : Image du véhicule
- `description` : Description détaillée
- `available` : Disponibilité
- `year` : Année du véhicule
- `mileage` : Kilométrage
- `fuel_type` : Type de carburant
- `transmission` : Type de transmission
- `seats` : Nombre de places

### **Agency (Agence)**
- `name` : Nom de l'agence
- `address` : Adresse complète
- `city` : Ville
- `country` : Pays
- `phone` : Numéro de téléphone
- `email` : Adresse email
- `opening_hours` : Horaires d'ouverture

### **Service**
- `name` : Nom du service
- `description` : Description du service
- `price` : Prix du service
- `is_active` : Service actif

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
- `notes` : Notes additionnelles
- `created_at` : Date de création
- `updated_at` : Date de modification

### **Contact**
- `name` : Nom du contact
- `email` : Email du contact
- `phone` : Téléphone
- `subject` : Sujet du message
- `message` : Contenu du message
- `status` : Statut du message
- `admin_response` : Réponse de l'admin
- `created_at` : Date de création
- `updated_at` : Date de modification

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

### **Créer un admin**
```bash
python create_admin.py
```

### **Via l'admin Django**
1. Aller sur http://127.0.0.1:8000/admin/
2. Se connecter avec le superutilisateur
3. Gérer voitures, agences, services, réservations, utilisateurs, contacts

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

### **Authentification**
- `POST /api/auth/login/` : Connexion
- `POST /api/auth/register/` : Inscription
- `POST /api/auth/logout/` : Déconnexion

### **Contact**
- `POST /api/contact/submit/` : Soumettre un message de contact

### **Admin**
- `GET /api/admin/users/` : Liste des utilisateurs (admin)

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

### **Authentification et Rôles**
- Système de rôles (client/admin)
- Inscription clients uniquement
- Admins créés via Django
- Gestion des sessions sécurisée

### **Dashboard Admin Frontend**
- Interface moderne et intuitive
- Gestion complète de tous les éléments
- Statistiques en temps réel
- Actions CRUD complètes

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
✅ **Dashboard admin frontend** complet  
✅ **Système d'authentification** avec rôles  
✅ **Gestion des agences** et voitures  
✅ **Design responsive** et professionnel  
✅ **Base de données** avec données de test  
✅ **Interface d'administration** complète  

**Prêt pour la production !** 🚀 