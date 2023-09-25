from datetime import datetime

from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models
from django.utils import timezone

from users.models import User


class SlugNameModel(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True,
        max_length=50,
    )

    class Meta:
        ordering = ['name']
        abstract = True

    def __str__(self):
        return self.name


class Category(SlugNameModel):

    class Meta(SlugNameModel.Meta):
        verbose_name = 'категория',
        verbose_name_plural = 'Категории'


class Genre(SlugNameModel):

    class Meta(SlugNameModel.Meta):
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год издания',
        validators=[
            MaxValueValidator(datetime.now().year)
        ]
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='categories'
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанр'
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(year__lte=timezone.now().year,),
                name='year_lte_this_year'
            ),
            models.CheckConstraint(
                check=models.Q(year__gte=0,),
                name='year_gte_min_year'
            ),
        ]
        ordering = ('name',)
        verbose_name = 'произведение',
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:30]


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.title}-{self.genre}'[:50]


class TextAuthorPub_date(models.Model):
    text = models.TextField('текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='автор')
    pub_date = models.DateTimeField(
        verbose_name='дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['pub_date']
        abstract = True

    def __str__(self):
        return self.name[:50]


class Review(TextAuthorPub_date):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    score = models.PositiveSmallIntegerField(
        'рейтинг произведения',
        validators=[
            MinValueValidator(1, '< 1'),
            MaxValueValidator(10, '> 10')
        ]
    )

    class Meta(TextAuthorPub_date.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='title_author'
            )
        ]
        ordering = ('pub_date',)
        verbose_name = 'отзыв',
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'


class Comment(TextAuthorPub_date):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='отзыв'
    )

    class Meta(TextAuthorPub_date.Meta):
        ordering = ('pub_date',)
        verbose_name = 'комментарий',
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
