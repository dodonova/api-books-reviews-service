from rest_framework.permissions import (
    BasePermission,
    SAFE_METHODS
)


class IsAdminOrSuperuser(BasePermission):
    def has_permission(self, request, view):

        if not request.user.is_anonymous:
            return (
                request.user.is_superuser
                or request.user.role == 'admin'
            )
        return False


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or (
                request.user.is_authenticated
                and (
                    request.user.is_superuser
                    or request.user.role == 'admin'
                )
            )
        )
