from django.utils import timezone
from django.contrib.sessions.models import Session


def delete_all_unexpired_sessions_for_user(user):
    unexpired_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    [
        session.delete() for session in unexpired_sessions
        if str(user.pk) == session.get_decoded().get('_auth_user_id')
    ]