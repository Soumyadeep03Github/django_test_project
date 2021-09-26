"""Movie handler for all business logic"""
from django.db import transaction

from api.models import Director, Genre, Movies


class MovieHandlers():
    """Handler for movies."""

    def init():
        """Initailise the handler class."""

    def get_list_of_all_movies(self):
        """Get list of all movies."""
        output = []
        data = Movies.objects.all().prefetch_related(
            'director', 'genre')
        for each_movie in data:
            output.append(
                {
                    "99popularity": each_movie.popularity,
                    "director": [
                        director_data.director_name for director_data in each_movie.director.all()
                    ],
                    "genre": [
                        genre_data.name for genre_data in each_movie.genre.all()
                    ],
                    "imdb_score": each_movie.imdb_score,
                    "name": each_movie.name
                }
            )
        return output

    def get_details_of_movie(self, movie_id):
        """Get the details of a movie."""
        data = Movies.objects.get(uuid=movie_id)
        output = {
            "id": movie_id,
            "99popularity": data.popularity,
            "director": [
                director.director_name for director in data.director.all()
            ],
            "genre": [
                genre_data.name for genre_data in data.genre.all()
            ],
            "imdb_score": data.imdb_score,
            "name": data.name
        }
        return output

    def add_new_movie_in_collection(self, data: dict):
        """Add a new movie in the collection of movies."""
        request_data = {}
        directors, genres = self.get_or_create_genre_and_director(data)
        application_data = data
        for field in Movies._meta.fields:  # noqa
            if field.name in application_data:
                request_data[field.name] = application_data.get(field.name)
        with transaction.atomic:
            movie_obj = Movies.objects.create(
                **request_data
            )
        movie_uuid = self.add_genre_director(movie_obj, directors, genres)
        return movie_uuid

    def update_a_movie_data(self, movie_id, data: dict):
        """Update data for a movie."""
        request_data = {}
        directors, genres = self.get_or_create_genre_and_director(data)
        application_data = data
        for field in Movies._meta.fields:  # noqa
            if field.name in application_data:
                request_data[field.name] = application_data.get(field.name)
        with transaction.atomic():
            movie_obj = Movies.objects.filter(
                uuid=movie_id).update(**request_data)
        movie_uuid = self.add_genre_director(movie_obj, directors, genres)
        movie_obj.refresh_from_db()
        if movie_obj.like >= 10:
            like_count = movie_obj.like%10
            movie_obj.popularity = movie_obj.popularity + 0.01
            movie_obj.like = like_count
            movie_obj.save()
            movie_obj.refresh_from_db()
        return movie_uuid

    def remove_movie(self, movie_id):
        """Remove movie form the collection."""
        Movies.objects.filter(uuid=movie_id).delete()
        return 'Successfully Deleted.'

    def create_or_get_director(self, directors: list):
        """Get or create directors."""
        directors_obj_list = []
        for director_name in directors:
            director_obj = Director.objects.get_or_create(
                director_name=director_name
            )
            directors_obj_list.append(director_obj)
        return directors_obj_list

    def create_or_get_genre(self, genres: list):
        """Get or create genres."""
        genres_obj_list = []
        for genre_name in genres:
            genre_obj = Genre.objects.get_or_create(
                name=genre_name
            )
            genres_obj_list.append(genre_obj)
        return genres_obj_list

    def get_or_create_genre_and_director(self, data: dict):
        """Get or create genre and director."""
        directors = self.create_or_get_director(data.get('director'))
        data.pop('director')
        genres = self.create_or_get_genre(data.get('genre'))
        data.pop('genre')
        return directors, genres

    def add_genre_director(self, movie_obj, genres: list, directors: list):
        """Add genre and director for a movie."""
        for genre_obj in genres:
            movie_obj.genre.add(genre_obj)
        for director_obj in directors:
            movie_obj.director.add(director_obj)
        self.movie_obj.save()
        return movie_obj.uuid

    def search_movies(self, input_data):
        return Movies.objects.filter(name__icontains=input_data.get('data'))
