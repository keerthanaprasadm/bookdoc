from django.urls import path
from .views import signup_view, logout_view,home,dashboard_redirect,admin_dashboard,doctor_dashboard,patient_dashboard,edit_doctor_profile,edit_patient_profile
from django.contrib.auth import views as auth_views

urlpatterns = [
     path('', home, name='home'),  
    path('signup/', signup_view, name='signup'),
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='accounts/login.html'),
        name='login'
    ),
    path('logout/', logout_view, name='logout'), 
    path('dashboard/', dashboard_redirect, name='dashboard'),
   path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('doctor/dashboard/', doctor_dashboard, name='doctor_dashboard'),
    path('patient/dashboard/', patient_dashboard, name='patient_dashboard'),
    path('doctor/profile/edit/',edit_doctor_profile, name='edit_doctor_profile'),
    path("patient/profile/edit/",edit_patient_profile, name="edit_patient_profile"),


]
