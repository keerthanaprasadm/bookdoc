from django.urls import path
from .views import doctor_list, doctor_detail,doctor_profile_details

urlpatterns = [
    path('doctors/', doctor_list, name='doctor_list'),
    path('doctors/<int:doctor_id>/', doctor_detail, name='doctor_detail'),
     path("profile-details/",doctor_profile_details,name="doctor_profile_details"
    ),
]
