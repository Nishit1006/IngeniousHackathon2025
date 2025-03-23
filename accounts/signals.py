from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, FarmerProfile

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """Create or update user profile."""
    if created and instance.user_type == 'farmer':
        FarmerProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    """Save user profile."""
    if instance.user_type == 'farmer':
        try:
            if not hasattr(instance, 'farmer_profile'):
                FarmerProfile.objects.create(user=instance)
        except FarmerProfile.DoesNotExist:
            FarmerProfile.objects.create(user=instance) 