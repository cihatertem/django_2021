from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, sender=User)
def create_update_profile(sender, instance, created, **kwargs):
    """
    The function creates a linked profile to the user that just created
    or
    updates the linked profile after user table updated.
    """
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=f"{user.first_name} {user.last_name}"
        )
    else:
        user = instance
        profile = Profile.objects.get(user_id=user.id)
        profile.user = user
        profile.username = user.username
        profile.email = user.email
        profile.name = f"{user.first_name} {user.last_name}"
        profile.save()


@receiver(post_delete, sender=Profile)
def delete_user(sender, instance, **kwargs):
    """
    The function deletes the linked user to the profile that has been just deleted.
    """
    user = instance.user
    user.delete()
