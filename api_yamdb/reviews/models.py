from django.core.validators import MaxLengthValidator, RegexValidator
from django.db import models

from users.models import User


class SlugNameModel(models.Model):
    name = models.CharField(
        max_length=200,
        validators=[
            MaxLengthValidator(limit_value=200)
        ]
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        validators=[
            MaxLengthValidator(50),
            RegexValidator(regex=r'^[-a-zA-Z0-9_]+$')
        ]
    )

    class Meta:
        abstract = True


class Category(SlugNameModel):
    pass


class Genre(SlugNameModel):
    pass


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 null=True)
    genre = models.ManyToManyField(Genre, blank=True)
    description = models.TextField(blank=True, null=True)


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