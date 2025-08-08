from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CarViewSet, ServiceViewSet, ReservationViewSet, main_page, AgencyViewSet, contact_page, login_page, profile_page

router = DefaultRouter()
router.register(r'cars', CarViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'reservations', ReservationViewSet, basename='reservation')
router.register(r'agencies', AgencyViewSet)

urlpatterns = [
    path('', main_page, name='main_page'),
    path('contact/', contact_page, name='contact'),
    path('login/', login_page, name='login'),
    path('profile/', profile_page, name='profile'),
    path('api/', include(router.urls)),
] 