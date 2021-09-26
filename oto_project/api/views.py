"""Views file for API app."""
from django.http import JsonResponse
from django.views import View

from api.auth import permission_check
from api.handlers.movie_handler import MovieHandlers


class MovieView(View):
    """Class view for list of all movies."""

    def get(self, request, movie_uuid=None):
        """Get the list of all movies."""
        permission_check(request)
        if movie_uuid:
            response = MovieHandlers().get_details_of_movie(
                movie_uuid)
        else:
            response = MovieHandlers().get_list_of_all_movies()
        return JsonResponse(response, safe=False)

    def post(self, request):
        """Add an new movie into the collection."""
        response = MovieHandlers().add_new_movie_in_collection(
            request.data)
        return JsonResponse(response, safe=False)

    def put(self, request, movie_uuid):
        """Update an movie information of the collection"""
        response = MovieHandlers().update_a_movie_data(
            movie_uuid, request.data)
        return JsonResponse(response, safe=False)

    def delete(self, request, movie_uuid):
        """Class view for deleting a movie from our collection."""
        response = MovieHandlers().remove_movie(
            movie_uuid)
        return JsonResponse(response, safe=False)
