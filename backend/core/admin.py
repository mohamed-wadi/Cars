from django.contrib import admin
from .models import Car, Service, Reservation, Agency

admin.site.register(Car)
admin.site.register(Service)
admin.site.register(Reservation)
admin.site.register(Agency)
