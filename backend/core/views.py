from django.shortcuts import render, redirect
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, SAFE_METHODS
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponseForbidden
import json
from .models import Car, Service, Reservation, Agency, UserProfile, Contact, Review, Payment
from .serializers import CarSerializer, ServiceSerializer, ReservationSerializer, AgencySerializer, ContactSerializer, UserProfileSerializer, ReviewSerializer
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET
from django.shortcuts import get_object_or_404
from .forms import CarForm, AgencyForm, ServiceForm, ReservationStatusForm, ContactAdminForm, UserAdminForm
from .email_utils import send_booking_confirmation_email, send_payment_confirmation_email, send_reservation_status_update_email, send_contact_response_email


def main_page(request):
    return render(request, 'mainPage.html')

def contact_page(request):
    return render(request, 'contact.html')

def login_page(request):
    return render(request, 'login.html')

def terms_page(request):
    return render(request, 'terms.html')

def faq_page(request):
    return render(request, 'faq.html')

def about_page(request):
    return render(request, 'about.html')

def profile_page(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    return render(request, 'profile.html')

def dashboard_page(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    
    # Vérifier si l'utilisateur est admin
    try:
        profile = request.user.profile
        if not profile.is_admin:
            return redirect('/')
    except UserProfile.DoesNotExist:
        # Si pas de profil, vérifier si c'est un superuser
        if not request.user.is_superuser and not request.user.is_staff:
            return redirect('/')
    
    return render(request, 'dashboard.html')

@csrf_exempt
def auth_login(request):
    """API endpoint pour la connexion"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username_or_email = data.get('username')
            password = data.get('password')
            
            # Essayer d'abord avec le username
            user = authenticate(request, username=username_or_email, password=password)
            
            # Si ça ne marche pas, essayer avec l'email
            if user is None:
                try:
                    user_with_email = User.objects.get(email=username_or_email)
                    user = authenticate(request, username=user_with_email.username, password=password)
                except User.DoesNotExist:
                    user = None
            
            if user is not None:
                login(request, user)
                
                # Récupérer le profil utilisateur
                try:
                    profile = user.profile
                    role = profile.role
                except UserProfile.DoesNotExist:
                    # Créer un profil par défaut si il n'existe pas
                    if user.is_superuser:
                        profile = UserProfile.objects.create(user=user, role='admin')
                        role = 'admin'
                    else:
                        profile = UserProfile.objects.create(user=user, role='client')
                        role = 'client'
                
                return JsonResponse({
                    'success': True,
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'is_staff': user.is_staff,
                        'is_superuser': user.is_superuser,
                        'role': role
                    },
                    'token': 'dummy_token'  # En production, utilisez JWT
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Email ou mot de passe incorrect'
                }, status=400)
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Erreur lors de la connexion'
            }, status=500)
    
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

@csrf_exempt
def auth_register(request):
    """API endpoint pour l'inscription (clients uniquement)"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            first_name = data.get('first_name', '')
            last_name = data.get('last_name', '')
            phone = data.get('phone', '')
            
            # Vérifier si l'utilisateur existe déjà
            if User.objects.filter(username=username).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'Un utilisateur avec cet email existe déjà'
                }, status=400)
            
            # Créer le nouvel utilisateur (client uniquement)
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            # Créer le profil utilisateur (client par défaut)
            profile = UserProfile.objects.create(
                user=user,
                role='client',
                phone=phone
            )
            
            return JsonResponse({
                'success': True,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'role': 'client'
                }
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Erreur lors de l\'inscription'
            }, status=500)
    
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

@csrf_exempt
def auth_logout(request):
    """API endpoint pour la déconnexion"""
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'success': True})
    
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

@csrf_exempt
def admin_users(request):
    """API endpoint pour récupérer tous les utilisateurs (admin)"""
    if request.method == 'GET':
        try:
            users = User.objects.all()
            users_data = []
            
            for user in users:
                try:
                    profile = user.profile
                    role = profile.role
                except UserProfile.DoesNotExist:
                    role = 'client'
                
                users_data.append({
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'is_active': user.is_active,
                    'is_staff': user.is_staff,
                    'role': role,
                    'date_joined': user.date_joined.isoformat()
                })
            
            return JsonResponse(users_data, safe=False)
            
        except Exception:
            return JsonResponse({
                'error': 'Erreur lors de la récupération des utilisateurs'
            }, status=500)
    
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

