# facilities/admin.py
from django.contrib import admin
from .models import CustomUser, UserProfile


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_approved', 'role',
                    'is_active', 'registration_number')
    actions = ['approve_users', 'disapprove_users']

    list_filter = ('role', 'is_approved')

    def approve_users(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, "Selected users have been approved.")

    def disapprove_users(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, "Selected users have been disapproved.")

    approve_users.short_description = "Approve selected users"
    disapprove_users.short_description = "Disapprove selected users"


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'date_of_birth',
                    'phone', 'county', "blood_group", "gender")


# Register the custom user admin class
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
