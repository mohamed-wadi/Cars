from django import forms
from django.contrib.auth.models import User
from .models import Car, Agency, Service, Reservation, Contact, UserProfile


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            'brand', 'model', 'price_per_day', 'image', 'description', 'available',
            'year', 'mileage', 'fuel_type', 'transmission', 'seats'
        ]


class AgencyForm(forms.ModelForm):
    class Meta:
        model = Agency
        fields = ['name', 'address', 'city', 'country', 'phone', 'email', 'opening_hours']


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'price', 'is_active']


class ReservationStatusForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['status', 'notes']


class ContactAdminForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['status', 'admin_response']


class UserAdminForm(forms.Form):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    is_active = forms.BooleanField(required=False)
    is_staff = forms.BooleanField(required=False)
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES)

    def __init__(self, *args, **kwargs):
        self.user_instance: User = kwargs.pop('user_instance', None)
        super().__init__(*args, **kwargs)
        if self.user_instance is not None:
            self.fields['first_name'].initial = self.user_instance.first_name
            self.fields['last_name'].initial = self.user_instance.last_name
            self.fields['email'].initial = self.user_instance.email
            self.fields['is_active'].initial = self.user_instance.is_active
            self.fields['is_staff'].initial = self.user_instance.is_staff
            try:
                self.fields['role'].initial = self.user_instance.profile.role
            except UserProfile.DoesNotExist:
                self.fields['role'].initial = 'client'

    def save(self):
        user = self.user_instance
        user.first_name = self.cleaned_data.get('first_name', user.first_name)
        user.last_name = self.cleaned_data.get('last_name', user.last_name)
        user.email = self.cleaned_data.get('email', user.email)
        user.is_active = bool(self.cleaned_data.get('is_active'))
        user.is_staff = bool(self.cleaned_data.get('is_staff'))
        user.save()
        role = self.cleaned_data.get('role')
        try:
            profile = user.profile
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=user, role='client')
        profile.role = role
        profile.save()
        return user 