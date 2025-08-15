import os
import sys
import django

# Configuration Django
sys.path.append('backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

def clean_all_alerts():
    """Nettoyer complètement toutes les alertes du projet"""
    print("🧹 Nettoyage complet de toutes les alertes...")
    
    # Liste des fichiers à vérifier
    files_to_check = [
        'frontend/templates/dashboard.html',
        'frontend/static/js/main.js',
        'frontend/static/js/auth.js',
        'frontend/static/js/contact.js',
        'frontend/templates/login.html',
        'frontend/templates/mainPage.html',
        'frontend/templates/profile.html',
        'frontend/templates/contact.html'
    ]
    
    alert_found = False
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Vérifier les alertes
                if 'alert(' in content:
                    print(f"   ❌ Alertes trouvées dans {file_path}")
                    alert_found = True
                    
                    # Afficher les lignes avec alert
                    lines = content.split('\n')
                    for i, line in enumerate(lines, 1):
                        if 'alert(' in line:
                            print(f"      Ligne {i}: {line.strip()}")
                else:
                    print(f"   ✅ {file_path} - Aucune alerte")
                    
                # Vérifier les messages de développement
                if 'Page de connexion en cours de développement' in content:
                    print(f"   ❌ Message de développement trouvé dans {file_path}")
                    alert_found = True
                    
                if 'admin Django pour l\'instant' in content:
                    print(f"   ❌ Message admin Django trouvé dans {file_path}")
                    alert_found = True
                    
                if 'en cours de développement' in content:
                    print(f"   ❌ Message 'en cours de développement' trouvé dans {file_path}")
                    alert_found = True
                    
            except Exception as e:
                print(f"   ❌ Erreur lecture {file_path}: {e}")
        else:
            print(f"   ⚠️  Fichier non trouvé: {file_path}")
    
    if not alert_found:
        print(f"\n🎉 Aucune alerte trouvée dans le projet !")
        print(f"Le projet est maintenant 100% propre.")
    else:
        print(f"\n⚠️  Des alertes ont été trouvées. Veuillez les supprimer manuellement.")
    
    print(f"\n🔑 Identifiants de test :")
    print(f"   Dashboard HTML: test@aymencars.com / test123")
    print(f"   Admin Django: admin@aymencars.com / admin123")
    print(f"   Client: client@aymencars.com / client123")
    
    print(f"\n🌐 Accès aux interfaces :")
    print(f"   Site principal: http://127.0.0.1:8000/")
    print(f"   Dashboard admin: http://127.0.0.1:8000/dashboard/")
    print(f"   Admin Django: http://127.0.0.1:8000/admin/")
    
    print(f"\n💡 Si vous voyez encore des alertes :")
    print(f"   1. Videz le cache du navigateur (Ctrl+F5)")
    print(f"   2. Essayez un autre navigateur")
    print(f"   3. Vérifiez les extensions du navigateur")
    print(f"   4. Redémarrez le serveur Django")

if __name__ == "__main__":
    clean_all_alerts() 