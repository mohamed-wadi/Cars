import os
import sys
import django

# Configuration Django
sys.path.append('backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import UserProfile

def fix_admin_user():
    """Corriger l'utilisateur admin avec le bon email"""
    print("🔧 Correction de l'utilisateur admin...")
    
    try:
        # Récupérer l'utilisateur admin existant
        admin_user = User.objects.get(username='admin')
        print(f"✅ Utilisateur admin trouvé: {admin_user.username}")
        print(f"   Email actuel: {admin_user.email}")
        
        # Mettre à jour l'email
        admin_user.email = 'admin@aymencars.com'
        admin_user.save()
        print(f"✅ Email mis à jour: {admin_user.email}")
        
        # Vérifier/créer le profil admin
        profile, created = UserProfile.objects.get_or_create(
            user=admin_user,
            defaults={'role': 'admin'}
        )
        
        if created:
            print("✅ Profil admin créé")
        else:
            profile.role = 'admin'
            profile.save()
            print("✅ Profil admin mis à jour")
        
        # Redéfinir le mot de passe
        admin_user.set_password('admin123')
        admin_user.save()
        print("✅ Mot de passe redéfini")
        
        print(f"\n🔑 Identifiants corrigés :")
        print(f"   Username: {admin_user.username}")
        print(f"   Email: {admin_user.email}")
        print(f"   Password: admin123")
        print(f"   Rôle: {admin_user.profile.role}")
        print(f"   Staff: {admin_user.is_staff}")
        print(f"   Superuser: {admin_user.is_superuser}")
        
        print(f"\n🌐 Accès aux interfaces :")
        print(f"   Site principal: http://127.0.0.1:8000/")
        print(f"   Connexion: http://127.0.0.1:8000/login/")
        print(f"   Dashboard admin: http://127.0.0.1:8000/dashboard/")
        print(f"   Admin Django: http://127.0.0.1:8000/admin/")
        
        print(f"\n📝 Test de connexion :")
        print(f"   1. Allez sur http://127.0.0.1:8000/login/")
        print(f"   2. Utilisez: admin@aymencars.com / admin123")
        print(f"   3. Ou utilisez: test@aymencars.com / test123")
        
    except User.DoesNotExist:
        print("❌ Utilisateur admin non trouvé")
        print("Création d'un nouvel utilisateur admin...")
        
        # Créer un nouvel utilisateur admin
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@aymencars.com',
            password='admin123'
        )
        
        # Créer le profil admin
        UserProfile.objects.create(
            user=admin_user,
            role='admin'
        )
        
        print("✅ Nouvel utilisateur admin créé !")
        print(f"   Username: {admin_user.username}")
        print(f"   Email: {admin_user.email}")
        print(f"   Password: admin123")

if __name__ == "__main__":
    fix_admin_user() 