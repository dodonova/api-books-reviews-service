from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import (Category,
                            Genre,
                            Title,
                            Review,
                            Comment)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('slug', 'name')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('slug', 'name')


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
    # category = CategorySerializer()
    # genre = GenreSerializer(many=True)


    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'category', 'genre', 'description', 'rating')
    
    def to_representation(self, instance):
         # Если запрос GET, то сериализуем связанные объекты через соответствующие сериализаторы
        if self.context['request'].method == 'GET':
            # category = CategorySerializer()
            # genre = GenreSerializer(many=True)
            
            genre_serializer = GenreSerializer(instance.genre.all(), many=True)
            category_serializer = CategorySerializer(instance.category)
            return {
                'id': instance.id,
                'name': instance.name,
                'year': instance.year,
                'rating': instance.rating,
                'description': instance.description,
                'genre': genre_serializer.data,
                'category': category_serializer.data
            }
        else:
            return super().to_representation(instance)

    def create(self, validated_data):
        genre_data = validated_data.pop('genre')
        category = validated_data.pop('category')
        # category = Category.objects.get(slug=category_slug)
        title = Title.objects.create(category=category, **validated_data)
        for genre_data in genre_data:
            genre = Genre.objects.get(slug=genre_data.slug)
            title.genre.add(genre)
        return title
        
    

    

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