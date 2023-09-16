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
    genres = serializers.SlugRelatedField(
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
