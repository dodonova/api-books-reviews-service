from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import MaxLengthValidator, RegexValidator
from django.db import models
from django.utils import timezone

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
    name = models.CharField(max_length=256)
    year = models.PositiveSmallIntegerField()
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='category'
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
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
        ordering = ('-id',)

    def __str__(self):
        return self.name


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
        return f'{self.title}-{self.genre}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField()
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, '< 1'),
            MaxValueValidator(10, '> 10')
        ]
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='title_author'
            )
        ]
        ordering = ('pub_date',)

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('pub_date',)

    def __str__(self):
        return self.text
