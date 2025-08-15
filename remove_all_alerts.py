import os
import sys
import re

def remove_all_alerts():
    """Supprimer toutes les alertes du projet de manière agressive"""
    print("🗑️ Suppression agressive de toutes les alertes...")
    
    # Liste des fichiers à traiter
    files_to_process = [
        'frontend/templates/dashboard.html',
        'frontend/static/js/main.js',
        'frontend/static/js/auth.js',
        'frontend/static/js/contact.js',
        'frontend/templates/login.html',
        'frontend/templates/mainPage.html',
        'frontend/templates/profile.html',
        'frontend/templates/contact.html'
    ]
    
    total_alerts_removed = 0
    
    for file_path in files_to_process:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                alerts_removed = 0
                
                # Supprimer toutes les alertes JavaScript
                # Pattern 1: alert('message')
                content = re.sub(r"alert\s*\(\s*['\"`][^'\"`]*['\"`]\s*\)\s*;?", "", content)
                alerts_removed += len(re.findall(r"alert\s*\(\s*['\"`][^'\"`]*['\"`]\s*\)\s*;?", original_content))
                
                # Pattern 2: alert(`message`)
                content = re.sub(r"alert\s*\(\s*`[^`]*`\s*\)\s*;?", "", content)
                alerts_removed += len(re.findall(r"alert\s*\(\s*`[^`]*`\s*\)\s*;?", original_content))
                
                # Pattern 3: alert(message)
                content = re.sub(r"alert\s*\(\s*[^)]+\s*\)\s*;?", "", content)
                alerts_removed += len(re.findall(r"alert\s*\(\s*[^)]+\s*\)\s*;?", original_content))
                
                # Supprimer les lignes contenant des alertes
                lines = content.split('\n')
                cleaned_lines = []
                for line in lines:
                    if 'alert(' not in line and 'alert (' not in line:
                        cleaned_lines.append(line)
                    else:
                        alerts_removed += 1
                
                content = '\n'.join(cleaned_lines)
                
                # Supprimer les messages de développement
                development_messages = [
                    "Page de connexion en cours de développement",
                    "admin Django pour l'instant",
                    "en cours de développement",
                    "Utilisez l'admin Django",
                    "Fonctionnalité en cours de développement",
                    "Page en cours de développement"
                ]
                
                for message in development_messages:
                    if message in content:
                        content = content.replace(message, "")
                        alerts_removed += 1
                
                # Écrire le fichier nettoyé
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"   ✅ {file_path} - {alerts_removed} alertes supprimées")
                    total_alerts_removed += alerts_removed
                else:
                    print(f"   ✅ {file_path} - Aucune alerte trouvée")
                    
            except Exception as e:
                print(f"   ❌ Erreur traitement {file_path}: {e}")
        else:
            print(f"   ⚠️  Fichier non trouvé: {file_path}")
    
    print(f"\n🎉 Nettoyage terminé !")
    print(f"Total d'alertes supprimées: {total_alerts_removed}")
    
    if total_alerts_removed > 0:
        print(f"✅ Le projet a été nettoyé avec succès !")
    else:
        print(f"✅ Le projet était déjà propre !")
    
    print(f"\n🔑 Identifiants de test :")
    print(f"   Dashboard HTML: test@aymencars.com / test123")
    print(f"   Admin Django: admin@aymencars.com / admin123")
    print(f"   Client: client@aymencars.com / client123")
    
    print(f"\n🌐 Accès aux interfaces :")
    print(f"   Site principal: http://127.0.0.1:8000/")
    print(f"   Dashboard admin: http://127.0.0.1:8000/dashboard/")
    print(f"   Admin Django: http://127.0.0.1:8000/admin/")
    
    print(f"\n💡 Instructions après nettoyage :")
    print(f"   1. Videz le cache du navigateur (Ctrl+F5)")
    print(f"   2. Redémarrez le serveur Django")
    print(f"   3. Testez dans une fenêtre privée")

if __name__ == "__main__":
    remove_all_alerts() 