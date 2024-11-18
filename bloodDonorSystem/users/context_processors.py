from users.models import Notification, Donation, UserProfile
from users.filters import DonationFilter
from users.tables import DonationTable
from django.contrib.auth.decorators import login_required


def notification_processor(request):
    if request.user.is_authenticated:

        notifications = Notification.objects.filter(
            user=request.user
        ).order_by('read', '-created_at')

        unread_notifications = notifications.filter(read=False)
    else:
        notifications = []

    return {
        'notifications': notifications,
        'unread_notifications': unread_notifications.count()
    }


def donations_filter_processor(request):
    user = request.user
    profile = UserProfile.objects.filter(user=user).first()
    if user.is_authenticated:
        donations = profile.donations.all()
        filter = DonationFilter(request.GET, queryset=donations)
        filtered_donations = filter.qs
        table = DonationTable(filtered_donations)
        return {
            'filter': filter,
            'table': table,
        }