@csrf_exempt
def admin_user_detail(request, user_id: int):
    """GET, PUT/PATCH, DELETE pour un utilisateur (admin uniquement)"""
    # Vérifier admin
    is_admin = False
    if request.user.is_authenticated:
        try:
            is_admin = request.user.is_superuser or request.user.is_staff or getattr(request.user.profile, 'is_admin', False)
        except UserProfile.DoesNotExist:
            is_admin = request.user.is_superuser or request.user.is_staff
    if not is_admin:
        return JsonResponse({'detail': 'Forbidden'}, status=403)

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'detail': 'Not found'}, status=404)

    if request.method == 'GET':
        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_active': user.is_active,
            'is_staff': user.is_staff,
        }
        try:
            data['role'] = user.profile.role
        except UserProfile.DoesNotExist:
            data['role'] = 'client'
        return JsonResponse(data)

    if request.method in ['PUT', 'PATCH']:
        try:
            payload = json.loads(request.body or '{}')
        except json.JSONDecodeError:
            payload = {}
        user.first_name = payload.get('first_name', user.first_name)
        user.last_name = payload.get('last_name', user.last_name)
        user.email = payload.get('email', user.email)
        is_active = payload.get('is_active')
        if is_active is not None:
            user.is_active = bool(is_active)
        is_staff = payload.get('is_staff')
        if is_staff is not None:
            user.is_staff = bool(is_staff)
        # Rôle dans le profil
        role = payload.get('role')
        if role in ['client', 'admin']:
            try:
                profile = user.profile
            except UserProfile.DoesNotExist:
                profile = UserProfile.objects.create(user=user, role='client')
            profile.role = role
            profile.save()
        user.save()
        return JsonResponse({'success': True})

    if request.method == 'DELETE':
        user.delete()
        return JsonResponse({'success': True})

    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

