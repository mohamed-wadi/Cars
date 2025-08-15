# 🚀 Guide de Démarrage Rapide - Aymen Car's

## ⚡ **Démarrage en 5 minutes**

### 1. **Lancer le serveur**
```bash
cd backend
python manage.py runserver
```

### 2. **Accéder aux interfaces**

#### 🌐 **Site Principal**
- **URL** : http://127.0.0.1:8000/
- **Fonctionnalités** :
  - Catalogue de 14 voitures
  - Système de réservation
  - Formulaire de contact
  - Navigation responsive

#### 🔐 **Connexion/Inscription**
- **URL** : http://127.0.0.1:8000/login/
- **Compte admin** :
  - Email : admin@aymencars.com
  - Mot de passe : admin123

#### 📊 **Dashboard Admin Frontend**
- **URL** : http://127.0.0.1:8000/dashboard/
- **Identifiants** : admin / admin123
- **Fonctionnalités** :
  - Vue d'ensemble avec statistiques
  - Gestion complète des voitures
  - Gestion des réservations
  - Gestion des agences
  - Gestion des utilisateurs
  - Messages de contact

#### 🔧 **Admin Django**
- **URL** : http://127.0.0.1:8000/admin/
- **Identifiants** : admin / admin123
- **Fonctionnalités** :
  - Interface d'administration complète
  - Gestion avancée de tous les modèles
  - Recherche et filtrage

## 📡 **API Endpoints**

### **Voitures**
- `GET /api/cars/` - Liste des voitures
- `GET /api/cars/search/?q=bmw` - Recherche

### **Agences**
- `GET /api/agencies/` - Liste des agences

### **Services**
- `GET /api/services/` - Liste des services

### **Réservations**
- `GET /api/reservations/` - Réservations utilisateur
- `POST /api/reservations/` - Créer réservation

### **Authentification**
- `POST /api/auth/login/` - Connexion
- `POST /api/auth/register/` - Inscription

## 🎯 **Fonctionnalités Principales**

### ✅ **Système de Réservation**
- Sélection de voiture
- Choix d'agences départ/retour
- Calcul automatique des prix
- Codes promo (WELCOME10 = 10%)
- Validation de l'âge conducteur

### ✅ **Gestion des Rôles**
- **Client** : Peut réserver des voitures
- **Admin** : Accès complet au dashboard

### ✅ **Dashboard Admin**
- Interface moderne avec sidebar
- Statistiques en temps réel
- CRUD complet pour tous les éléments
- Gestion des messages de contact

## 🔧 **Scripts Utiles**

### **Ajouter des données**
```bash
python add_cars.py      # Ajouter des voitures
python add_agencies.py  # Ajouter des agences
```

### **Créer un admin**
```bash
python create_admin.py  # Créer utilisateur admin
```

### **Tester le système**
```bash
python test_system.py   # Test complet
```

## 📊 **Données de Test**

### **Voitures (14)**
- BMW X5, Mercedes Classe C, Audi A4
- Volkswagen Golf, Peugeot 3008, Renault Clio
- Tesla Model 3, Toyota Yaris, Ford Focus
- Citroën C3, et plus...

### **Agences (15)**
- Paris, Lyon, Marseille, Toulouse
- Nice, Bordeaux, Nantes, Strasbourg
- Et plus dans toute la France

### **Services**
- Assurance, GPS, Siège bébé
- Chauffeur, etc.

## 🎨 **Design**

### **Palette de Couleurs**
- **Orange principal** : #FF6600
- **Orange secondaire** : #FFA040
- **Design moderne** et responsive

### **Typographie**
- **Roboto** (Google Fonts)
- **Responsive** pour tous les appareils

## 🚀 **Prêt pour la Production**

Le projet est **100% fonctionnel** avec :
- ✅ Backend Django complet
- ✅ Frontend moderne
- ✅ API REST
- ✅ Système d'authentification
- ✅ Dashboard admin
- ✅ Base de données avec données de test

**Bon développement !** 🚗✨ 