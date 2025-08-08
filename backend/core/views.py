from django.shortcuts import render, redirect
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from datetime import datetime, timedelta
from .models import Car, Service, Reservation, Agency
from .serializers import CarSerializer, ServiceSerializer, ReservationSerializer, AgencySerializer

def main_page(request):
    return render(request, 'mainPage.html')

def contact_page(request):
    return render(request, 'contact.html')

def login_page(request):
    return render(request, 'login.html')

def profile_page(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    return render(request, 'profile.html')

class CarViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Car.objects.filter(available=True)
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Recherche et filtrage des voitures"""
        query = request.query_params.get('q', '')
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        brand = request.query_params.get('brand')
        
        queryset = self.queryset
        
        if query:
            queryset = queryset.filter(
                Q(brand__icontains=query) | 
                Q(model__icontains=query) | 
                Q(description__icontains=query)
            )
        
        if min_price:
            queryset = queryset.filter(price_per_day__gte=min_price)
        
        if max_price:
            queryset = queryset.filter(price_per_day__lte=max_price)
        
        if brand:
            queryset = queryset.filter(brand__iexact=brand)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class AgencyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Agency.objects.all()
    serializer_class = AgencySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Calcul automatique du prix total
        car = serializer.validated_data['car']
        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']
        
        # Calcul du nombre de jours
        days = (end_date - start_date).days
        if days == 0:
            days = 1
        
        # Prix de base
        total_price = car.price_per_day * days
        
        # Ajout des services
        services = serializer.validated_data.get('services', [])
        for service in services:
            total_price += service.price
        
        # Application du code promo (exemple: 10% de réduction)
        promo_code = serializer.validated_data.get('promo_code', '')
        if promo_code and promo_code.upper() == 'WELCOME10':
            total_price *= 0.9
        
        # Sauvegarder la réservation
        reservation = serializer.save(
            user=self.request.user,
            total_price=total_price
        )
        
        return reservation

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Annuler une réservation"""
        reservation = self.get_object()
        
        # Vérifier si la réservation peut être annulée (plus de 24h avant)
        if reservation.start_date > datetime.now().date() + timedelta(days=1):
            reservation.status = 'cancelled'
            reservation.save()
            return Response({'message': 'Réservation annulée avec succès'})
        else:
            return Response(
                {'error': 'Impossible d\'annuler une réservation moins de 24h avant'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Réservations à venir"""
        queryset = self.get_queryset().filter(
            start_date__gte=datetime.now().date(),
            status='confirmed'
        ).order_by('start_date')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def past(self, request):
        """Réservations passées"""
        queryset = self.get_queryset().filter(
            end_date__lt=datetime.now().date()
        ).order_by('-end_date')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