@csrf_exempt
def contact_submit(request):
    """API endpoint pour soumettre un message de contact"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            contact = Contact.objects.create(
                name=data.get('name'),
                email=data.get('email'),
                phone=data.get('phone', ''),
                subject=data.get('subject'),
                message=data.get('message')
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Message envoyé avec succès'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Erreur lors de l\'envoi du message'
            }, status=500)
    
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def _is_admin(self, user):
        if not user.is_authenticated:
            return False
        try:
            return user.is_superuser or user.is_staff or getattr(user.profile, 'is_admin', False)
        except UserProfile.DoesNotExist:
            return user.is_superuser or user.is_staff

    def create(self, request, *args, **kwargs):
        if not self._is_admin(request.user):
            return Response({'detail': 'Forbidden'}, status=403)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not self._is_admin(request.user):
            return Response({'detail': 'Forbidden'}, status=403)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if not self._is_admin(request.user):
            return Response({'detail': 'Forbidden'}, status=403)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not self._is_admin(request.user):
            return Response({'detail': 'Forbidden'}, status=403)
        return super().destroy(request, *args, **kwargs)

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

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def _is_admin(self, user):
        if not user.is_authenticated:
            return False
        try:
            return user.is_superuser or user.is_staff or getattr(user.profile, 'is_admin', False)
        except UserProfile.DoesNotExist:
            return user.is_superuser or user.is_staff

    def create(self, request, *args, **kwargs):
        if not self._is_admin(request.user):
            return Response({'detail': 'Forbidden'}, status=403)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not self._is_admin(request.user):
            return Response({'detail': 'Forbidden'}, status=403)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if not self._is_admin(request.user):
            return Response({'detail': 'Forbidden'}, status=403)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not self._is_admin(request.user):
            return Response({'detail': 'Forbidden'}, status=403)
        return super().destroy(request, *args, **kwargs)

class AgencyViewSet(viewsets.ModelViewSet):
    queryset = Agency.objects.all()
    serializer_class = AgencySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def _is_admin(self, user):
        if not user.is_authenticated:
            return False
        try:
            return user.is_superuser or user.is_staff or getattr(user.profile, 'is_admin', False)
        except UserProfile.DoesNotExist:
            return user.is_superuser or user.is_staff

    def create(self, request, *args, **kwargs):
        if not self._is_admin(request.user):
            return Response({'detail': 'Forbidden'}, status=403)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not self._is_admin(request.user):
            return Response({'detail': 'Forbidden'}, status=403)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if not self._is_admin(request.user):
            return Response({'detail': 'Forbidden'}, status=403)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not self._is_admin(request.user):
            return Response({'detail': 'Forbidden'}, status=403)
        return super().destroy(request, *args, **kwargs)

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def _is_admin(self, user):
        if not user.is_authenticated:
            return False
        try:
            return user.is_superuser or user.is_staff or getattr(user.profile, 'is_admin', False)
        except UserProfile.DoesNotExist:
            return user.is_superuser or user.is_staff

    def create(self, request, *args, **kwargs):
        # Autoriser la création via le site public (non admin) déjà gérée par contact_submit
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not self._is_admin(request.user):
            return Response({'detail': 'Forbidden'}, status=403)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if not self._is_admin(request.user):
            return Response({'detail': 'Forbidden'}, status=403)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not self._is_admin(request.user):
            return Response({'detail': 'Forbidden'}, status=403)
        return super().destroy(request, *args, **kwargs)

class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def _is_admin(self, user):
        if not user.is_authenticated:
            return False
        try:
            return user.is_superuser or user.is_staff or getattr(user.profile, 'is_admin', False)
        except UserProfile.DoesNotExist:
            return user.is_superuser or user.is_staff

    def get_queryset(self):
        if self._is_admin(self.request.user):
            return Reservation.objects.all().order_by('-created_at')
        return Reservation.objects.filter(user=self.request.user).order_by('-created_at')

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
        
        # Send booking confirmation email
        send_booking_confirmation_email(reservation)
        
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

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only show approved reviews for non-admin users
        if self._is_admin(self.request.user):
            return Review.objects.all().order_by('-created_at')
        return Review.objects.filter(is_approved=True).order_by('-created_at')

    def _is_admin(self, user):
        if not user.is_authenticated:
            return False
        try:
            return user.is_superuser or user.is_staff or getattr(user.profile, 'is_admin', False)
        except UserProfile.DoesNotExist:
            return user.is_superuser or user.is_staff

    def perform_create(self, serializer):
        # Check if user has completed the reservation
        reservation = serializer.validated_data['reservation']
        if reservation.user != self.request.user:
            raise serializers.ValidationError("You can only review your own reservations")
        
        if reservation.status != 'completed':
            raise serializers.ValidationError("You can only review completed reservations")
        
        # Check if review already exists
        if hasattr(reservation, 'review'):
            raise serializers.ValidationError("You have already reviewed this reservation")
        
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def by_car(self, request):
        """Get reviews for a specific car"""
        car_id = request.query_params.get('car_id')
        if not car_id:
            return Response({'error': 'car_id parameter is required'}, status=400)
        
        queryset = self.get_queryset().filter(car_id=car_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_reviews(self, request):
        """Get current user's reviews"""
        queryset = Review.objects.filter(user=request.user).order_by('-created_at')
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


def _user_is_admin(user) -> bool:
    if not user.is_authenticated:
        return False
    try:
        return user.is_superuser or user.is_staff or getattr(user.profile, 'is_admin', False)
    except UserProfile.DoesNotExist:
        return user.is_superuser or user.is_staff


@login_required
def admin_cars_list(request):
    if not _user_is_admin(request.user):
        return redirect('/')
    cars = Car.objects.all().order_by('-created_at')
    return render(request, 'admin/cars_list.html', {'cars': cars})


@login_required
@require_http_methods(["GET", "POST"])
def admin_car_create(request):
    if not _user_is_admin(request.user):
        return redirect('/')
    form = CarForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('/dashboard/')
    return render(request, 'admin/car_form.html', {'form': form, 'mode': 'create'})


@login_required
@require_http_methods(["GET", "POST"])
def admin_car_update(request, pk: int):
    if not _user_is_admin(request.user):
        return redirect('/')
    car = get_object_or_404(Car, pk=pk)
    form = CarForm(request.POST or None, request.FILES or None, instance=car)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('/dashboard/')
    return render(request, 'admin/car_form.html', {'form': form, 'mode': 'update', 'object': car})


@login_required
@require_http_methods(["POST"])
def admin_car_delete(request, pk: int):
    if not _user_is_admin(request.user):
        return redirect('/')
    car = get_object_or_404(Car, pk=pk)
    car.delete()
    return redirect('/dashboard/')


