# notifications/context_processors.py

from .models import Notification

def unread_notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user, read=False).order_by('-timestamp')
        return {'unread_notifications': notifications}
    return {'unread_notifications': []}
