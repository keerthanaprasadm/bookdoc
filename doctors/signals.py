from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User
from .models import DoctorProfile

@receiver(post_save, sender=User)
def create_doctor_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'doctor':
        DoctorProfile.objects.create(user=instance)
