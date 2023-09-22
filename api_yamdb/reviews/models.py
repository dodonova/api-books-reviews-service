from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


from users.models import User

# User = get_user_model() # можно для начала так оставить



class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=50)


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    genre = models.ManyToManyField(Genre)
    description = models.TextField(blank=True, null=True)
    rating = models.FloatField(
        blank=True,
        null=True,
        default=5.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)]
    )



class Review(models.Model):
    title_id = models.ForeignKey(Title, on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    pub_date = models.DateTimeField(
        'Дата добавления ревью', auto_now_add=True, db_index=True)


class Comment(models.Model):
    review_id = models.ForeignKey(Review, on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(
        'Дата добавления комментария', auto_now_add=True, db_index=True)