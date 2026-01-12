from django import forms
from .models import Appointment
from django import forms
from .models import DoctorRating 

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'time']
        widgets = {
            'date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'time': forms.TimeInput(
                attrs={'type': 'time', 'class': 'form-control'}
            ),
        }


class DoctorRatingForm(forms.ModelForm):
    class Meta:
        model = DoctorRating
        fields = ['rating', 'review']
        widgets = {
            'rating': forms.RadioSelect(
                choices=[(i, i) for i in range(1, 6)]
            ),
            'review': forms.Textarea(attrs={'rows': 3})
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if not rating:
            raise forms.ValidationError("Please select a rating.")
        if rating < 1 or rating > 5:
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating