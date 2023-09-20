from django.shortcuts import render
from rest_framework import viewsets, filters, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import LimitOffsetPagination


from users.permissions import IsAdminOrReadOnly

from .serializers import CategorySerializer, GenreSerializer, TitleSerializer
from reviews.models import Category, Genre, Title, Review, Comment
# from users.permissions import IsAdminOrReadOnly

from api.serializers import (
    ReviewSerializer,
    CommentSerializer,
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly, )
    pagination_class = LimitOffsetPagination


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly, )


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer



class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    # permission_classes = (AuthorOrReadOnly,)

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        serializer.save(
            author=self.request.user, title_id=Title.objects.get(id=title_id))

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        new_queryset = Review.objects.filter(title_id=title_id)
        return new_queryset


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    # permission_classes = (AuthorOrReadOnly,)

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        serializer.save(
            author=self.request.user,
            review_id=Review.objects.get(id=review_id)
        )

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        new_queryset = Comment.objects.filter(review_id=review_id)
        return new_queryset
