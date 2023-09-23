from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from api.filters import TitleGenreFilter
from api.permissions import (
    IsAdminOrSafeMethods,
    IsAuthorModerAdminOrSafeMethods
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import (
    viewsets, filters, permissions, mixins
)

from users.permissions import IsAdminOrReadOnly, IsAdmin
from reviews.models import (
    Category,
    Genre,
    Title,
    Review,
    Comment
)
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer
)
from api.serializers import (
    ReviewSerializer,
    CommentSerializer,
)
from .permissions import IsAdminOrGetList

class BaseSlugNameViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (IsAdminOrGetList, )
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=slug', 'name')


class CategoryViewSet(BaseSlugNameViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class GenreViewSet(BaseSlugNameViewSet):
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
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthorModerAdminOrSafeMethods,)

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id).reviews.all()


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
