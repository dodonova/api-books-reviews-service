from rest_framework import permissions

class IsAdminUserOrReadonly(permissions.IsAuthenticatedOrReadOnly):
    def has_permission(self, request, view):
        return (
                request.method in permissions.SAFE_METHODS
                or request.user.is_superuser # is_staff
            )
