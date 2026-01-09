from rest_framework.permissions import BasePermission

class IsNormalUser(BasePermission):
    def has_permission(self, request, view):
        return(
            request.user and
            request.user.is_authenticated and
            not request.user.is_superuser
        )
        
class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return(
            request.user and
            request.user.is_authenticated and
            request.user.is_superuser
        )
        
class IsAnonymousUser(BasePermission):
    def has_permission(self, request, view):
        return not request.user or not request.user.is_authenticated