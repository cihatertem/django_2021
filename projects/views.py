from django.shortcuts import render
from django.http import HttpResponse
from .models import Project


# Create your views here.
def projects(request):
    template_name = "projects/projects.html"
    projects = Project.objects.all()
    context = {
        "projects": projects
    }
    return render(request, template_name, context)


def project(request, pk):
    template_name = "projects/project.html"
    project_object = Project.objects.get(id=pk)
    tags = project_object.tags.all()

    context = {
        "project": project_object,
        "tags": tags
    }
    return render(request, template_name, context)
