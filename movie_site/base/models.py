from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=200)
    day = models.CharField(max_length=200)
    month = models.CharField(max_length=200)
    year = models.CharField(max_length=200)
    film = models.CharField(max_length=200)
    released = models.CharField(max_length=200)
    rating = models.CharField(max_length=200)
    review_link = models.CharField(max_length=200)
    film_link = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

class Item2(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

class MovieInfo(models.Model):
    image = models.TextField()
    director = models.TextField()
    dateModified = models.TextField()
    productionCompany = models.TextField()
    releasedEvent = models.TextField()
    url = models.TextField()
    actors = models.TextField()
    dateCreated = models.TextField()
    name = models.TextField()
    reviewCount = models.TextField()
    ratingValue = models.TextField()
    ratingCount = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
