from rest_framework.permissions import BasePermission

class IsAdminForCreate(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            return request.user.is_superuser
        return True