# Agencies
@login_required
def admin_agencies_list(request):
    if not _user_is_admin(request.user):
        return redirect('/')
    agencies = Agency.objects.all().order_by('-created_at')
    return render(request, 'admin/agencies_list.html', {'agencies': agencies})


@login_required
@require_http_methods(["GET", "POST"])
def admin_agency_create(request):
    if not _user_is_admin(request.user):
        return redirect('/')
    form = AgencyForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('/dashboard/')
    return render(request, 'admin/agency_form.html', {'form': form, 'mode': 'create'})


@login_required
@require_http_methods(["GET", "POST"])
def admin_agency_update(request, pk: int):
    if not _user_is_admin(request.user):
        return redirect('/')
    agency = get_object_or_404(Agency, pk=pk)
    form = AgencyForm(request.POST or None, instance=agency)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('/dashboard/')
    return render(request, 'admin/agency_form.html', {'form': form, 'mode': 'update', 'object': agency})


@login_required
@require_http_methods(["POST"])
def admin_agency_delete(request, pk: int):
    if not _user_is_admin(request.user):
        return redirect('/')
    agency = get_object_or_404(Agency, pk=pk)
    agency.delete()
    return redirect('/dashboard/')


# Services
@login_required
def admin_services_list(request):
    if not _user_is_admin(request.user):
        return redirect('/')
    services = Service.objects.all().order_by('-created_at')
    return render(request, 'admin/services_list.html', {'services': services})


@login_required
@require_http_methods(["GET", "POST"])
def admin_service_create(request):
    if not _user_is_admin(request.user):
        return redirect('/')
    form = ServiceForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('/dashboard/')
    return render(request, 'admin/service_form.html', {'form': form, 'mode': 'create'})


@login_required
@require_http_methods(["GET", "POST"])
def admin_service_update(request, pk: int):
    if not _user_is_admin(request.user):
        return redirect('/')
    service = get_object_or_404(Service, pk=pk)
    form = ServiceForm(request.POST or None, instance=service)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('/dashboard/')
    return render(request, 'admin/service_form.html', {'form': form, 'mode': 'update', 'object': service})


@login_required
@require_http_methods(["POST"])
def admin_service_delete(request, pk: int):
    if not _user_is_admin(request.user):
        return redirect('/')
    service = get_object_or_404(Service, pk=pk)
    service.delete()
    return redirect('/dashboard/')


# Reservations (status only)
@login_required
def admin_reservations_list(request):
    if not _user_is_admin(request.user):
        return redirect('/')
    reservations = Reservation.objects.all().order_by('-created_at')
    return render(request, 'admin/reservations_list.html', {'reservations': reservations})


@login_required
@require_http_methods(["GET", "POST"])
def admin_reservation_update_status(request, pk: int):
    if not _user_is_admin(request.user):
        return redirect('/')
    reservation = get_object_or_404(Reservation, pk=pk)
    form = ReservationStatusForm(request.POST or None, instance=reservation)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('/dashboard/')
    return render(request, 'admin/reservation_status_form.html', {'form': form, 'object': reservation})


# Contacts (admin answers)
@login_required
def admin_contacts_list(request):
    if not _user_is_admin(request.user):
        return redirect('/')
    contacts = Contact.objects.all().order_by('-created_at')
    return render(request, 'admin/contacts_list.html', {'contacts': contacts})


@login_required
@require_http_methods(["GET", "POST"])
def admin_contact_update(request, pk: int):
    if not _user_is_admin(request.user):
        return redirect('/')
    contact = get_object_or_404(Contact, pk=pk)
    form = ContactAdminForm(request.POST or None, instance=contact)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('/dashboard/')
    return render(request, 'admin/contact_form.html', {'form': form, 'object': contact})


# Users
@login_required
def admin_users_list_page(request):
    if not _user_is_admin(request.user):
        return redirect('/')
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'admin/users_list.html', {'users': users})


