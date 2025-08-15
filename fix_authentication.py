import os
import sys
import django

# Configuration Django
sys.path.append('backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from core.models import UserProfile

def fix_authentication():
    """Corriger complètement l'authentification"""
    print("🔧 Correction complète de l'authentification...")
    
    # 1. Corriger l'utilisateur admin
    try:
        admin_user = User.objects.get(username='admin')
        print(f"✅ Utilisateur admin trouvé: {admin_user.username}")
        
        # Mettre à jour l'email
        admin_user.email = 'admin@aymencars.com'
        admin_user.save()
        
        # Redéfinir le mot de passe
        admin_user.set_password('admin123')
        admin_user.save()
        
        # Vérifier le profil
        profile, created = UserProfile.objects.get_or_create(
            user=admin_user,
            defaults={'role': 'admin'}
        )
        if not created:
            profile.role = 'admin'
            profile.save()
        
        print(f"   ✅ Admin configuré: {admin_user.email} / admin123")
        
        # Test de connexion
        user = authenticate(username=admin_user.email, password='admin123')
        if user:
            print(f"   ✅ Connexion admin avec email: SUCCÈS")
        else:
            print(f"   ❌ Connexion admin avec email: ÉCHEC")
        
        user = authenticate(username=admin_user.username, password='admin123')
        if user:
            print(f"   ✅ Connexion admin avec username: SUCCÈS")
        else:
            print(f"   ❌ Connexion admin avec username: ÉCHEC")
            
    except User.DoesNotExist:
        print("❌ Utilisateur admin non trouvé")
    
    # 2. Corriger l'utilisateur test
    try:
        test_user = User.objects.get(username='test')
        print(f"✅ Utilisateur test trouvé: {test_user.username}")
        
        # Mettre à jour l'email
        test_user.email = 'test@aymencars.com'
        test_user.save()
        
        # Redéfinir le mot de passe
        test_user.set_password('test123')
        test_user.save()
        
        # Vérifier le profil
        profile, created = UserProfile.objects.get_or_create(
            user=test_user,
            defaults={'role': 'admin'}
        )
        if not created:
            profile.role = 'admin'
            profile.save()
        
        print(f"   ✅ Test configuré: {test_user.email} / test123")
        
        # Test de connexion
        user = authenticate(username=test_user.email, password='test123')
        if user:
            print(f"   ✅ Connexion test avec email: SUCCÈS")
        else:
            print(f"   ❌ Connexion test avec email: ÉCHEC")
            
    except User.DoesNotExist:
        print("❌ Utilisateur test non trouvé")
    
    # 3. Corriger l'utilisateur client
    try:
        client_user = User.objects.get(username='client')
        print(f"✅ Utilisateur client trouvé: {client_user.username}")
        
        # Mettre à jour l'email
        client_user.email = 'client@aymencars.com'
        client_user.save()
        
        # Redéfinir le mot de passe
        client_user.set_password('client123')
        client_user.save()
        
        # Vérifier le profil
        profile, created = UserProfile.objects.get_or_create(
            user=client_user,
            defaults={'role': 'client'}
        )
        if not created:
            profile.role = 'client'
            profile.save()
        
        print(f"   ✅ Client configuré: {client_user.email} / client123")
        
        # Test de connexion
        user = authenticate(username=client_user.email, password='client123')
        if user:
            print(f"   ✅ Connexion client avec email: SUCCÈS")
        else:
            print(f"   ❌ Connexion client avec email: ÉCHEC")
            
    except User.DoesNotExist:
        print("❌ Utilisateur client non trouvé")
    
    print(f"\n🔑 Identifiants finaux :")
    print(f"   Admin: admin@aymencars.com / admin123")
    print(f"   Test: test@aymencars.com / test123")
    print(f"   Client: client@aymencars.com / client123")
    
    print(f"\n🌐 Accès aux interfaces :")
    print(f"   Site principal: http://127.0.0.1:8000/")
    print(f"   Connexion: http://127.0.0.1:8000/login/")
    print(f"   Dashboard admin: http://127.0.0.1:8000/dashboard/")
    print(f"   Admin Django: http://127.0.0.1:8000/admin/")
    
    print(f"\n📝 Instructions de connexion :")
    print(f"   1. Allez sur http://127.0.0.1:8000/login/")
    print(f"   2. Utilisez: test@aymencars.com / test123")
    print(f"   3. Ou utilisez: admin@aymencars.com / admin123")
    print(f"   4. Ou utilisez: client@aymencars.com / client123")

if __name__ == "__main__":
    fix_authentication() 