from .models import Project, Tag, Review
from django.forms import ModelForm
from django import forms


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        # fields = "__all__"
        fields = ["title", "featured_img", "description", "demo_link", "source_link", "tags"]
        widgets = {
            "tags": forms.CheckboxSelectMultiple(),
        }


    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        # self.fields["title"].widget.attrs.update({"class": "input", "placeholder": "Add title"})
        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input input--text"})


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["value", "body"]
        labels = {
            "value": "Place your vote",
            "body": "Add a comment with your vote"
        }


    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        # self.fields["title"].widget.attrs.update({"class": "input", "placeholder": "Add title"})
        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})
