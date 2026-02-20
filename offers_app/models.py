from django.contrib.auth.models import User
from django.db import models


class Offer(models.Model):
    """Represents a service offer created by a business user."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offers')
    title = models.CharField(max_length=200)
    image = models.FileField(upload_to='offer_images/', blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Offer'
        verbose_name_plural = 'Offers'
        ordering = ['-updated_at']

    def __str__(self):
        return f'{self.title} (by {self.user.username})'


class OfferDetail(models.Model):
    """Represents one of the three pricing tiers of an offer (basic, standard, premium)."""

    BASIC = 'basic'
    STANDARD = 'standard'
    PREMIUM = 'premium'
    OFFER_TYPE_CHOICES = [
        (BASIC, 'Basic'),
        (STANDARD, 'Standard'),
        (PREMIUM, 'Premium'),
    ]

    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='details')
    title = models.CharField(max_length=200)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=10, choices=OFFER_TYPE_CHOICES)

    class Meta:
        verbose_name = 'Offer Detail'
        verbose_name_plural = 'Offer Details'
        ordering = ['offer', 'offer_type']

    def __str__(self):
        return f'{self.offer.title} – {self.offer_type}'
