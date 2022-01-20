from django.shortcuts import render, redirect
# Django Auth.
from django.contrib.auth.decorators import login_required
# Django messages
from django.contrib import messages
# models
from .models import Project
# app imports
from .forms import ProjectForm
from .utils import search_projects, pagination_projects


# Create your views here.
def projects(request):
    template_name = "projects/projects.html"
    search_query, projects = search_projects(request)
    custom_range, projects = pagination_projects(request, projects, 6)

    context = {
        "projects": projects,
        "search_query": search_query,
        "custom_range": custom_range
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


@login_required(login_url="users:login")
def create_project(request):
    profile = request.user.profile
    template_name = "projects/project_form.html"
    form = ProjectForm()

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect("users:account")

    context = {
        "form": form
    }

    return render(request, template_name, context)


@login_required(login_url="users:login")
def update_project(request, pk):
    profile = request.user.profile
    template_name = "projects/project_form.html"

    try:
        project = profile.project_set.get(id=pk)
    except:
        messages.error(request, "This project does not belongs to you!")
        return redirect("users:profiles")

    form = ProjectForm(instance=project)

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect("users:account")

    context = {
        "form": form
    }

    return render(request, template_name, context)


@login_required(login_url="users:login")
def delete_project(request, pk):
    profile = request.user.profile
    template_name = "projects/delete_template.html"

    try:
        project = profile.project_set.get(id=pk)
    except:
        messages.error(request, "This project does not belongs to you!")
        return redirect("users:profiles")

    if request.method == "POST":
        project.delete()
        return redirect("users:account")

    context = {
        "object": project
    }

    return render(request, template_name, context)
