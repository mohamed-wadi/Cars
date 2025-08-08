import os
import sys
import django
import requests
from pathlib import Path

# Configuration Django
sys.path.append(str(Path(__file__).parent / 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from core.models import Car

# URLs des images de voitures (Unsplash - libres de droits)
car_images = [
    {
        'url': 'https://images.unsplash.com/photo-1555215695-3004980ad54e?w=800&h=600&fit=crop',
        'filename': 'bmw_x5.jpg',
        'brand': 'BMW',
        'model': 'X5',
        'price': 120.00,
        'description': 'SUV de luxe BMW X5, parfait pour les familles et les voyages.'
    },
    {
        'url': 'https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?w=800&h=600&fit=crop',
        'filename': 'mercedes_c200.jpg',
        'brand': 'Mercedes',
        'model': 'Classe C 200',
        'price': 95.00,
        'description': 'Berline élégante Mercedes Classe C, confort et style garantis.'
    },
    {
        'url': 'https://images.unsplash.com/photo-1614200187524-dc4b892acf16?w=800&h=600&fit=crop',
        'filename': 'audi_a4.jpg',
        'brand': 'Audi',
        'model': 'A4',
        'price': 85.00,
        'description': 'Audi A4, performance et technologie allemande.'
    },
    {
        'url': 'https://images.unsplash.com/photo-1614200187524-dc4b892acf16?w=800&h=600&fit=crop',
        'filename': 'volkswagen_golf.jpg',
        'brand': 'Volkswagen',
        'model': 'Golf',
        'price': 65.00,
        'description': 'Volkswagen Golf, polyvalente et économique.'
    },
    {
        'url': 'https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?w=800&h=600&fit=crop',
        'filename': 'peugeot_3008.jpg',
        'brand': 'Peugeot',
        'model': '3008',
        'price': 75.00,
        'description': 'SUV Peugeot 3008, design moderne et spacieux.'
    },
    {
        'url': 'https://images.unsplash.com/photo-1555215695-3004980ad54e?w=800&h=600&fit=crop',
        'filename': 'renault_clio.jpg',
        'brand': 'Renault',
        'model': 'Clio',
        'price': 45.00,
        'description': 'Citadine Renault Clio, parfaite pour la ville.'
    },
    {
        'url': 'https://images.unsplash.com/photo-1614200187524-dc4b892acf16?w=800&h=600&fit=crop',
        'filename': 'toyota_corolla.jpg',
        'brand': 'Toyota',
        'model': 'Corolla',
        'price': 55.00,
        'description': 'Toyota Corolla, fiabilité japonaise reconnue.'
    },
    {
        'url': 'https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?w=800&h=600&fit=crop',
        'filename': 'honda_civic.jpg',
        'brand': 'Honda',
        'model': 'Civic',
        'price': 60.00,
        'description': 'Honda Civic, sportive et économique.'
    },
    {
        'url': 'https://images.unsplash.com/photo-1555215695-3004980ad54e?w=800&h=600&fit=crop',
        'filename': 'ford_focus.jpg',
        'brand': 'Ford',
        'model': 'Focus',
        'price': 50.00,
        'description': 'Ford Focus, conduite dynamique et confortable.'
    },
    {
        'url': 'https://images.unsplash.com/photo-1614200187524-dc4b892acf16?w=800&h=600&fit=crop',
        'filename': 'citroen_c3.jpg',
        'brand': 'Citroën',
        'model': 'C3',
        'price': 40.00,
        'description': 'Citroën C3, design unique et confort optimal.'
    }
]

def download_image(url, filename):
    """Télécharge une image depuis une URL"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Chemin vers le dossier media/cars
        media_path = Path(__file__).parent / 'media' / 'cars'
        media_path.mkdir(parents=True, exist_ok=True)
        
        file_path = media_path / filename
        with open(file_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ Image téléchargée: {filename}")
        return f'cars/{filename}'
    except Exception as e:
        print(f"❌ Erreur téléchargement {filename}: {e}")
        return None

def add_cars_to_database():
    """Ajoute les voitures à la base de données"""
    print("🚗 Ajout des voitures à la base de données...")
    
    for i, car_data in enumerate(car_images, 1):
        print(f"\n--- Voiture {i}/10 ---")
        
        # Télécharger l'image
        image_path = download_image(car_data['url'], car_data['filename'])
        
        # Créer la voiture dans la base de données
        try:
            car = Car.objects.create(
                brand=car_data['brand'],
                model=car_data['model'],
                price_per_day=car_data['price'],
                description=car_data['description'],
                available=True
            )
            
            # Si l'image a été téléchargée, l'assigner
            if image_path:
                car.image = image_path
                car.save()
            
            print(f"✅ {car_data['brand']} {car_data['model']} ajoutée (€{car_data['price']}/jour)")
            
        except Exception as e:
            print(f"❌ Erreur ajout {car_data['brand']} {car_data['model']}: {e}")

if __name__ == "__main__":
    print("🎯 Script d'ajout de voitures Aymen Car's")
    print("=" * 50)
    
    # Vérifier si des voitures existent déjà
    existing_cars = Car.objects.count()
    if existing_cars > 0:
        print(f"⚠️  {existing_cars} voiture(s) existent déjà dans la base de données.")
        response = input("Voulez-vous continuer et ajouter 10 nouvelles voitures ? (o/n): ")
        if response.lower() not in ['o', 'oui', 'y', 'yes']:
            print("❌ Opération annulée.")
            sys.exit(0)
    
    add_cars_to_database()
    print("\n" + "=" * 50)
    print("🎉 Script terminé !")
    print(f"📊 Total voitures en base: {Car.objects.count()}")
    print("🌐 Accédez à http://127.0.0.1:8000/ pour voir le site")
    print("🔧 Accédez à http://127.0.0.1:8000/admin/ pour gérer les voitures") 