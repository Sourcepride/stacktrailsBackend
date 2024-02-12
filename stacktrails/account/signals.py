from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import SocialAccount, User, UserProfile


@receiver(post_save, sender=User)
def create_profile(sender, created, instance=None, **kwargs):
    if created and instance.id:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=SocialAccount)
def add_avatar_to_profile(sender, created, instance=None, **kwargs):
    if created and instance.id:
        profile = instance.user.profile
        if profile and instance.avatar and not (profile.avatar or profile.image):
            profile.avatar = instance.avatar
