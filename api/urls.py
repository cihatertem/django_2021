from . import views
from django.urls import path
# RestFrameWork Simple JWT
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = "api"

urlpatterns = [
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("", views.get_routes, name="route_demo"),
    path("projects/", views.get_projects, name="get_projects"),
    path("projects/<str:pk>/", views.get_project, name="get_project"),
    path("projects/<str:pk>/vote/", views.project_vote, name="project_vote"),
]
