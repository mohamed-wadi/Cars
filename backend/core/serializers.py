from rest_framework import serializers
from .models import Car, Service, Reservation, Agency, UserProfile, Contact, Review
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'date_joined']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'role', 'phone', 'address', 'birth_date', 'created_at']

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    # Read-only nested output
    user = UserSerializer(read_only=True)
    car = CarSerializer(read_only=True)
    agency_start = AgencySerializer(read_only=True)
    agency_end = AgencySerializer(read_only=True)
    services = ServiceSerializer(many=True, read_only=True)
    
    # Write-only inputs for creation/update
    car_id = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all(), source='car', write_only=True)
    agency_start_id = serializers.PrimaryKeyRelatedField(queryset=Agency.objects.all(), source='agency_start', write_only=True)
    agency_end_id = serializers.PrimaryKeyRelatedField(queryset=Agency.objects.all(), source='agency_end', write_only=True)
    services_ids = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all(), many=True, source='services', required=False, write_only=True)
    
    class Meta:
        model = Reservation
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    car = CarSerializer(read_only=True)
    reservation = serializers.PrimaryKeyRelatedField(read_only=True)
    
    # Write-only inputs for creation
    car_id = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all(), source='car', write_only=True)
    reservation_id = serializers.PrimaryKeyRelatedField(queryset=Reservation.objects.all(), source='reservation', write_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'car', 'reservation', 'rating', 'title', 'comment', 'is_approved', 'created_at', 'car_id', 'reservation_id']
        read_only_fields = ['user', 'created_at']