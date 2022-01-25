from django.shortcuts import render, redirect, get_object_or_404
# Django Auth.
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
# Django User Model
from django.contrib.auth.models import User
# Django messages
from django.contrib import messages
from django.utils.safestring import mark_safe
# app imports
from .models import Profile, Message
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from .utils import search_profiles, pagination_profiles


# Create your views here.
def profiles(request):
    template = "users/profiles.html"
    profiles, search_query = search_profiles(request)
    custom_range, profiles = pagination_profiles(request, profiles, 6)

    context = {
        "profiles": profiles,
        "search_query": search_query,
        "custom_range": custom_range
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


def login_page(request):
    page = "login"
    template = "users/login_register.html"

    if request.user.is_authenticated:
        return redirect("users:profiles")

    if request.method == "POST":
        username = request.POST["username"].lower()
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist!")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            profile = user.profile
            # not set_messages; because of related_name, it should be "messages!
            message_requests = profile.messages.all()
            unread_count = message_requests.filter(is_read=False).count()

            if unread_count:
                messages.error(request, mark_safe("<a href='/inbox/'>You have " + f"{unread_count} "
                                                                                  f"unread "
                                                                                  "messages!</a>"))

            return redirect(request.GET["next"] if "next" in request.GET else "users:account")

        else:
            messages.error(request, "Username or password is incorrect!")

    return render(request, template)


def logout_user(request):
    logout(request)
    messages.info(request, "User was logged out.")
    return redirect("users:login")


def register_user(request):
    template = "users/login_register.html"
    page = "register"
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, "User account was created.")
            login(request, user)
            return redirect("users:edit_account")
        else:
            messages.error(request, "An error has occurred during registration!")

    context = {
        "page": page,
        "form": form
    }

    return render(request, template, context)


@login_required(login_url="users:login")
def user_account(request):
    template = "users/account.html"
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    context = {
        "profile": profile,
        "skills": skills,
        "projects": projects
    }

    return render(request, template, context)


@login_required(login_url="users:login")
def edit_account(request):
    template = "users/profile_form.html"
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect("users:account")

    context = {
        "form": form
    }

    return render(request, template, context)


@login_required(login_url="users:login")
def create_skill(request):
    template = "users/skill_form.html"
    profile = request.user.profile
    form = SkillForm()

    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, "You have a new skill!")
            return redirect("users:account")

    context = {
        "form": form
    }

    return render(request, template, context)


@login_required(login_url="users:login")
def update_skill(request, pk):
    template = "users/skill_form.html"
    profile = request.user.profile

    try:
        skill = profile.skill_set.get(id=pk)
    except:
        messages.error(request, "This skill does not belongs to you!")
        return redirect("users:profiles")

    form = SkillForm(instance=skill)

    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "The skill was updated.")
            return redirect("users:account")

    context = {
        "form": form
    }

    return render(request, template, context)


@login_required(login_url="users:login")
def delete_skill(request, pk):
    template = "users/delete_skill.html"
    profile = request.user.profile

    try:
        skill = profile.skill_set.get(id=pk)
    except:
        messages.error(request, "This skill does not belongs to you!")
        return redirect("users:profiles")

    if request.method == "POST":
        skill.delete()
        messages.success(request, "The skill was deleted successfully.")
        return redirect("users:account")

    context = {
        "skill": skill
    }

    return render(request, template, context)


@login_required(login_url="users:login")
def inbox(request):
    template = "users/inbox.html"
    profile = request.user.profile
    # not set_messages; because of related_name, it should be "messages!
    message_requests = profile.messages.all()
    unread_count = message_requests.filter(is_read=False).count()
    context = {
        "message_requests": message_requests,
        "unread_count": unread_count
    }

    return render(request, template, context)


@login_required(login_url="users:login")
def view_message(request, pk):
    template = "users/message.html"
    profile = request.user.profile
    message = profile.messages.get(id=pk)

    if message.is_read == False:
        message.is_read = True
        message.save()

    context = {
        "message": message
    }

    return render(request, template, context)


def create_message(request, pk):
    template = "users/message_form.html"
    recipient = get_object_or_404(Profile, id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email

            message.save()
            messages.success(request, "Your message successfully sent to the developer.")

            return redirect("users:user_profile", pk=recipient.id)

    context = {
        "recipient": recipient,
        "form": form,
    }

    return render(request, template, context)
