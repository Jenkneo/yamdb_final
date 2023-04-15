from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Разрешение на уровне запроса, позволяющее редактировать его только
    администратору или суперюзеру.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_staff or request.user.role == "admin"


class IsAdminOrReadOnly(permissions.BasePermission):
    """Разрешение на уровне запроса, позволяющее редактировать только
    администратору и читать всем остальным.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_staff or request.user.role == 'admin'


class IsAdminOrModeratorOrAuthor(permissions.BasePermission):
    """Разрешение на уровне запроса/объекта, позволяющее редактировать/
    выполнять его только администратору/модератору/автору объекта.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if (
                obj.author == request.user
                or request.user.is_staff
                or request.user.role == 'moderator'
                or request.user.role == 'admin'
                or request.method == 'POST'
            ):
                return True
        elif request.method in permissions.SAFE_METHODS:
            return True
