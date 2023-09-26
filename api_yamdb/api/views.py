from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from api.filters import TitleGenreFilter
from api.permissions import (
    IsAdminOrSafeMethods,
    IsAuthorModerAdminOrSafeMethods
)
from api.serializers import (
    CommentSerializer,
    ReviewSerializer,
)
from reviews.models import (
    Category,
    Genre,
    Title,
    Review,
)
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleGETSerializer,
    TitleSerializer,
)
from api.mixins import SlugNameViewSet


class CategoryViewSet(SlugNameViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(SlugNameViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('name')
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitleGenreFilter
    permission_classes = (IsAdminOrSafeMethods,)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitleSerializer
        return TitleGETSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorModerAdminOrSafeMethods,)

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())

    def get_queryset(self):
        return self.get_title().reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorModerAdminOrSafeMethods,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_review(self):
        return get_object_or_404(
            Review,
            pk=self.kwargs['review_id'],
            title__id=self.kwargs['title_id'],
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        return serializer.save(
            author=self.request.user, review=self.get_review()
        )
