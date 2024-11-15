from users.models import Notification  
from django.contrib.auth.decorators import login_required

def notification_processor(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    else:
        notifications = []

    return {
        'notifications': notifications,
    }