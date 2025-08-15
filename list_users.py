import os
import sys
import django

# Configuration Django
sys.path.append('backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import UserProfile

def list_users():
    """Lister tous les utilisateurs disponibles"""
    print("👥 Liste de tous les utilisateurs disponibles")
    print("=" * 60)
    
    users = User.objects.all().order_by('username')
    
    if not users.exists():
        print("❌ Aucun utilisateur trouvé")
        return
    
    for i, user in enumerate(users, 1):
        try:
            profile = user.profile
            role = profile.role
        except UserProfile.DoesNotExist:
            role = "Pas de profil"
        
        print(f"\n{i}. 👤 {user.username}")
        print(f"   📧 Email: {user.email}")
        print(f"   👨‍💼 Nom complet: {user.get_full_name()}")
        print(f"   🎭 Rôle: {role}")
        print(f"   🔧 Staff: {user.is_staff}")
        print(f"   👑 Superuser: {user.is_superuser}")
        print(f"   📅 Date d'inscription: {user.date_joined.strftime('%d/%m/%Y')}")
        
        # Afficher les identifiants de test
        if user.username in ['admin', 'test', 'client']:
            if user.username == 'admin':
                password = 'admin123'
            elif user.username == 'test':
                password = 'test123'
            elif user.username == 'client':
                password = 'client123'
            
            print(f"   🔑 Identifiants de test:")
            print(f"      Username: {user.username}")
            print(f"      Password: {password}")
    
    print(f"\n" + "=" * 60)
    print("🌐 Accès aux interfaces :")
    print("   Site principal: http://127.0.0.1:8000/")
    print("   Connexion: http://127.0.0.1:8000/login/")
    print("   Dashboard admin: http://127.0.0.1:8000/dashboard/")
    print("   Admin Django: http://127.0.0.1:8000/admin/")
    
    print(f"\n📝 Comptes recommandés pour les tests :")
    print("   🎯 Dashboard HTML: test@aymencars.com / test123")
    print("   🎯 Admin Django: admin@aymencars.com / admin123")
    print("   🎯 Client: client@aymencars.com / client123")

if __name__ == "__main__":
    list_users() 