from django.contrib.auth.models import User
from django.db import models

# class UserProfile(models.Model):
#   user = models.OneToOneField(User, on_delete=models.CASCADE)

class Appointment(models.Model):
    user = models.ManyToManyField(User)
    title = models.CharField(max_length=64)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)