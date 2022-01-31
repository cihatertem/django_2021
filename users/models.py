from django.db import models
from django.contrib.auth.models import User
import uuid


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=200, blank=True, null=True, unique=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=500, blank=True, null=True, unique=True)
    short_intro = models.CharField(max_length=200, null=True, blank=True, verbose_name="Intro")
    bio = models.TextField(blank=True, null=True)
    profile_img = models.ImageField(null=True, blank=True, upload_to="profiles/",
                                    default="profiles/user-default.png", verbose_name="Avatar")
    social_github = models.URLField(max_length=200, null=True, blank=True, verbose_name="Github",
                                    help_text="https://github.com/USERNAME")
    social_twitter = models.URLField(max_length=200, null=True, blank=True,
                                     verbose_name="Twitter", help_text="https://twitter.com/USERNAME")
    social_facebook = models.URLField(max_length=200, null=True, blank=True, verbose_name="Facebook",
                                      help_text="https://facebook.com/YOUR.NAME.1234")
    social_linkedin = models.URLField(max_length=200, null=True, blank=True, verbose_name="Linkedin",

                                      help_text="https://tr.linkedin.com/in/USERNAME-1234")
    social_youtube = models.URLField(max_length=200, null=True, blank=True, verbose_name="Youtube Channel",
                                     help_text="https://www.youtube.com/c/YOURCHANNELNAME")
    social_website = models.URLField(max_length=200, null=True, blank=True, verbose_name="Personal Website")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)


    class Meta:
        ordering = ("-created",)


    def __str__(self):
        return str(self.username)

    @property
    def image_url(self):
        try:
            url = self.profile_img.url
        except:
            url = ""
        return url


class Skill(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.name[:10])


class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.subject


    class Meta:
        ordering = ["is_read", "-created"]
