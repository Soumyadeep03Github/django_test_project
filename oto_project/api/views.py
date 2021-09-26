"""Views file for API app."""
import json 
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from api.auth import permission_check
from api.handlers.movie_handler import MovieHandlers
from api.models import Token


@method_decorator(csrf_exempt, name='dispatch')
class MovieView(View):
    """Class view for list of all movies."""

    def get(self, request, movie_uuid=None):
        """Get the list of all movies."""
        if not permission_check(request):
            return access_denied()
        if movie_uuid:
            response = MovieHandlers().get_details_of_movie(
                movie_uuid)
        else:
            response = MovieHandlers().get_list_of_all_movies()
        return JsonResponse(response, safe=False)

    def post(self, request):
        """Add an new movie into the collection."""
        if not permission_check(request, role='SuperUser'):
            return access_denied()
        response = MovieHandlers().add_new_movie_in_collection(
            json.loads(request.body.decode()))
        return JsonResponse(response, safe=False)

    def put(self, request, movie_uuid):
        """Update an movie information of the collection"""
        if not permission_check(request, role='SuperUser'):
            return access_denied()
        response = MovieHandlers().update_a_movie_data(
            movie_uuid, json.loads(request.body.decode()))
        return JsonResponse(response, safe=False)

    def delete(self, request, movie_uuid):
        """Class view for deleting a movie from our collection."""
        if not permission_check(request, role='SuperUser'):
            return access_denied()
        response = MovieHandlers().remove_movie(
            movie_uuid)
        return JsonResponse(response, safe=False)

def access_denied():
    """Access denied."""
    data = {
        'message': 'Not Authorized'
    }
    return JsonResponse(data, status=403)


@method_decorator(csrf_exempt, name='dispatch')
class UserLoginView(View):
    """View class for user login."""

    def post(self, request):
        """Login the user."""
        data = json.loads(request.body.decode())
        user = authenticate(
            request,
            username=data.get('username'),
            password=data.get('password'))
        if user:
            token_obj = Token.objects.get_or_create(user=user)
            response = {
                'token': token_obj[0].token
            }
            return JsonResponse(response)
        response = {
            'message': 'Invalid Credential.'
        }
        return JsonResponse(response, status=401)
