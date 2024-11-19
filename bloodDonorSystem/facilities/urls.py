from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", view=views.dashboard_view, name='facility-dashboard'),
    path("register/", view=views.register_facility, name='register-facility'),
    path("awaiting-approval/", view=views.awaiting_approval,
         name='awaiting-approval'),
    path("complete-profile/", view=views.complete_profile,
         name='complete-facility-profile'),
    path("profile-settings/", views.profile_settings_view,
         name="facility-profile-settings"),
    path("requests", view=views.requests_view, name='facility-requests'),
    path('requests/approve-request/<int:id>/',
         view=views.approve_request, name='approve-request'),
    path('requests/reject-request/<int:id>/',
         view=views.reject_request, name='reject-request'),
    path("donations", view=views.donations_view, name='facility-donations'),
    path('donations/approve-donation/<int:id>/',
         view=views.approve_donation, name='approve-donation'),
    path('donations/reject-donation/<int:id>/',
         view=views.reject_donation, name='reject-donation'),
    path('donations/mark-donation-complete/<int:id>/',
         view=views.mark_donation_complete, name='mark_donation_complete'),
    path("inventory", view=views.inventory_view, name='facility-inventory'),
    path("donors", view=views.donor_management_view,
         name='donors-management'),
    path('donors/<str:user_uuid>/', views.donor_view, name='donor-detail')

]
