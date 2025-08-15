import os
import sys
import django

# Configuration Django
sys.path.append('backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import UserProfile

def create_client_user():
    """Créer un utilisateur client pour tester les réservations"""
    print("👤 Création d'un utilisateur client...")
    
    # Créer l'utilisateur client
    client_user, created = User.objects.get_or_create(
        username='client',
        defaults={
            'email': 'client@aymencars.com',
            'first_name': 'Jean',
            'last_name': 'Dupont',
            'is_staff': False,
            'is_superuser': False
        }
    )
    
    if created:
        # Créer le profil client
        UserProfile.objects.create(
            user=client_user,
            role='client',
            phone='+33 6 12 34 56 78'
        )
        print("✅ Utilisateur client créé avec succès !")
    else:
        # Mettre à jour le profil existant
        profile, profile_created = UserProfile.objects.get_or_create(
            user=client_user,
            defaults={'role': 'client'}
        )
        if not profile_created:
            profile.role = 'client'
            profile.save()
        print("✅ Utilisateur client mis à jour !")
    
    # Définir le mot de passe
    client_user.set_password('client123')
    client_user.save()
    
    print(f"\n🔑 Identifiants client :")
    print(f"   Username: {client_user.username}")
    print(f"   Email: {client_user.email}")
    print(f"   Password: client123")
    print(f"   Rôle: {client_user.profile.role}")
    print(f"   Nom complet: {client_user.get_full_name()}")
    
    print(f"\n🌐 Accès aux interfaces :")
    print(f"   Site principal: http://127.0.0.1:8000/")
    print(f"   Connexion: http://127.0.0.1:8000/login/")
    print(f"   Profil utilisateur: http://127.0.0.1:8000/profile/")
    
    print(f"\n📝 Instructions de connexion :")
    print(f"   1. Allez sur http://127.0.0.1:8000/login/")
    print(f"   2. Utilisez les identifiants client ci-dessus")
    print(f"   3. Vous pourrez réserver des voitures")
    print(f"   4. Accédez à votre profil pour voir vos réservations")

if __name__ == "__main__":
    create_client_user() 