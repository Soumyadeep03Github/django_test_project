
from api.models import Token


def permission_check(request, role=None):
    """Permission checker."""
    if 'token' not in request.headers:
        return False
    try:
        token_obj = Token.objects.get(token=request.headers['token'])
        user_obj = token_obj.user
        if user_obj and not role:
            return True
        user_groups = ', '.join(map(str, user_obj.groups.all()))
        if role in user_groups:
            return True
        else:
            return False
    except Exception:
        return False
