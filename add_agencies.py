import os
import sys
import django
from pathlib import Path

# Configuration Django
sys.path.append(str(Path(__file__).parent / 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from core.models import Agency

# Données des agences
agencies_data = [
    {
        'name': 'Aymen Car\'s - Paris Centre',
        'address': '123 Avenue des Champs-Élysées',
        'city': 'Paris',
        'country': 'France',
        'phone': '+33 1 23 45 67 89'
    },
    {
        'name': 'Aymen Car\'s - Paris Nord',
        'address': '456 Boulevard de la Chapelle',
        'city': 'Paris',
        'country': 'France',
        'phone': '+33 1 98 76 54 32'
    },
    {
        'name': 'Aymen Car\'s - Lyon Centre',
        'address': '789 Rue de la République',
        'city': 'Lyon',
        'country': 'France',
        'phone': '+33 4 72 34 56 78'
    },
    {
        'name': 'Aymen Car\'s - Marseille',
        'address': '321 La Canebière',
        'city': 'Marseille',
        'country': 'France',
        'phone': '+33 4 91 23 45 67'
    },
    {
        'name': 'Aymen Car\'s - Toulouse',
        'address': '654 Place du Capitole',
        'city': 'Toulouse',
        'country': 'France',
        'phone': '+33 5 61 23 45 67'
    },
    {
        'name': 'Aymen Car\'s - Nice',
        'address': '987 Promenade des Anglais',
        'city': 'Nice',
        'country': 'France',
        'phone': '+33 4 93 12 34 56'
    },
    {
        'name': 'Aymen Car\'s - Bordeaux',
        'address': '147 Place de la Bourse',
        'city': 'Bordeaux',
        'country': 'France',
        'phone': '+33 5 56 78 90 12'
    },
    {
        'name': 'Aymen Car\'s - Nantes',
        'address': '258 Cours Cambronne',
        'city': 'Nantes',
        'country': 'France',
        'phone': '+33 2 40 12 34 56'
    }
]

def add_agencies():
    """Ajoute les agences à la base de données"""
    print("🏢 Ajout des agences Aymen Car's...")
    
    for i, agency_data in enumerate(agencies_data, 1):
        try:
            agency, created = Agency.objects.get_or_create(
                name=agency_data['name'],
                defaults=agency_data
            )
            
            if created:
                print(f"✅ {agency_data['name']} ajoutée")
            else:
                print(f"ℹ️  {agency_data['name']} existe déjà")
                
        except Exception as e:
            print(f"❌ Erreur ajout {agency_data['name']}: {e}")

if __name__ == "__main__":
    print("🎯 Script d'ajout d'agences Aymen Car's")
    print("=" * 50)
    
    add_agencies()
    
    print("\n" + "=" * 50)
    print("🎉 Script terminé !")
    print(f"📊 Total agences en base: {Agency.objects.count()}")
    print("🌐 Accédez à http://127.0.0.1:8000/ pour voir le site")
    print("🔧 Accédez à http://127.0.0.1:8000/admin/ pour gérer les agences") 