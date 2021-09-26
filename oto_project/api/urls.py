"""Urls file for API app."""

from django.urls import path
from api.views import (
    MovieView,
    UserLoginView
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
         MovieView.as_view(),
         name='movie-create'),
    path('movie/<uuid:movie_uuid>/update/',
         MovieView.as_view(),
         name='movie-update'),
    path('movie/<uuid:movie_uuid>/delete/',
         MovieView.as_view(),
         name='movie-delete'),
    path('login/',
         UserLoginView.as_view(),
         name='user-login'),
]
