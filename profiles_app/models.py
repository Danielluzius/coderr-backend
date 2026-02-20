from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """Extends the default Django User with profile information."""

    CUSTOMER = 'customer'
    BUSINESS = 'business'
    USER_TYPE_CHOICES = [
        (CUSTOMER, 'Customer'),
        (BUSINESS, 'Business'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    file = models.FileField(upload_to='profile_pictures/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, default='')
    tel = models.CharField(max_length=50, blank=True, default='')
    description = models.TextField(blank=True, default='')
    working_hours = models.CharField(max_length=100, blank=True, default='')
    type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default=CUSTOMER)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        ordering = ['user__username']

    def __str__(self):
        return f'{self.user.username} ({self.type})'
