from django.shortcuts import render, redirect, get_object_or_404

# models
from .models import Project

# forms
from .forms import ProjectForm


# Create your views here.
def projects(request):
    template_name = "projects/projects.html"
    projects = Project.objects.all().order_by("-created")
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


def create_project(request):
    template_name = "projects/project_form.html"
    form = ProjectForm()

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("projects:projects")

    context = {
        "form": form
    }

    return render(request, template_name, context)


def update_project(request, pk):
    template_name = "projects/project_form.html"
    project = get_object_or_404(Project, id=pk)
    form = ProjectForm(instance=project)

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect("projects:projects")

    context = {
        "form": form
    }

    return render(request, template_name, context)


def delete_project(request, pk):
    template_name = "projects/delete_template.html"
    project = get_object_or_404(Project, id=pk)

    if request.method == "POST":
        project.delete()
        return redirect("projects:projects")

    context = {
        "object": project
    }

    return render(request, template_name, context)
