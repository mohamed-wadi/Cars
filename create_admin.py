import os
import sys
import django

# Configuration Django
sys.path.append('backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import UserProfile

# Créer un superutilisateur
try:
    # Vérifier si l'utilisateur admin existe déjà
    if User.objects.filter(username='admin').exists():
        print("✅ L'utilisateur admin existe déjà")
        admin_user = User.objects.get(username='admin')
        print(f"   Username: {admin_user.username}")
        print(f"   Email: {admin_user.email}")
        print(f"   Superuser: {admin_user.is_superuser}")
        
        # Créer ou mettre à jour le profil admin
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
            
    else:
        # Créer un nouveau superutilisateur
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@aymencars.com',
            password='admin123'
        )
        print("✅ Superutilisateur créé avec succès !")
        print(f"   Username: admin")
        print(f"   Email: admin@aymencars.com")
        print(f"   Password: admin123")
        
        # Créer le profil admin
        UserProfile.objects.create(
            user=admin_user,
            role='admin'
        )
        print("✅ Profil admin créé")
    
    print("\n🌐 Accédez à l'admin Django :")
    print("   URL: http://127.0.0.1:8000/admin/")
    print("   Username: admin")
    print("   Password: admin123")
    
    print("\n🚗 Accédez au dashboard frontend :")
    print("   URL: http://127.0.0.1:8000/dashboard/")
    print("   Username: admin")
    print("   Password: admin123")
    
except Exception as e:
    print(f"❌ Erreur lors de la création du superutilisateur: {e}") 