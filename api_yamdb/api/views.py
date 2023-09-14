from rest_framework import viewsets

from api.serializers import (
    ReviewSerializer,
    CommentSerializer,
)

from reviews.models import Review, Comment, Title


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
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
    # permission_classes = (AuthorOrReadOnly,)

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        serializer.save(
            author=self.request.user,
            review_id=Review.objects.get(id=review_id)
        )

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        review_id = self.kwargs.get("review_id")
        new_queryset = Comment.objects.filter(
            title_id=title_id, review_id=review_id
        )
        return new_queryset
