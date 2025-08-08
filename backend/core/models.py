from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Car(models.Model):
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='cars/', blank=True, null=True)
    description = models.TextField(blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.brand} {self.model}"

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name

class Agency(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='France')
    phone = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.name} - {self.city}"

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    agency_start = models.ForeignKey(Agency, on_delete=models.SET_NULL, null=True, related_name='departures')
    agency_end = models.ForeignKey(Agency, on_delete=models.SET_NULL, null=True, related_name='returns')
    start_date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_date = models.DateField()
    end_time = models.TimeField(null=True, blank=True)
    services = models.ManyToManyField(Service, blank=True)
    promo_code = models.CharField(max_length=50, blank=True)
    driver_age = models.PositiveIntegerField(null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f"Reservation {self.id} - {self.user.username} - {self.car}"
