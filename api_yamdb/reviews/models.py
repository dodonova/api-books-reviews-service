from django.contrib.auth import get_user_model
from django.db import models
from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Review(models.Model):
    title_id = models.ForeignKey(Title, on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    pub_date = models.DateTimeField()


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)


class Comment(models.Model):
    review_id = models.ForeignKey(Review, on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField()


class Genre_Title(models.Model):
    title_id = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE)