@login_required
@require_http_methods(["GET", "POST"])
def admin_user_update_page(request, user_id: int):
    if not _user_is_admin(request.user):
        return redirect('/')
    user = get_object_or_404(User, pk=user_id)
    form = UserAdminForm(request.POST or None, user_instance=user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('/dashboard/')
    return render(request, 'admin/user_form.html', {'form': form, 'object': user})


@require_GET
def auth_status(request):
    if request.user.is_authenticated:
        user = request.user
        try:
            role = user.profile.role
        except UserProfile.DoesNotExist:
            role = 'admin' if (user.is_staff or user.is_superuser) else 'client'
        return JsonResponse({
            'authenticated': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser,
                'role': role,
            }
        })
    return JsonResponse({'authenticated': False})

# Payment views
import paypalrestsdk
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Reservation, Payment

# Configure PayPal SDK
paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})

@csrf_exempt
def create_paypal_payment(request):
    """Create a PayPal payment for a reservation"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            reservation_id = data.get('reservation_id')
            
            # Get the reservation
            reservation = get_object_or_404(Reservation, id=reservation_id)
            
            # Check if payment already exists
            if hasattr(reservation, 'payment'):
                return JsonResponse({
                    'success': False,
                    'message': 'Payment already exists for this reservation'
                }, status=400)
            
            # Create PayPal payment using SDK
            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"
                },
                "redirect_urls": {
                    "return_url": f"{request.build_absolute_uri('/payment/success/')}?reservation_id={reservation.id}",
                    "cancel_url": f"{request.build_absolute_uri('/payment/cancel/')}?reservation_id={reservation.id}"
                },
                "transactions": [{
                    "item_list": {
                        "items": [{
                            "name": f"Car Rental - {reservation.car.brand} {reservation.car.model}",
                            "sku": f"car-{reservation.car.id}",
                            "price": str(reservation.total_price),
                            "currency": "EUR",
                            "quantity": 1
                        }]
                    },
                    "amount": {
                        "total": str(reservation.total_price),
                        "currency": "EUR"
                    },
                    "description": f"Car rental reservation #{reservation.id} from {reservation.start_date} to {reservation.end_date}"
                }]
            })
            
            if payment.create():
                # Create payment record in database
                db_payment = Payment.objects.create(
                    reservation=reservation,
                    amount=reservation.total_price,
                    currency='EUR',
                    payment_method='paypal',
                    transaction_id=payment.id,
                    status='pending'
                )
                
                # Get approval URL
                approval_url = None
                for link in payment.links:
                    if link.rel == "approval_url":
                        approval_url = link.href
                        break
                
                return JsonResponse({
                    'success': True,
                    'approval_url': approval_url,
                    'payment_id': db_payment.id,
                    'paypal_payment_id': payment.id
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': f'PayPal payment creation failed: {payment.error}'
                }, status=400)
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def execute_paypal_payment(request):
    """Execute a PayPal payment after user approval"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            paypal_payment_id = data.get('paypal_payment_id')
            payer_id = data.get('payer_id')
            
            # Find PayPal payment
            payment = paypalrestsdk.Payment.find(paypal_payment_id)
            
            if payment.execute({"payer_id": payer_id}):
                # Update database payment record
                try:
                    db_payment = Payment.objects.get(transaction_id=paypal_payment_id)
                    db_payment.status = 'completed'
                    db_payment.save()
                    
                    # Update reservation status
                    reservation = db_payment.reservation
                    old_status = reservation.status
                    reservation.status = 'confirmed'
                    reservation.save()
                    
                    # Send payment confirmation email
                    send_payment_confirmation_email(db_payment)
                    
                    # Send status update email if status changed
                    if old_status != 'confirmed':
                        send_reservation_status_update_email(reservation, old_status, 'confirmed')
                    
                    return JsonResponse({
                        'success': True,
                        'message': 'Payment executed successfully',
                        'reservation_id': reservation.id
                    })
                except Payment.DoesNotExist:
                    return JsonResponse({
                        'success': False,
                        'message': 'Payment record not found in database'
                    }, status=404)
            else:
                return JsonResponse({
                    'success': False,
                    'message': f'PayPal payment execution failed: {payment.error}'
                }, status=400)
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def payment_success(request):
    """Handle successful payment redirect"""
    # In a real implementation, you would verify the payment
    # and update the reservation status
    return render(request, 'payment_success.html')

def payment_cancel(request):
    """Handle cancelled payment redirect"""
    # In a real implementation, you would handle the cancellation
    # and possibly allow the user to try again
    return render(request, 'payment_cancel.html')
