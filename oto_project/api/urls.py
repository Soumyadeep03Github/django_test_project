"""Urls file for API app."""

from django.urls import path
from api.views import (
    MovieView,
)


app_name = 'api'
urlpatterns = [
    path('',
         MovieView.as_view(),
         name='movie-list'),
    path('movie/<uuid:movie_uuid>/detail/',
         MovieView.as_view(),
         name='movie-detail'),
    path('movie/create/',
         MovieView,
         name='movie-create'),
    path('movie/<uuid:movie_uuid>/update/',
         MovieView,
         name='movie-update'),
    path('movie/<uuid:movie_uuid>/delete/',
         MovieView.as_view(),
         name='movie-delete'),
]
