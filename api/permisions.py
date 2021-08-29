from rest_framework import permissions


class MenuPermission(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        if view.action == 'menus_with_dishes':
            return True
        if view.action == 'retrieve':
            return True
        return request.user.is_authenticated
