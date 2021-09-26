"""Test file for testing all the views and the handlers."""
import json

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from api.models import (
    Director,
    Genre,
    Movies
)


class TestMovieView(TestCase):
    """Test class for movie view."""

    def setUp(self):
        """Setup the test case."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='test_user', email='test@test.com', password='1234')
        self.user.set_password('1234')
        self.user.save()
        self.client.force_login(self.user) 
        director = Director.objects.create(
            director_name='Test Name'
        )
        list_of_genres = ['Horror', 'Adventure', 'Fantasy']
        list_of_genres_objs = []
        for genre in list_of_genres:
            genres_obj = Genre.objects.create(
                name=genre
            )
            list_of_genres_objs.append(genres_obj)
        self.movie = Movies.objects.create(
            popularity='99.0',
            imdb_score='8.5',
            name='Test Movie Name'
        )
        for genre_obj in list_of_genres_objs:
            self.movie.genre.add(genre_obj)
        self.movie.director.add(director)
        self.movie.save()

    def test_movie_list(self):
        """Test case to show movie list."""
        url = reverse('api:movie-list')
        main_url = 'http://127.0.0.1' + url
        response = self.client.get(main_url)
        self.assertEqual(response.status_code, 200)

    def test_movie_details(self):
        """Test case to show movie details."""
        url = reverse('api:movie-detail',
                      args=(self.movie.uuid,))
        main_url = 'http://127.0.0.1' + url
        response = self.client.get(main_url)
        self.assertEqual(response.status_code, 200)

    def test_movie_delete(self):
        """Test case to show movie delete."""
        url = reverse('api:movie-delete',
                      args=(self.movie.uuid,))
        main_url = 'http://127.0.0.1' + url
        response = self.client.delete(main_url)
        movie_obj = Movies.objects.filter(uuid=self.movie.uuid).first()
        self.assertEqual(movie_obj, None)
        self.assertEqual(response.status_code, 200)

    def test_movie_update(self):
        """Test case to show movie update."""
        url = reverse('api:movie-update',
                      args=(self.movie.uuid,))
        main_url = 'http://127.0.0.1' + url
        response = self.client.put(main_url, {'name': 'Test Movie Name Updated'})
        self.assertEqual(response.status_code, 200)


class TestMovieCreate(TestCase):
    """Test class for creating movie objects."""

    def setUp(self):
        """Set up for test class"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='test_user', email='test@test.com', password='1234')
        self.user.set_password('1234')
        self.user.save()
        self.client.force_login(self.user) 
        Director.objects.create(
            director_name='Test Name'
        )

    def test_movie_create(self):
        """Test case to movie create."""
        url = reverse('api:movie-create')
        main_url = 'http://127.0.0.1' + url
        response = self.client.post(main_url, {
            'popularity': 83.0,
            'director': [
                'Victor Fleming'
            ],
            'genre': [
                'Adventure',
                'Family',
                'Fantasy',
                'Musical'
            ],
            'imdb_score': 8.3,
            'name': 'The Wizard of Oz'
        })
        self.assertEqual(response.status_code, 200)
