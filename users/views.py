from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .serializers import UserRegisterSerializer, LoginSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAdminUser
from .permissions import IsNormalUser, IsSuperUser, IsAnonymousUser
from .models import CustomUser
from django.core.cache import cache

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

class NormalUserAPI(APIView):
    permission_classes=[IsNormalUser]
    
    def get(self, request):
        return Response({"message": "Hello World 1."})

class SuperUserAPI(APIView):
    permission_classes=[IsSuperUser]
    
    def get(self, request):
        return Response({"message": "Hello World 2."})
    
class AnonymousAPI(APIView):
    permission_classes=[IsAnonymousUser]
    
    def get(self, request):
        return Response({"message":"Hello World 3."})
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    
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