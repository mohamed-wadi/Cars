from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CarViewSet, ServiceViewSet, ReservationViewSet, main_page, AgencyViewSet, contact_page, login_page, profile_page, dashboard_page, auth_login, auth_register, auth_logout, admin_users

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
    path('dashboard/', dashboard_page, name='dashboard'),
    path('api/', include(router.urls)),
    path('api/auth/login/', auth_login, name='auth_login'),
    path('api/auth/register/', auth_register, name='auth_register'),
    path('api/auth/logout/', auth_logout, name='auth_logout'),
    path('api/admin/users/', admin_users, name='admin_users'),
] 