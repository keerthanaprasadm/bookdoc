from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_appointments, name='my_appointments'),
    path('book/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
    path('doctor/', views.doctor_appointments, name='doctor_appointments'), 
     path('confirm/<int:appt_id>/', views.confirm_appointment, name='confirm_appointment'),
    path('cancel/<int:appt_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('slots/<int:doctor_id>/', views.get_available_slots, name='get_available_slots'),
    path('success/<int:appointment_id>/', views.appointment_success, name='appointment_success'),
    path('rate-doctor/<int:appointment_id>/', views.rate_doctor, name='rate_doctor'),

]

