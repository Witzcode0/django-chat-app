from django.urls import path
from .views import *

urlpatterns = [
    path("", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("profile/", profile_view, name="profile"),
    path("logout/", logout_view, name="logout"),
]
