from rest_framework.pagination import LimitOffsetPagination
from rest_framework import (
    filters,
    mixins,
    viewsets
)

from api.permissions import IsAdminOrGetList


class SlugNameViewSet(
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
