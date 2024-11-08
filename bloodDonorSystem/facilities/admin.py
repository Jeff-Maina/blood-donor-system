# # facilities/admin.py
from django.contrib import admin
# from users.models import CustomUser  

# class FacilitiesAdmin(admin.ModelAdmin):
#     list_display = ('email', 'is_approved', 'role', 'is_active','facility_name', 'registration_number')
#     actions = ['approve_users', 'disapprove_users']

#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         return qs.filter(role='facility')  

#     def approve_users(self, request, queryset):
#         queryset.update(is_approved=True)
#         self.message_user(request, "Selected users have been approved.")

#     def disapprove_users(self, request, queryset):
#         queryset.update(is_approved=False)
#         self.message_user(request, "Selected users have been disapproved.")

#     approve_users.short_description = "Approve selected users"
#     disapprove_users.short_description = "Disapprove selected users"

# admin.site.register(CustomUser, FacilitiesAdmin)