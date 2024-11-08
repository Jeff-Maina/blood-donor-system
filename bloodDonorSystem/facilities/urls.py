from django.urls import path
from .views import dashboard_view, register_facility

urlpatterns = [
    path("dashboard/", view=dashboard_view, name='facility-dashboard'),
    path("register/", view=register_facility, name='register-facility')
]
