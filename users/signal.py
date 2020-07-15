from django.db.models.signals import post_save
# when a user is created we want to build a profile
from django.contrib.auth.models import User
# we need a reciver that is a function that gets the signal and performs a task
from django.dispatch import receiver
from .models import Profile


# we want to create a profile for every user that has been created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):

    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
