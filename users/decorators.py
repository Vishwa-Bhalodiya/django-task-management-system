from functools import wraps
from rest_framework.response import Response
from rest_framework import status

def log_user_action(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        user = request.user
        print(f"[LOG] User={user} | View={self.__class__.__name__}")
        return func(self, request, *args, **kwargs)
    return wrapper

def normal_user_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        
        if hasattr(args[0], "user"):#Function-based View
            request = args[0]
        else:
            request = args[1]#Class-Based View
            
        if not  request.user.is_authenticated:
            return Response(
                {"detail": "Authentication required"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if  request.user.is_superuser or request.user.is_staff:
            return Response(
                {"detail": "Admins are not allowed"},
                status=status.HTTP_403_FORBIDDEN
            )
            
        return func(*args, **kwargs)
    return wrapper

def superuser_required(func):
    @wraps(func)
    def wrapper( *args, **kwargs):
        if hasattr(args[0], "user"):
            request = args[0]
        else:
            request = args[1]
            
        if not request.user.is_superuser:
            return Response(
                {"detail":"Admin Only"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return func(*args, **kwargs)
    return wrapper

def anonymous_required(func):
    @wraps(func)
    def wrapper( *args, **kwargs):
        if hasattr(args[0], "user"):
            request = args[0]
        else:
            request = args[1]
            
        if request.user.is_authenticated:
            return Response(
                {"detail":"Only Anonymous Users are Allowed"},
                status=status.HTTP_403_FORBIDDEN
                            
            )
        return func(*args, **kwargs)
    return wrapper
        