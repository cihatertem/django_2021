from django.shortcuts import render, redirect, get_object_or_404
# Django Auth.
from django.contrib.auth.decorators import login_required
# Django messages
from django.contrib import messages
# models
from .models import Project, Tag
# app imports
from .forms import ProjectForm, ReviewForm
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
    project_object = get_object_or_404(Project, id=pk)
    tags = project_object.tags.all()
    form = ReviewForm()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.project = project_object
            review.owner = request.user.profile
            review.save()
            project_object.get_vote_count
            messages.success(request, "Your review was successfully submited.")

            return redirect("projects:project", pk=project_object.id)

    context = {
        "project": project_object,
        "tags": tags,
        "form": form,
    }
    return render(request, template_name, context)


@login_required(login_url="users:login")
def create_project(request):
    profile = request.user.profile
    template_name = "projects/project_form.html"
    form = ProjectForm()

    if request.method == "POST":
        new_tags = request.POST.get("newtags").replace(',', " ").split(" ")
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            for tag in new_tags:
                if tag != "":
                    tag, created = Tag.objects.get_or_create(
                        name=tag
                    )
                    project.tags.add(tag)
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
        new_tags = request.POST.get("newtags").replace(',', " ").split(" ")
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for tag in new_tags:
                if tag != "":
                    tag, created = Tag.objects.get_or_create(
                        name=tag
                    )
                    project.tags.add(tag)

            return redirect("users:account")

    context = {
        "form": form,
        "project": project
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
