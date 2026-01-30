from rest_framework.permissions import BasePermission

class IsNormalUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        
        if not user or not user.is_authenticated:
            return False
        
        return user.roles.filter(name="user").exists()
        
class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        
        if not user or not user.is_authenticated:
            return False
        
        return user.roles.filter(name="admin").exists()
        
        
class IsAnonymousUser(BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_authenticated
    
