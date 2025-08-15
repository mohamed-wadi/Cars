from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CarViewSet, ServiceViewSet, ReservationViewSet, main_page, AgencyViewSet, contact_page, login_page, profile_page, dashboard_page, auth_login, auth_register, auth_logout, admin_users, contact_submit, ContactViewSet, admin_user_detail, terms_page, faq_page, about_page, ReviewViewSet
from .views import (
    admin_cars_list, admin_car_create, admin_car_update, admin_car_delete,
    admin_agencies_list, admin_agency_create, admin_agency_update, admin_agency_delete,
    admin_services_list, admin_service_create, admin_service_update, admin_service_delete,
    admin_reservations_list, admin_reservation_update_status,
    admin_contacts_list, admin_contact_update,
    admin_users_list_page, admin_user_update_page,
)
from .views import auth_status, create_paypal_payment, execute_paypal_payment, payment_success, payment_cancel

router = DefaultRouter()
router.register(r'cars', CarViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'reservations', ReservationViewSet, basename='reservation')
router.register(r'agencies', AgencyViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('', main_page, name='main_page'),
    path('contact/', contact_page, name='contact'),
    path('login/', login_page, name='login'),
    path('profile/', profile_page, name='profile'),
    path('dashboard/', dashboard_page, name='dashboard'),
    path('terms/', terms_page, name='terms'),
    path('faq/', faq_page, name='faq'),
    path('about/', about_page, name='about'),

    # Pages de gestion (éviter le conflit avec Django admin)
    path('manage/cars/', admin_cars_list, name='admin_cars_list'),
    path('manage/cars/create/', admin_car_create, name='admin_car_create'),
    path('manage/cars/<int:pk>/edit/', admin_car_update, name='admin_car_update'),
    path('manage/cars/<int:pk>/delete/', admin_car_delete, name='admin_car_delete'),

    path('manage/agencies/', admin_agencies_list, name='admin_agencies_list'),
    path('manage/agencies/create/', admin_agency_create, name='admin_agency_create'),
    path('manage/agencies/<int:pk>/edit/', admin_agency_update, name='admin_agency_update'),
    path('manage/agencies/<int:pk>/delete/', admin_agency_delete, name='admin_agency_delete'),

    path('manage/services/', admin_services_list, name='admin_services_list'),
    path('manage/services/create/', admin_service_create, name='admin_service_create'),
    path('manage/services/<int:pk>/edit/', admin_service_update, name='admin_service_update'),
    path('manage/services/<int:pk>/delete/', admin_service_delete, name='admin_service_delete'),

    path('manage/reservations/', admin_reservations_list, name='admin_reservations_list'),
    path('manage/reservations/<int:pk>/status/', admin_reservation_update_status, name='admin_reservation_update_status'),

    path('manage/contacts/', admin_contacts_list, name='admin_contacts_list'),
    path('manage/contacts/<int:pk>/edit/', admin_contact_update, name='admin_contact_update'),

    path('manage/users/', admin_users_list_page, name='admin_users_list_page'),
    path('manage/users/<int:user_id>/edit/', admin_user_update_page, name='admin_user_update_page'),

    path('api/', include(router.urls)),
    path('api/auth/login/', auth_login, name='auth_login'),
    path('api/auth/register/', auth_register, name='auth_register'),
    path('api/auth/logout/', auth_logout, name='auth_logout'),
    path('api/auth/status/', auth_status, name='auth_status'),
    path('api/admin/users/', admin_users, name='admin_users'),
    path('api/admin/users/<int:user_id>/', admin_user_detail, name='admin_user_detail'),
    path('api/contact/submit/', contact_submit, name='contact_submit'),
    path('api/payment/create/', create_paypal_payment, name='create_paypal_payment'),
    path('api/payment/execute/', execute_paypal_payment, name='execute_paypal_payment'),
    path('payment/success/', payment_success, name='payment_success'),
    path('payment/cancel/', payment_cancel, name='payment_cancel'),
]