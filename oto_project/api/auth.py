from django.http import JsonResponse

from api.models import Token


def permission_check(request, role=None):
    """Permission checker."""
    data = {
        'message': 'Not Authorized'
    }
    if not request.headers.get('token'):
        print('I am here')
        return JsonResponse(data, status=403)
    try:
        print('I am here with token')
        token_obj = Token.objects.get(uuid=request.headers.get('token'))
        user_obj = token_obj.user
        if user_obj and not role:
            return True
        user_groups = ', '.join(map(str, user_obj.groups.all()))
        if role in user_groups:
            return True
        else:
            return JsonResponse(data, status=403)
    except Exception:
        return JsonResponse(data, status=403)
