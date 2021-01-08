from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserModel


@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        UserModel.objects.create(user=instance)

