from django.urls import path
from . import views


urlpatterns = [
    path("", views.home_view, name="user-dashboard"),
    path("register/", views.register_user, name="register"),
    path("complete-profile/", views.complete_profile, name="complete-profile"),
    path("dashboard/", views.dashboard_view, name='user-dashboard')
]
