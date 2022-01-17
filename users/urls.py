from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("", views.profiles, name="profiles"),
    path("profile/<str:pk>/", views.user_profile, name="user_profile"),
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_user, name="logut"),
    path("register/", views.register_user, name="register"),
]
