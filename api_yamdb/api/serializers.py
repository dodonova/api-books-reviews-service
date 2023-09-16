from django.core.files.base import ContentFile
from rest_framework import serializers, permissions
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'slug', 'name')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('id', 'slug', 'name')


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        slug_field='slug',
    )

    class Meta:
        model = Title
        fields = ('name', 'year', 'category', 'genre')


    def create(self, validated_data):
        genre_data = validated_data.pop('genre')
        category = validated_data.pop('category')
        title = Title.objects.create(category=category, **validated_data)
        for genre_data in genre_data:
            genre = Genre.objects.get(slug=genre_data.slug)
            title.genre.add(genre)
        return title
from rest_framework import serializers

from reviews.models import Review, Comment


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date',)
        model = Comment
        # read_only_fields = ('author', 'review_id',)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        model = Review
        # read_only_fields = ('author', 'title_id',)
