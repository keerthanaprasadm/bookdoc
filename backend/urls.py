from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('accounts.urls')),          # login / signup / home
    path('doctors/', include('doctors.urls')),  # doctor module
    path('appointments/', include('appointments.urls')),
]
