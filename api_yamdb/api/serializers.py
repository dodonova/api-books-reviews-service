from rest_framework import serializers

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
    category = CategorySerializer()
    genre = GenreSerializer(many=True)


    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'category',
            'genre',
            'description','rating'
        )
    

    def create(self, validated_data):
        genre_data = validated_data.pop('genre')
        category = validated_data.pop('category')
        title = Title.objects.create(
            category=category, **validated_data)
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


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = (
            'id', 'text', 'author', 'score', 'pub_date',)
        model = Review