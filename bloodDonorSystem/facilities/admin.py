# # facilities/admin.py
from django.contrib import admin
from .models import FacilityProfile


class FacilitiesAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_number', 'facility_type',
                    'county', "open_days", "opening_time", "closing_time", "user_email", "is_superuser", "profile_completed", "registration_number")

    list_filter = ['facility_type', 'county']

    def registration_number(self, obj):
        return obj.user.registration_number if obj.user else "N/A"

    def user_email(self, obj):
        return obj.user.email if obj.user else "N/A"

    @admin.display(boolean=True)
    def is_superuser(self, obj):
        return obj.user.is_superuser if obj.user else "N/A"

    @admin.display(boolean=True)
    def profile_completed(self, obj):
        return obj.user.profile_completed if obj.user else "N/A"


admin.site.register(FacilityProfile, FacilitiesAdmin)