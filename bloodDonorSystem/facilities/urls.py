from django.urls import path
from .views import dashboard_view, register_facility, awaiting_approval

urlpatterns = [
    path("dashboard/", view=dashboard_view, name='facility-dashboard'),
    path("register/", view=register_facility, name='register-facility'),
    path("awaiting-approval/", view=awaiting_approval, name='awaiting-approval')
]
