from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Review(models.Model):
    """Represents a rating and review left by a customer for a business user."""

    business_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['-updated_at']
        constraints = [
            models.UniqueConstraint(fields=['business_user', 'reviewer'], name='unique_review_per_business')
        ]

    def __str__(self):
        return f'Review by {self.reviewer.username} for {self.business_user.username} ({self.rating}*)'
