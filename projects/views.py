from django.shortcuts import render
from django.http import HttpResponse

projectsList = [
    {
        'id': '1',
        'title': 'Ecommerce Website',
        'description': 'Fully functional ecommerce website',
        "topRated": True
    },
    {
        'id': '2',
        'title': 'Portfolio Website',
        'description': 'A personal website to write articles and display work',
        "topRated": False
    },
    {
        'id': '3',
        'title': 'Social Network',
        'description': 'An open source project built by the community',
        "topRated": True
    }
]


# Create your views here.
def projects(request):
    template_name = "projects/projects.html"
    context = {
        "projects": projectsList
    }
    return render(request, template_name, context)


def project(request, pk):
    template_name = "projects/project.html"
    project_object = None
    for i in projectsList:
        if i["id"] == str(pk):
            project_object = i
    context = {
        "pk": pk,
        "project": project_object
    }
    return render(request, template_name, context)
