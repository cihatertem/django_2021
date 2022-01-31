from django.db import models
import uuid
from users.models import Profile


# Create your models here.
class Project(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    featured_img = models.ImageField(null=True, blank=True, default="default.jpg", verbose_name="Featured Image")
    demo_link = models.URLField(max_length=2000, null=True, blank=True, verbose_name="Demo Link")
    source_link = models.URLField(max_length=2000, null=True, blank=True, verbose_name="Source Link")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField("Tag", blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        if len(self.title) < 25:
            return self.title
        else:
            return f"{self.title[:25]}..."


    class Meta:
        ordering = ["-vote_ratio", "-vote_total", "title"]


    @property
    def image_url(self):
        try:
            url = self.featured_img.url
        except:
            url = ""
        return url

    @property
    def reviewers(self):
        query_set = self.review_set.all().values_list("owner__id", flat=True)
        return query_set

    @property
    def get_vote_count(self):
        reviews = self.review_set.all()
        up_votes = reviews.filter(value="up").count()
        total_votes = reviews.count()
        ratio = (up_votes / total_votes) * 100
        self.vote_total = total_votes
        self.vote_ratio = ratio
        self.save()


class Review(models.Model):
    VOTE_TYPE = (
        ("up", "Up Vote"),
        ("down", "Down Vote"),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)


    class Meta:
        unique_together = [["owner", "project"]]


    def __str__(self):
        if len(self.value) < 25:
            return self.value
        else:
            return f"{self.value[:25]}..."


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        if len(self.name) < 25:
            return self.name
        else:
            return f"{self.name[:25]}..."
