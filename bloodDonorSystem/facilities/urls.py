from django.urls import path
from .views import dashboard_view, register_facility, awaiting_approval, complete_profile

urlpatterns = [
    path("dashboard/", view=dashboard_view, name='facility-dashboard'),
    path("register/", view=register_facility, name='register-facility'),
    path("awaiting-approval/", view=awaiting_approval, name='awaiting-approval'),
    path("complete-profile/", view=complete_profile, name='complete-facility-profile')
]
