# 🔧 Guide d'Utilisation de l'Admin Django - Aymen Car's

## 🌐 **Accès à l'Admin**

**URL :** http://127.0.0.1:8000/admin/

**Identifiants :**
- **Username :** admin
- **Password :** admin123

## 📊 **Gestion des Données**

### **1. Gestion des Voitures**
- **Accès :** Admin → Cars
- **Actions disponibles :**
  - ✅ Voir toutes les voitures
  - ✅ Ajouter une nouvelle voiture
  - ✅ Modifier une voiture existante
  - ✅ Supprimer une voiture
  - ✅ Upload d'images

**Champs à remplir :**
- **Brand** : Marque (ex: BMW, Mercedes, Audi)
- **Model** : Modèle (ex: X5, Classe C 200, A4)
- **Price per day** : Prix par jour (ex: 120.00)
- **Image** : Photo de la voiture
- **Description** : Description détaillée
- **Available** : Disponibilité (cocher si disponible)

### **2. Gestion des Agences**
- **Accès :** Admin → Agencies
- **Actions disponibles :**
  - ✅ Voir toutes les agences
  - ✅ Ajouter une nouvelle agence
  - ✅ Modifier une agence existante
  - ✅ Supprimer une agence

**Champs à remplir :**
- **Name** : Nom de l'agence (ex: Aymen Car's - Paris Centre)
- **Address** : Adresse complète
- **City** : Ville
- **Country** : Pays (par défaut: France)
- **Phone** : Numéro de téléphone

### **3. Gestion des Services**
- **Accès :** Admin → Services
- **Actions disponibles :**
  - ✅ Voir tous les services
  - ✅ Ajouter un nouveau service
  - ✅ Modifier un service existant
  - ✅ Supprimer un service

**Champs à remplir :**
- **Name** : Nom du service (ex: Assurance complète, GPS)
- **Description** : Description du service
- **Price** : Prix du service

### **4. Gestion des Réservations**
- **Accès :** Admin → Reservations
- **Actions disponibles :**
  - ✅ Voir toutes les réservations
  - ✅ Modifier une réservation
  - ✅ Supprimer une réservation
  - ✅ Voir les détails complets

**Informations affichées :**
- **User** : Utilisateur qui a fait la réservation
- **Car** : Voiture réservée
- **Agency start/end** : Agences de départ/retour
- **Start/End date** : Dates de début/fin
- **Total price** : Prix total calculé
- **Status** : Statut de la réservation
- **Created at** : Date de création

## 🚀 **Fonctionnalités Avancées**

### **Recherche et Filtrage**
- Utilisez la barre de recherche pour trouver rapidement des éléments
- Filtrez par différents critères (disponibilité, prix, etc.)

### **Actions en Lot**
- Sélectionnez plusieurs éléments pour les modifier en lot
- Supprimez plusieurs éléments simultanément

### **Export/Import**
- Exportez les données en CSV
- Importez des données depuis des fichiers

## 📈 **Statistiques Disponibles**

### **Dashboard Principal**
- Nombre total de voitures
- Nombre total d'agences
- Nombre total de réservations
- Nombre total d'utilisateurs

### **Statistiques par Section**
- **Cars** : Voitures disponibles/indisponibles
- **Reservations** : Réservations confirmées/en attente/annulées
- **Agencies** : Répartition géographique des agences

## 🔐 **Sécurité**

### **Gestion des Utilisateurs**
- **Accès :** Admin → Users
- **Actions :**
  - ✅ Créer de nouveaux utilisateurs
  - ✅ Modifier les permissions
  - ✅ Désactiver des comptes
  - ✅ Réinitialiser les mots de passe

### **Permissions**
- **Superuser** : Accès complet à tout
- **Staff** : Accès limité à certaines sections
- **Regular User** : Pas d'accès à l'admin

## 🛠️ **Maintenance**

### **Sauvegarde de la Base de Données**
```bash
python manage.py dumpdata > backup.json
```

### **Restauration de la Base de Données**
```bash
python manage.py loaddata backup.json
```

### **Nettoyage des Données**
- Supprimez les réservations anciennes
- Archivez les voitures non disponibles
- Mettez à jour les prix régulièrement

## 📞 **Support**

En cas de problème avec l'admin Django :
1. Vérifiez que le serveur Django fonctionne
2. Vérifiez vos identifiants de connexion
3. Consultez les logs Django pour les erreurs
4. Contactez l'équipe technique

---

## ✅ **Checklist d'Utilisation**

- [ ] Se connecter à l'admin Django
- [ ] Vérifier les voitures disponibles
- [ ] Vérifier les agences configurées
- [ ] Vérifier les services disponibles
- [ ] Consulter les réservations existantes
- [ ] Ajouter/modifier des données si nécessaire
- [ ] Sauvegarder les modifications importantes

**L'admin Django est maintenant votre interface principale pour gérer le site Aymen Car's !** 🚗✨ 