from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Avg

class User(AbstractUser):
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        # ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)



def average_rating(self):
    return self.ratings.aggregate(avg=Avg('rating'))['avg'] or 0
