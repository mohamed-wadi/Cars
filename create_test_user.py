import os
import sys
import django

# Configuration Django
sys.path.append('backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import UserProfile

def create_test_user():
    """Créer un utilisateur de test avec accès au dashboard"""
    print("👤 Création d'un utilisateur de test...")
    
    # Créer l'utilisateur
    test_user, created = User.objects.get_or_create(
        username='test',
        defaults={
            'email': 'test@aymencars.com',
            'first_name': 'Test',
            'last_name': 'User',
            'is_staff': True,
            'is_superuser': True
        }
    )
    
    if created:
        # Créer le profil admin
        UserProfile.objects.create(
            user=test_user,
            role='admin'
        )
        print("✅ Utilisateur de test créé avec succès !")
    else:
        # Mettre à jour le profil existant
        profile, profile_created = UserProfile.objects.get_or_create(
            user=test_user,
            defaults={'role': 'admin'}
        )
        if not profile_created:
            profile.role = 'admin'
            profile.save()
        print("✅ Utilisateur de test mis à jour !")
    
    # Définir le mot de passe
    test_user.set_password('test123')
    test_user.save()
    
    print(f"\n🔑 Identifiants de connexion :")
    print(f"   Username: {test_user.username}")
    print(f"   Email: {test_user.email}")
    print(f"   Password: test123")
    print(f"   Rôle: {test_user.profile.role}")
    print(f"   Staff: {test_user.is_staff}")
    print(f"   Superuser: {test_user.is_superuser}")
    
    print(f"\n🌐 Accès aux interfaces :")
    print(f"   Site principal: http://127.0.0.1:8000/")
    print(f"   Connexion: http://127.0.0.1:8000/login/")
    print(f"   Dashboard admin: http://127.0.0.1:8000/dashboard/")
    print(f"   Admin Django: http://127.0.0.1:8000/admin/")
    
    print(f"\n📝 Instructions de connexion :")
    print(f"   1. Allez sur http://127.0.0.1:8000/login/")
    print(f"   2. Utilisez les identifiants ci-dessus")
    print(f"   3. Vous serez automatiquement redirigé vers le dashboard")
    print(f"   4. Ou accédez directement à http://127.0.0.1:8000/dashboard/")

if __name__ == "__main__":
    create_test_user() 