from rest_framework.permissions import SAFE_METHODS, BasePermission
from users.models import User


class IsAdminOrSuperuser(BasePermission):
    def has_permission(self, request, view):

        return (
            request.user.is_superuser
            or request.user.role == User.ADMIN
        )


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or (
                request.user.is_authenticated
                and (
                    request.user.is_superuser
                    or request.user.role == User.ADMIN
                )
            )
        )
