from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import Profile
from django.conf import settings


@receiver(post_save, sender=User)
def create_update_profile(sender, instance, created, **kwargs):
    """
    The function creates a linked profile to the user that just created
    """
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=f"{user.first_name} {user.last_name}"
        )
        subject = "Welcome to DevSearch!"
        message = "We are glad you are here. Enjoy!"
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False
        )


@receiver(post_save, sender=Profile)
def update_profile(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


@receiver(post_delete, sender=Profile)
def delete_user(sender, instance, **kwargs):
    """
    The function deletes the linked user to the profile that has been just deleted.
    """
    try:
        user = instance.user
        user.delete()
    except:
        pass
