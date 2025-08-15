import os
import sys
import django
from pathlib import Path

# Configuration Django
sys.path.append('backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from core.models import Agency

# Données des agences
agencies_data = [
    {
        'name': 'Aymen Car\'s - Paris Centre',
        'address': '123 Avenue des Champs-Élysées, 75008 Paris',
        'city': 'Paris',
        'country': 'France',
        'phone': '+33 1 42 65 43 21',
        'email': 'paris@aymencars.com',
        'opening_hours': '8h-20h'
    },
    {
        'name': 'Aymen Car\'s - Lyon Part-Dieu',
        'address': '45 Rue de la Part-Dieu, 69003 Lyon',
        'city': 'Lyon',
        'country': 'France',
        'phone': '+33 4 78 62 34 56',
        'email': 'lyon@aymencars.com',
        'opening_hours': '8h-19h'
    },
    {
        'name': 'Aymen Car\'s - Marseille Vieux-Port',
        'address': '78 Quai des Belges, 13001 Marseille',
        'city': 'Marseille',
        'country': 'France',
        'phone': '+33 4 91 54 32 10',
        'email': 'marseille@aymencars.com',
        'opening_hours': '8h-18h'
    },
    {
        'name': 'Aymen Car\'s - Toulouse Capitole',
        'address': '12 Place du Capitole, 31000 Toulouse',
        'city': 'Toulouse',
        'country': 'France',
        'phone': '+33 5 61 23 45 67',
        'email': 'toulouse@aymencars.com',
        'opening_hours': '8h-19h'
    },
    {
        'name': 'Aymen Car\'s - Nice Promenade',
        'address': '25 Promenade des Anglais, 06000 Nice',
        'city': 'Nice',
        'country': 'France',
        'phone': '+33 4 93 87 65 43',
        'email': 'nice@aymencars.com',
        'opening_hours': '8h-20h'
    },
    {
        'name': 'Aymen Car\'s - Bordeaux Mériadeck',
        'address': '15 Place Pey-Berland, 33000 Bordeaux',
        'city': 'Bordeaux',
        'country': 'France',
        'phone': '+33 5 56 78 90 12',
        'email': 'bordeaux@aymencars.com',
        'opening_hours': '8h-18h'
    },
    {
        'name': 'Aymen Car\'s - Nantes Centre',
        'address': '8 Place du Commerce, 44000 Nantes',
        'city': 'Nantes',
        'country': 'France',
        'phone': '+33 2 40 12 34 56',
        'email': 'nantes@aymencars.com',
        'opening_hours': '8h-19h'
    },
    {
        'name': 'Aymen Car\'s - Strasbourg Grand Île',
        'address': '3 Place de la Cathédrale, 67000 Strasbourg',
        'city': 'Strasbourg',
        'country': 'France',
        'phone': '+33 3 88 76 54 32',
        'email': 'strasbourg@aymencars.com',
        'opening_hours': '8h-18h'
    }
]

def add_agencies():
    """Ajouter les agences à la base de données"""
    print("🏢 Ajout des agences...")
    
    for agency_data in agencies_data:
        # Vérifier si l'agence existe déjà
        existing_agency = Agency.objects.filter(
            name=agency_data['name']
        ).first()
        
        if existing_agency:
            print(f"⚠️  {agency_data['name']} existe déjà")
            continue
        
        # Créer l'agence
        agency = Agency.objects.create(
            name=agency_data['name'],
            address=agency_data['address'],
            city=agency_data['city'],
            country=agency_data['country'],
            phone=agency_data['phone'],
            email=agency_data['email'],
            opening_hours=agency_data['opening_hours']
        )
        
        print(f"✅ {agency_data['name']} ajoutée")
    
    print(f"\n🎉 {Agency.objects.count()} agences disponibles dans la base de données")

if __name__ == "__main__":
    add_agencies() 