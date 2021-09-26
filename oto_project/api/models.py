"""Model file for API app."""
import uuid

from django.contrib.auth.models import User
from django.db import models


class Genre(models.Model):
    """Model class for Geners."""
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4,
                            editable=False)
    name = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Created At',
                                      db_index=True)
    modified_at = models.DateTimeField(auto_now=True,
                                       verbose_name='Last Modified At')

    def __str__(self):
        """Return name."""
        return self.name


class Director(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4,
                            editable=False)
    director_name = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Created At',
                                      db_index=True)
    modified_at = models.DateTimeField(auto_now=True,
                                       verbose_name='Last Modified At')


    def __str__(self):
        """Return name."""
        return self.director_name


class Movies(models.Model):
    """Model class for movies."""
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4,
                            editable=False)
    popularity = models.DecimalField(max_digits=10, decimal_places=4)
    director = models.ManyToManyField(Director, related_name='director')
    genre = models.ManyToManyField(Genre, related_name='genre')
    imdb_score = models.DecimalField(max_digits=10, decimal_places=4)
    name = models.CharField(max_length=200, blank=True, null=True)
    like = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Created At',
                                      db_index=True)
    modified_at = models.DateTimeField(auto_now=True,
                                       verbose_name='Last Modified At')

    def __str__(self):
        """Return name."""
        return self.name


class Token(models.Model):
    """Model Class for tokens."""
    token = models.UUIDField(primary_key=True, default=uuid.uuid4,
                            editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
