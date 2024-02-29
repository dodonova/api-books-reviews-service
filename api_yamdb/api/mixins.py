from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from users.permissions import IsAdminOrReadOnly


class SlugNameViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (IsAdminOrReadOnly, )
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=slug', 'name')
