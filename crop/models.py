from django.db import models
from django.conf import settings

class CropListing(models.Model):
    UNIT_CHOICES = [
        ('kg', 'Kilograms'),
        ('quintal', 'Quintal'),
        ('ton', 'Ton'),
    ]

    farmer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    crop_name = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    location = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.crop_name} - {self.quantity} {self.unit} by {self.farmer.username}"

    class Meta:
        ordering = ['-created_at'] 