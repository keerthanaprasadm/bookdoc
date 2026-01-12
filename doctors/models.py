from django.conf import settings
from django.db import models
from django.db.models import Avg
from accounts.models import User


User = settings.AUTH_USER_MODEL


class Specialization(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    specialization = models.CharField(max_length=100, blank=True)
    experience_years = models.IntegerField(null=True, blank=True)
    bio = models.TextField(blank=True)
    consultation_fee = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True
    )

    def average_rating(self):
        avg = self.ratings.aggregate(avg=Avg('rating'))['avg']
        return avg or 0

    def __str__(self):
        return self.user.username



class Availability(models.Model):
    doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.CASCADE,
        related_name='availabilities'
    )
    day_of_week = models.IntegerField(
        choices=[
            (0, 'Monday'),
            (1, 'Tuesday'),
            (2, 'Wednesday'),
            (3, 'Thursday'),
            (4, 'Friday'),
            (5, 'Saturday'),
            (6, 'Sunday'),
        ]
    )
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.doctor.user.email} - {self.get_day_of_week_display()}"
