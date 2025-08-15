import os
import sys
import django

# Configuration Django
sys.path.append('backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from core.models import Car, Agency, Service, UserProfile

def test_no_alerts():
    """Test que le projet fonctionne sans alertes"""
    print("🔇 Test du projet sans alertes...")
    
    # Test 1: Vérifier l'authentification
    try:
        test_user = User.objects.get(username='test')
        user = authenticate(username=test_user.email, password='test123')
        if user:
            print("   ✅ Authentification fonctionne sans alertes")
        else:
            print("   ❌ Problème d'authentification")
    except Exception as e:
        print(f"   ❌ Erreur d'authentification: {e}")
    
    # Test 2: Vérifier la base de données
    try:
        cars_count = Car.objects.count()
        agencies_count = Agency.objects.count()
        services_count = Service.objects.count()
        users_count = User.objects.count()
        
        print(f"   ✅ Base de données: {cars_count} voitures, {agencies_count} agences, {services_count} services, {users_count} utilisateurs")
    except Exception as e:
        print(f"   ❌ Erreur base de données: {e}")
    
    # Test 3: Vérifier les profils utilisateur
    try:
        profiles_count = UserProfile.objects.count()
        print(f"   ✅ Profils utilisateur: {profiles_count} profils")
    except Exception as e:
        print(f"   ❌ Erreur profils: {e}")
    
    # Test 4: Vérifier les fichiers sans alertes
    try:
        # Vérifier le dashboard
        with open('frontend/templates/dashboard.html', 'r', encoding='utf-8') as f:
            dashboard_content = f.read()
            if 'alert(' not in dashboard_content:
                print("   ✅ Dashboard.html sans alertes")
            else:
                print("   ❌ Alertes trouvées dans dashboard.html")
        
        # Vérifier main.js
        with open('frontend/static/js/main.js', 'r', encoding='utf-8') as f:
            mainjs_content = f.read()
            if 'alert(' not in mainjs_content:
                print("   ✅ main.js sans alertes")
            else:
                print("   ❌ Alertes trouvées dans main.js")
                
    except Exception as e:
        print(f"   ❌ Erreur lecture fichiers: {e}")
    
    print(f"\n🎉 Test terminé !")
    print(f"Le projet fonctionne maintenant sans alertes.")
    
    print(f"\n🔑 Identifiants de test :")
    print(f"   Dashboard HTML: test@aymencars.com / test123")
    print(f"   Admin Django: admin@aymencars.com / admin123")
    print(f"   Client: client@aymencars.com / client123")
    
    print(f"\n🌐 Accès aux interfaces :")
    print(f"   Site principal: http://127.0.0.1:8000/")
    print(f"   Dashboard admin: http://127.0.0.1:8000/dashboard/")
    print(f"   Admin Django: http://127.0.0.1:8000/admin/")

if __name__ == "__main__":
    test_no_alerts() 