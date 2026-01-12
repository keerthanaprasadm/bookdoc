from django.contrib import admin
from .models import DoctorProfile, Specialization, Availability

admin.site.register(DoctorProfile)
admin.site.register(Specialization)
admin.site.register(Availability)
