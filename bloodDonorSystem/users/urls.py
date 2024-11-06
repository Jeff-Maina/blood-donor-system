from django.urls import path
from . import views


urlpatterns = [
    path("", views.home_view, name="dashboard"),
    path("register/", views.register_user, name="register")
]
