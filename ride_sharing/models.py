from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Ride(models.Model):
    STATUS_CHOICES = (
        ('REQUESTED', 'Requested'),
        ('STARTED', 'Started'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )

    rider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rides_as_rider')
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rides_as_driver', null=True, blank=True)

    pickup_location = models.JSONField(null=True, blank=True)
    dropoff_location = models.JSONField(null=True, blank=True)
    current_location = models.JSONField(null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='REQUESTED')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
