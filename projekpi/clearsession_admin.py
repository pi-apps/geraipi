from django.contrib.sessions.models import Session
from django.utils import timezone


def delete_all_unexpired_sessions_for_user(user):
    unexpired_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    [session.delete() for session in unexpired_sessions if str(user.pk) == session.get_decoded().get("_auth_user_id")]
