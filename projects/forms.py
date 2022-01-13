from .models import Project, Tag, Review
from django.forms import ModelForm


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        # fields = "__all__"
        fields = ("title", "description", "demo_link", "source_link", "tags")
