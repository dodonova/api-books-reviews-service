import re
from rest_framework import status
from rest_framework.response import Response


from users.permissions import IsAdmin


class CorrectSlugName(IsAdmin):
    def has_object_permission(self, request, view, obj):
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
        return True