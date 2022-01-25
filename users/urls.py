from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("", views.profiles, name="profiles"),
    path("profile/<str:pk>/", views.user_profile, name="user_profile"),
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_user, name="logut"),
    path("register/", views.register_user, name="register"),
    path("account/", views.user_account, name="account"),
    path("edit-account/", views.edit_account, name="edit_account"),
    path("create-skill/", views.create_skill, name="create_skill"),
    path("update-skill/<str:pk>/", views.update_skill, name="update_skill"),
    path("delete-skill/<str:pk>/", views.delete_skill, name="delete_skill"),
    path("inbox/", views.inbox, name="inbox"),
    path("inbox/message/<str:pk>/", views.view_message, name="message"),
    path("send-message/<str:pk>/", views.create_message, name="create_message"),
]
