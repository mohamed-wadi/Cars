from rest_framework import serializers
from .models import Car, Service, Reservation, Agency
from django.contrib.auth.models import User

class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = '__all__'

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    car = CarSerializer(read_only=True)
    services = ServiceSerializer(many=True, read_only=True)
    agency_start = AgencySerializer(read_only=True)
    agency_end = AgencySerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = '__all__' 