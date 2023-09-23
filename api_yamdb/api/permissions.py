from rest_framework import permissions


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == 'admin')


class IsAdminOrSafeMethods(IsAdmin):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or super().has_permission(request, view)
        )


class IsAuthorModerAdminOrSafeMethods(permissions.IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or (request.user.role == 'moderator')
            or (request.user.role == 'admin')
        )
