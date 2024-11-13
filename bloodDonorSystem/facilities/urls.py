from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", view=views.dashboard_view, name='facility-dashboard'),
    path("register/", view=views.register_facility, name='register-facility'),
    path("awaiting-approval/", view=views.awaiting_approval, name='awaiting-approval'),
    path("complete-profile/", view=views.complete_profile,
         name='complete-facility-profile'),
    path("requests", view=views.requests_view, name='facility-requests'),
    path('requests/approve-request/<int:id>/',view = views.approve_request, name='approve-request'),
    path('requests/reject-request/<int:id>/',view = views.reject_request, name='reject-request'),
]
