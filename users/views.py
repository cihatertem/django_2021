from django.shortcuts import render, get_list_or_404, get_object_or_404
from .models import Profile


# Create your views here.
def profiles(request):
    template = "users/profiles.html"
    profiles = get_list_or_404(Profile)
    context = {
        "profiles": profiles
    }
    return render(request, template, context)


def user_profile(request, pk):
    template = "users/user_profile.html"
    profile = get_object_or_404(Profile, id=pk)
    top_skills = profile.skill_set.exclude(description__exact="")
    other_skills = profile.skill_set.filter(description="")
    context = {
        "profile": profile,
        "topSkills": top_skills,
        "otherSkills": other_skills
    }
    return render(request, template, context)
