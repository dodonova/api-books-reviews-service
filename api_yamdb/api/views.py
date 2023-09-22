import re

from django.shortcuts import render
from django.views.decorators.http import require_http_methods


from rest_framework import viewsets, filters, permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response



from users.permissions import IsAdminOrReadOnly, IsAdmin, IsAdminExceptGet

from .serializers import CategorySerializer, GenreSerializer, TitleSerializer
from reviews.models import Category, Genre, Title, Review, Comment
# from users.permissions import IsAdminOrReadOnly

from api.serializers import (
    ReviewSerializer,
    CommentSerializer,
)


class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly, IsAdmin)
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=slug', 'name')

    def get_permissions(self):
        if self.action == 'list': 
            if self.request.method == 'GET':
                self.permission_classes = [permissions.AllowAny]
            else:
                self.permission_classes = [IsAdmin, ]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdmin]
        return super(BaseViewSet, self).get_permissions()
    
    def create(self, request, *args, **kwargs):
        data = request.data
        if set(data.keys()) != {'slug', 'name'}:
            return Response(
                {'error': 'JSON should contain "slug" and "name" keys'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if len(data['name']) > 200:
            return Response(
                {'error': 'Name should not exceed 256 characters'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if len(data['slug']) > 50:
            return Response(
                {'error': 'Slug should not exceed 50 characters'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not re.match(r'^[-a-zA-Z0-9_]+$', data['slug']):
            return Response(
                {'error': 'Slug should match the pattern ^[-a-zA-Z0-9_]+$'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super(BaseViewSet, self).create(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        return Response({'error': f'Method {self.request.method} Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def update(self, request, *args, **kwargs):
        return Response({'error': f'Method {self.request.method} Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, *args, **kwargs):
        return Response({'error': f'Method {self.request.method} Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class CategoryViewSet(BaseViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class GenreViewSet(BaseViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


# class CategoryViewSet(viewsets.ModelViewSet):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     permission_classes = (IsAdminOrReadOnly, IsAdmin)
#     pagination_class = LimitOffsetPagination
#     lookup_field = 'slug'
#     filter_backends = (filters.SearchFilter,)
#     search_fields = ('=slug', 'name')

#     def get_permissions(self):
#         if self.action == 'list': 
#             if self.request.method == 'GET':
#                 self.permission_classes = [permissions.AllowAny]
#             else:
#                 self.permission_classes = [IsAdmin, ]
#         elif self.action in ['update', 'partial_update', 'destroy']:
#             self.permission_classes = [IsAdmin]
#         return super(CategoryViewSet, self).get_permissions()
    
#     def create(self, request, *args, **kwargs):
#         data = request.data
#         if set(data.keys()) != {'slug', 'name'}:
#             return Response(
#                 {'error': 'JSON should contain "slug" and "name" keys'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         if len(data['name']) > 200:
#             return Response(
#                 {'error': 'Name should not exceed 256 characters'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         if len(data['slug']) > 50:
#             return Response(
#                 {'error': 'Slug should not exceed 50 characters'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         if not re.match(r'^[-a-zA-Z0-9_]+$', data['slug']):
#             return Response(
#                 {'error': 'Slug should match the pattern ^[-a-zA-Z0-9_]+$'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         return super(CategoryViewSet, self).create(request, *args, **kwargs)
    
#     def partial_update(self, request, *args, **kwargs):
#         return Response({'error': f'Method {self.request.method} Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
#     def update(self, request, *args, **kwargs):
#         return Response({'error': f'Method {self.request.method} Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

#     def retrieve(self, request, *args, **kwargs):
#         return Response({'error': f'Method {self.request.method} Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# # TODO: объединить классы Genre и Category одним предком

 
# class GenreViewSet(viewsets.ModelViewSet):
#     queryset = Genre.objects.all()
#     serializer_class = GenreSerializer
#     # permission_classes = (IsAdminOrReadOnly, )
#     permission_classes = (IsAdminOrReadOnly, IsAdmin)
#     pagination_class = LimitOffsetPagination
#     lookup_field = 'slug'
#     filter_backends = (filters.SearchFilter,)
#     search_fields = ('=slug', 'name')

#     def get_permissions(self):
#         if self.action == 'list': 
#             if self.request.method == 'GET':
#                 self.permission_classes = [permissions.AllowAny]
#             else:
#                 self.permission_classes = [IsAdmin, ]
#         elif self.action in ['update', 'partial_update', 'destroy']:
#             self.permission_classes = [IsAdmin]
#         return super(GenreViewSet, self).get_permissions()
    
#     def create(self, request, *args, **kwargs):
#         data = request.data
#         if set(data.keys()) != {'slug', 'name'}:
#             return Response(
#                 {'error': 'JSON should contain "slug" and "name" keys'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         if len(data['name']) > 200:
#             return Response(
#                 {'error': 'Name should not exceed 256 characters'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         if len(data['slug']) > 50:
#             return Response(
#                 {'error': 'Slug should not exceed 50 characters'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         if not re.match(r'^[-a-zA-Z0-9_]+$', data['slug']):
#             return Response(
#                 {'error': 'Slug should match the pattern ^[-a-zA-Z0-9_]+$'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         return super(GenreViewSet, self).create(request, *args, **kwargs)

#     def partial_update(self, request, *args, **kwargs):
#         return Response({'error': f'Method {self.request.method} Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
#     def update(self, request, *args, **kwargs):
#         return Response({'error': f'Method {self.request.method} Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

#     def retrieve(self, request, *args, **kwargs):
#         return Response({'error': f'Method {self.request.method} Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly, )




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
