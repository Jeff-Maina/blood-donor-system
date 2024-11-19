from users.models import Notification, Donation, UserProfile
from users.filters import DonationFilter, RequestsFilter
from users.tables import DonationTable, RequestsTable
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.timesince import timesince


def notification_processor(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(
            user=request.user
        ).order_by('read', '-created_at')

        formatted_notifications = []

        for notification in notifications:
            time_diff = timesince(notification.created_at, timezone.now())

            time_diff_parts = time_diff.split(",")

            formatted_notifications.append({
                'notification': notification,
                'time_ago': time_diff_parts[0].strip() 
            })

            unread_notifications = notifications.filter(read=False).count()
    else:
        notifications = []
        unread_notifications = 0

    return {
        'notifications': formatted_notifications,
        'unread_notifications': unread_notifications
    }


def donations_filter_processor(request):
    user = request.user
    if user.is_authenticated and user.role == 'individual':
        profile = UserProfile.objects.filter(user=user).first()
        donations = profile.donations.all()
        filter = DonationFilter(request.GET, queryset=donations)
        filtered_donations = filter.qs
        table = DonationTable(filtered_donations)
        return {
            'donations_filter': filter,
            'donations_table': table,
        }
    else:
        return {}


def requests_filter_processor(request):
    user = request.user
    if user.is_authenticated and user.role == 'individual':
        profile = UserProfile.objects.filter(user=user).first()
        requests = profile.requests.all()
        filter = RequestsFilter(request.GET, queryset=requests)
        filtered_requests = filter.qs
        table = RequestsTable(filtered_requests)
        return {
            'requests_filter': filter,
            'requests_table': table,
        }
    else:
        return {}
