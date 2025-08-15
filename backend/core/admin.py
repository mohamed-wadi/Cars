from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Car, Service, Reservation, Agency, UserProfile, Contact

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_role', 'is_staff', 'is_active')
    list_filter = ('profile__role', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    
    def get_role(self, obj):
        return obj.profile.role if hasattr(obj, 'profile') else 'N/A'
    get_role.short_description = 'Rôle'

class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'price_per_day', 'year', 'fuel_type', 'available', 'created_at')
    list_filter = ('brand', 'fuel_type', 'transmission', 'available', 'year')
    search_fields = ('brand', 'model', 'description')
    list_editable = ('price_per_day', 'available')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Informations générales', {
            'fields': ('brand', 'model', 'description', 'year')
        }),
        ('Caractéristiques', {
            'fields': ('fuel_type', 'transmission', 'seats', 'mileage')
        }),
        ('Prix et disponibilité', {
            'fields': ('price_per_day', 'available')
        }),
        ('Image', {
            'fields': ('image',)
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

class AgencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'country', 'phone', 'email', 'created_at')
    list_filter = ('city', 'country')
    search_fields = ('name', 'city', 'address')
    readonly_fields = ('created_at', 'updated_at')

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    list_editable = ('price', 'is_active')
    readonly_fields = ('created_at', 'updated_at')

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'car', 'start_date', 'end_date', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'start_date', 'end_date', 'agency_start', 'agency_end')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'car__brand', 'car__model')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('services',)
    
    fieldsets = (
        ('Client et véhicule', {
            'fields': ('user', 'car')
        }),
        ('Agences', {
            'fields': ('agency_start', 'agency_end')
        }),
        ('Dates et heures', {
            'fields': ('start_date', 'start_time', 'end_date', 'end_time')
        }),
        ('Services et options', {
            'fields': ('services', 'promo_code', 'driver_age')
        }),
        ('Prix et statut', {
            'fields': ('total_price', 'status', 'notes')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('status',)
    
    fieldsets = (
        ('Informations du contact', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Message', {
            'fields': ('subject', 'message')
        }),
        ('Gestion', {
            'fields': ('status', 'admin_response')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if 'admin_response' in form.changed_data and obj.admin_response:
            obj.status = 'resolved'
        super().save_model(request, obj, form, change)

# Enregistrer les modèles avec les admins personnalisés
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Agency, AgencyAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Contact, ContactAdmin)
