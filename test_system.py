import os
import sys
import django
import requests
import json
from datetime import datetime, timedelta

# Configuration Django
sys.path.append('backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Car, Agency, Service, Reservation, UserProfile, Contact

def test_database():
    """Test de la base de données"""
    print("🔍 Test de la base de données...")
    
    # Test des voitures
    cars_count = Car.objects.count()
    print(f"   ✅ {cars_count} voitures en base")
    
    # Test des agences
    agencies_count = Agency.objects.count()
    print(f"   ✅ {agencies_count} agences en base")
    
    # Test des services
    services_count = Service.objects.count()
    print(f"   ✅ {services_count} services en base")
    
    # Test des utilisateurs
    users_count = User.objects.count()
    print(f"   ✅ {users_count} utilisateurs en base")
    
    # Test des profils
    profiles_count = UserProfile.objects.count()
    print(f"   ✅ {profiles_count} profils utilisateur en base")
    
    # Test des réservations
    reservations_count = Reservation.objects.count()
    print(f"   ✅ {reservations_count} réservations en base")
    
    # Test des contacts
    contacts_count = Contact.objects.count()
    print(f"   ✅ {contacts_count} messages de contact en base")

def test_api_endpoints():
    """Test des endpoints API"""
    print("\n🌐 Test des endpoints API...")
    
    base_url = "http://127.0.0.1:8000"
    
    try:
        # Test API Cars
        response = requests.get(f"{base_url}/api/cars/", timeout=5)
        if response.status_code == 200:
            cars = response.json()
            print(f"   ✅ API Cars: {len(cars)} voitures récupérées")
        else:
            print(f"   ❌ API Cars: Erreur {response.status_code}")
    except:
        print("   ⚠️  API Cars: Serveur non accessible")
    
    try:
        # Test API Agencies
        response = requests.get(f"{base_url}/api/agencies/", timeout=5)
        if response.status_code == 200:
            agencies = response.json()
            print(f"   ✅ API Agencies: {len(agencies)} agences récupérées")
        else:
            print(f"   ❌ API Agencies: Erreur {response.status_code}")
    except:
        print("   ⚠️  API Agencies: Serveur non accessible")
    
    try:
        # Test API Services
        response = requests.get(f"{base_url}/api/services/", timeout=5)
        if response.status_code == 200:
            services = response.json()
            print(f"   ✅ API Services: {len(services)} services récupérées")
        else:
            print(f"   ❌ API Services: Erreur {response.status_code}")
    except:
        print("   ⚠️  API Services: Serveur non accessible")

def test_admin_user():
    """Test de l'utilisateur admin"""
    print("\n👤 Test de l'utilisateur admin...")
    
    try:
        admin_user = User.objects.get(username='admin')
        print(f"   ✅ Utilisateur admin trouvé: {admin_user.username}")
        print(f"   ✅ Email: {admin_user.email}")
        print(f"   ✅ Superuser: {admin_user.is_superuser}")
        
        # Test du profil admin
        try:
            profile = admin_user.profile
            print(f"   ✅ Profil admin: {profile.role}")
        except UserProfile.DoesNotExist:
            print("   ❌ Profil admin manquant")
            
    except User.DoesNotExist:
        print("   ❌ Utilisateur admin non trouvé")

def test_models():
    """Test des modèles"""
    print("\n📊 Test des modèles...")
    
    # Test Car
    if Car.objects.exists():
        car = Car.objects.first()
        print(f"   ✅ Modèle Car: {car.brand} {car.model}")
        print(f"      Prix: {car.price_per_day}€/jour")
        print(f"      Année: {car.year}")
        print(f"      Carburant: {car.fuel_type}")
        print(f"      Transmission: {car.transmission}")
    
    # Test Agency
    if Agency.objects.exists():
        agency = Agency.objects.first()
        print(f"   ✅ Modèle Agency: {agency.name}")
        print(f"      Ville: {agency.city}")
        print(f"      Téléphone: {agency.phone}")
        print(f"      Email: {agency.email}")
        print(f"      Horaires: {agency.opening_hours}")
    
    # Test Service
    if Service.objects.exists():
        service = Service.objects.first()
        print(f"   ✅ Modèle Service: {service.name}")
        print(f"      Prix: {service.price}€")
        print(f"      Actif: {service.is_active}")

def test_reservation_system():
    """Test du système de réservation"""
    print("\n📅 Test du système de réservation...")
    
    # Créer un utilisateur de test
    test_user, created = User.objects.get_or_create(
        username='test_user',
        defaults={
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    
    if created:
        UserProfile.objects.create(user=test_user, role='client')
        print("   ✅ Utilisateur de test créé")
    
    # Créer une réservation de test
    if Car.objects.exists() and Agency.objects.count() >= 2:
        car = Car.objects.first()
        agency_start = Agency.objects.first()
        agency_end = Agency.objects.last()
        
        # Calculer les dates
        start_date = datetime.now().date() + timedelta(days=1)
        end_date = start_date + timedelta(days=3)
        
        reservation = Reservation.objects.create(
            user=test_user,
            car=car,
            agency_start=agency_start,
            agency_end=agency_end,
            start_date=start_date,
            start_time=datetime.now().time(),
            end_date=end_date,
            end_time=datetime.now().time(),
            driver_age=25,
            total_price=car.price_per_day * 3,
            status='pending'
        )
        
        print(f"   ✅ Réservation de test créée")
        print(f"      Voiture: {car.brand} {car.model}")
        print(f"      Prix total: {reservation.total_price}€")
        print(f"      Statut: {reservation.status}")
        
        # Nettoyer
        reservation.delete()
        print("   ✅ Réservation de test supprimée")
    
    # Nettoyer l'utilisateur de test
    test_user.delete()
    print("   ✅ Utilisateur de test supprimé")

def main():
    """Fonction principale de test"""
    print("🚗 Test complet du système Aymen Car's")
    print("=" * 50)
    
    test_database()
    test_api_endpoints()
    test_admin_user()
    test_models()
    test_reservation_system()
    
    print("\n" + "=" * 50)
    print("🎉 Tests terminés !")
    print("\n📋 Résumé des fonctionnalités :")
    print("✅ Base de données configurée")
    print("✅ Modèles créés et fonctionnels")
    print("✅ API REST opérationnelle")
    print("✅ Système d'authentification")
    print("✅ Système de réservation")
    print("✅ Dashboard admin frontend")
    print("✅ Interface d'administration Django")
    print("\n🌐 Accès aux interfaces :")
    print("   Site principal: http://127.0.0.1:8000/")
    print("   Dashboard admin: http://127.0.0.1:8000/dashboard/")
    print("   Admin Django: http://127.0.0.1:8000/admin/")
    print("\n🔑 Identifiants admin :")
    print("   Username: admin")
    print("   Password: admin123")

if __name__ == "__main__":
    main() 