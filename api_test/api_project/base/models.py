from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=200)
    day = models.CharField(max_length=200)
    film = models.CharField(max_length=200)
    released = models.CharField(max_length=200)
    rating = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
