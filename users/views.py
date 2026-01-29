from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .serializers import UserRegisterSerializer, LoginSerializer, UserSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from .permissions import IsNormalUser, IsSuperUser, IsAnonymousUser
from .models import CustomUser
from django.core.cache import cache
from .decorators import log_user_action, role_required, superuser_required, anonymous_required
from .utils import ExternalAPIService
from dataclasses import dataclass
from users.services.user_api import UserAPI

@dataclass
class RegisterRequest:
    username: str
    email: str
    password: str
    
@dataclass
class RegisterResponse:
    status: str
    message: str
    user_id: int = None
    
class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        #Validate allowed fields only
        allowed_fields = ['username',  'email', 'password']
        extra_fields = set(request.data.keys()) - set(allowed_fields)
        if extra_fields:
            return Response({"detail": f"Invalid fields: {', '.join(extra_fields)}"}, status=400)
        
        #Wrap request in dataclass
        try:
            req = RegisterRequest(**request.data)
        except TypeError as e:
            return Response({"detail": f"Invalif fields: {str(e)}"}, status=400)
        
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            resp = RegisterResponse(status="success", message="User Created", user_id=user.id)
            return Response(resp.__dict__, status=201)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer
"""
class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "is_admin": user.is_superuser, 
            "username": user.username,
        })
"""
class NormalUserAPI(APIView):
    permission_classes=[IsNormalUser]
    
    @log_user_action
    def get(self, request):
        return Response({"message": "Hello World 1."})

class SuperUserAPI(APIView):
    permission_classes=[IsSuperUser]
    
    @log_user_action
    def get(self, request):
        return Response({"message": "Hello World 2."})
    
class AnonymousAPI(APIView):
    permission_classes=[IsAnonymousUser]
    
    @log_user_action
    def get(self, request):
        return Response({"message":"Hello World 3."})

#Example of API using RBAC decorators
class NormalAPI(APIView):
    @role_required(allowed_roles=["user"])
    def get(self, request):
        return Response({"message": "Hello World 1 from Decorators"})
    
class SuperAPI(APIView):
    @role_required(["admin"])
    def get(self, request):
        return Response({"message":"Hello World 2 From Decorators"})
    
class AnonymousUserAPI(APIView):
    permission_classes = [AllowAny]
    @role_required(["anonymous"])
    def get (self, request):
        return Response({"message":"Hello World 3 From Decorators"})
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    
    @log_user_action
    def list(self, request, *args, **kwargs):
       return super().list(request, *args, **kwargs)
    
    def get_queryset(self):
        cache_key = "admin_users"
        user_ids = cache.get(cache_key)
        
        if user_ids is None:
            user_ids = list(
                CustomUser.objects.values_list("id", flat=True)
            )
            cache.set(cache_key, user_ids, 300)
    
        return CustomUser.objects.filter(id__in=user_ids)
    
    def perform_create(self, serializer):
        serializer.save()
        cache.delete("admin_users")
        
    def perform_update(self, serializer):
        serializer.save()
        cache.delete("admin_users")
        
    def perform_destroy(self, instance):
        cache.delete("admin_users")
        instance.delete()
        
class ExternalAPITest(APIView):
    def get(self, request):
        
        result = ExternalAPIService.fetch_public_apis()

        if not result["success"]:
            return Response(
                {"error": result["error"]},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        return Response(result, status=status.HTTP_200_OK)
    
class UserServiceAPI(APIView):
    def get(self, request):
        service = UserAPI()
        result = service.process_request(request)
        return Response(result, status=status.HTTP_200_OK)
    
