from .models import Notification
def notification(request):
    a=Notification.objects.filter(is_read=False).count()
    return {'aaa':a} 