from django.urls import resolve
from .models import Teacher


def notifications_count(request):
    if request.user.is_authenticated:
        return {'user_notifications_count': request.user.notifications.count()}
    else:
        return {'user_notifications_count': 0}
    
    
def nearby_teachers_processor(request):
    excluded_urls = ['about_us_page']  # Add any other URLs to exclude
    current_url = resolve(request.path_info).url_name

    if current_url in excluded_urls:
        return {}

    if request.user.is_authenticated and hasattr(request.user, 'teacher'):
        user_state = request.user.teacher.state
        if request.user.is_staff:  # Check if the current user is an admin
            nearby_teachers = Teacher.objects.filter(state=user_state).exclude(user=request.user)
        else:
            nearby_teachers = Teacher.objects.filter(state=user_state)
        return {'nearby_teachers': nearby_teachers}
    
    return {}