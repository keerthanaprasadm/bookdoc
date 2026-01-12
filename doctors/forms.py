from django import forms
from .models import DoctorProfile
from accounts.models import User

class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        fields = ['specialization', 'experience_years', 'consultation_fee', 'bio']


class DoctorUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
