import os
import sys
import django

# Configuration Django
sys.path.append('backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from core.models import Car
import requests
from io import BytesIO
from django.core.files import File

# Données des voitures
cars_data = [
    {
        'brand': 'BMW',
        'model': 'X5',
        'price_per_day': 120.00,
        'description': 'SUV luxueux avec toutes les options modernes',
        'year': 2022,
        'mileage': 15000,
        'fuel_type': 'hybrid',
        'transmission': 'automatic',
        'seats': 5
    },
    {
        'brand': 'Mercedes',
        'model': 'Classe C 200',
        'price_per_day': 95.00,
        'description': 'Berline élégante et confortable',
        'year': 2023,
        'mileage': 8000,
        'fuel_type': 'essence',
        'transmission': 'automatic',
        'seats': 5
    },
    {
        'brand': 'Audi',
        'model': 'A4',
        'price_per_day': 85.00,
        'description': 'Berline sportive avec finition premium',
        'year': 2022,
        'mileage': 12000,
        'fuel_type': 'diesel',
        'transmission': 'manual',
        'seats': 5
    },
    {
        'brand': 'Volkswagen',
        'model': 'Golf',
        'price_per_day': 65.00,
        'description': 'Compacte polyvalente et économique',
        'year': 2021,
        'mileage': 25000,
        'fuel_type': 'essence',
        'transmission': 'manual',
        'seats': 5
    },
    {
        'brand': 'Peugeot',
        'model': '3008',
        'price_per_day': 75.00,
        'description': 'SUV moderne avec design innovant',
        'year': 2023,
        'mileage': 5000,
        'fuel_type': 'hybrid',
        'transmission': 'automatic',
        'seats': 5
    },
    {
        'brand': 'Renault',
        'model': 'Clio',
        'price_per_day': 45.00,
        'description': 'Citadine parfaite pour la ville',
        'year': 2022,
        'mileage': 18000,
        'fuel_type': 'essence',
        'transmission': 'manual',
        'seats': 5
    },
    {
        'brand': 'Tesla',
        'model': 'Model 3',
        'price_per_day': 130.00,
        'description': 'Voiture électrique haute performance',
        'year': 2023,
        'mileage': 3000,
        'fuel_type': 'electric',
        'transmission': 'automatic',
        'seats': 5
    },
    {
        'brand': 'Toyota',
        'model': 'Yaris',
        'price_per_day': 50.00,
        'description': 'Compacte hybride économique',
        'year': 2022,
        'mileage': 15000,
        'fuel_type': 'hybrid',
        'transmission': 'automatic',
        'seats': 5
    },
    {
        'brand': 'Ford',
        'model': 'Focus',
        'price_per_day': 60.00,
        'description': 'Berline familiale fiable',
        'year': 2021,
        'mileage': 22000,
        'fuel_type': 'diesel',
        'transmission': 'manual',
        'seats': 5
    },
    {
        'brand': 'Citroën',
        'model': 'C3',
        'price_per_day': 55.00,
        'description': 'Citadine avec design unique',
        'year': 2023,
        'mileage': 7000,
        'fuel_type': 'essence',
        'transmission': 'manual',
        'seats': 5
    }
]

def download_image(brand, model):
    """Télécharger une image depuis Unsplash"""
    try:
        query = f"{brand} {model} car"
        url = f"https://source.unsplash.com/800x600/?{query}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return BytesIO(response.content)
    except:
        pass
    return None

def add_cars():
    """Ajouter les voitures à la base de données"""
    print("🚗 Ajout des voitures...")
    
    for i, car_data in enumerate(cars_data):
        # Vérifier si la voiture existe déjà
        existing_car = Car.objects.filter(
            brand=car_data['brand'],
            model=car_data['model']
        ).first()
        
        if existing_car:
            print(f"⚠️  {car_data['brand']} {car_data['model']} existe déjà")
            continue
        
        # Créer la voiture
        car = Car.objects.create(
            brand=car_data['brand'],
            model=car_data['model'],
            price_per_day=car_data['price_per_day'],
            description=car_data['description'],
            year=car_data['year'],
            mileage=car_data['mileage'],
            fuel_type=car_data['fuel_type'],
            transmission=car_data['transmission'],
            seats=car_data['seats'],
            available=True
        )
        
        # Télécharger et ajouter l'image
        image_data = download_image(car_data['brand'], car_data['model'])
        if image_data:
            filename = f"{car_data['brand'].lower()}_{car_data['model'].lower().replace(' ', '_')}.jpg"
            car.image.save(filename, File(image_data), save=True)
        
        print(f"✅ {car_data['brand']} {car_data['model']} ajoutée")
    
    print(f"\n🎉 {Car.objects.count()} voitures disponibles dans la base de données")

if __name__ == "__main__":
    add_cars() 