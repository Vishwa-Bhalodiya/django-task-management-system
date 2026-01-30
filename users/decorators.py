from dataclasses import dataclass
from functools import wraps
from datetime import datetime
from rest_framework.response import Response
from rest_framework import status
from .utils import Utils
from typing import Optional
from rest_framework_simplejwt.authentication import JWTAuthentication

@dataclass
class DecoratorResponse:#Hold response data and convert DRF Response object
    message: str # Response message like Permission Denied
    status_code: int = status.HTTP_403_FORBIDDEN
    
    def to_response(self):
        # Convert to DRF Response Object
        return Response({"detail": self.message}, status=self.status_code)
    
@dataclass
class RequestUser:
    user: object
    is_authenticated: bool
    role: Optional[str] = None
    is_superuser: bool = False
    is_staff: bool = False
    


def log_user_action(func):
    @wraps(func)
    def wrapper(self, request):
        user = request.user
        print(f"[{Utils.format_datetime(datetime.now())}] User={user} | View={self.__class__.__name__}")
        return func(self, request)
    return wrapper

"""
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
"""        


def role_required(allowed_roles, allowed_fields=None):
    """
    RABC decorator with optional field restriction.
    - allowed_roles: list of roles allowed for this API
    - allowed_fields: list of keys allowed in request.data
    """
    allowed_fields = allowed_fields or []
    
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):

            # 1️⃣ Field validation
            if allowed_fields and request.method in ["POST", "PUT", "PATCH"]:
                extra_fields = set(request.data.keys()) - set(allowed_fields)
                if extra_fields:
                    return Response(
                        {"detail": f"Invalid fields: {', '.join(extra_fields)}"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            user = request.user

            # 2️⃣ Authentication check
            if not user.is_authenticated:
                if "anonymous" in allowed_roles:
                    return func(self, request, *args, **kwargs)
                return Response(
                    {"detail": "Authentication required"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # 3️⃣ Role check (MULTIPLE ROLES)
            user_roles = user.roles.values_list("name", flat=True)
            if not set(user_roles).intersection(set(allowed_roles)):
                return Response(
                    {"detail": "Access denied"},
                    status=status.HTTP_403_FORBIDDEN
                )

            return func(self, request, *args, **kwargs)

        return wrapper
    return decorator
    """
            # Wrap user info in dataclass      
            user = request.user
            req_user = RequestUser(
                user=user,
                is_authenticated=user.is_authenticated,
                role=getattr(user, "role", None),
                is_superuser=getattr(user, "is_superuser", False),
                is_staff=getattr(user, "is_staff", False)
            )

            # Check authentication
            if not req_user.is_authenticated:
                if "anonymous" in allowed_roles:
                    return func(self, request)
                return DecoratorResponse("Authentication required", status.HTTP_401_UNAUTHORIZED).to_response()

            # Check role authorization
            if req_user.role not in allowed_roles:
                return DecoratorResponse("Access Denied: Insufficient role", status.HTTP_403_FORBIDDEN).to_response()

            return func(self, request)
        return wrapper
    return decorator
"""
def superuser_required(func):
    """Allows only superuser/admin access"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        request = args[0] if hasattr(args[0], "user") else args[1]
        user = request.user

        req_user = RequestUser(
            user=user,
            is_authenticated=user.is_authenticated,
            is_superuser=getattr(user, "is_superuser", False)
        )

        if not req_user.is_superuser:
            resp = DecoratorResponse(
                message="Admin Only",
                status_code=status.HTTP_401_UNAUTHORIZED
            )
            return resp.to_response()
        return func(*args, **kwargs)
    return wrapper


def anonymous_required(func):
    """Allows only anonymous users"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        request = args[0] if hasattr(args[0], "user") else args[1]
        user = request.user

        req_user = RequestUser(
            user=user,
            is_authenticated=user.is_authenticated
        )

        if req_user.is_authenticated:
            resp = DecoratorResponse(
                message="Only Anonymous Users are Allowed",
                status_code=status.HTTP_403_FORBIDDEN
            )
            return resp.to_response()
        return func(*args, **kwargs)
    return wrapper