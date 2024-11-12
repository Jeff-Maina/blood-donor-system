from django.urls import path
from . import views


urlpatterns = [
    path("register/", views.register_user, name="register"),
    path("complete-profile/", views.complete_profile, name="complete-profile"),
    path("dashboard/", views.dashboard_view, name='user-dashboard'),
    path("donations/", views.donations_view, name='donations'),
    path("requests/", views.requests_view, name='requests'),
    path("donations/check-eligibility/", views.check_eligibility, name="check-eligibility"),
    path("donations/book-donation-appointment/", views.book_appointment, name="book-donation-appointment"),
    path("donations/delete-donation/<int:id>/", views.deleteTask, name='delete-donation'),
]
