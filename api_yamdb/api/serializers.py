from django.shortcuts import get_object_or_404
from rest_framework import serializers, validators

from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title,
)


class SlugNameSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('slug', 'name')
        abstract = True


class CategorySerializer(SlugNameSerializer):

    class Meta(SlugNameSerializer.Meta):
        model = Category


class GenreSerializer(SlugNameSerializer):

    class Meta(SlugNameSerializer.Meta):
        model = Genre


class TitleGETSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )

    class Meta:
        fields = '__all__'
        model = Title

    def to_representation(self, instance):
        return TitleGETSerializer(instance).data


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        if not self.context['request'].method == 'POST':
            return data
        author = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if Review.objects.filter(title=title, author=author).exists():
            raise validators.ValidationError(
                'Нельзя дважды писать ревью на одно произведение'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Comment
        exclude = ('review',)
