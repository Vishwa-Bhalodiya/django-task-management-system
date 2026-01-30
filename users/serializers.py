from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .utils import Utils

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}
        
    def validate_email(self, value):
        if not Utils.validate_email(value):
            raise serializers.ValidationError("Invalid email format")
        return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        user.is_superuser = False
        user.is_staff = False
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data['username'],
            password=data['password']
        )
        if user is None:
            raise serializers.ValidationError("Invalid credentials")
        return user  
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'is_superuser', 'is_staff', 'is_active']
        read_only_fields = fields
        
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        #Custom Claims
        token["roles"] = list(user.roles.values_list("name", flat=True))
        token["username"] = user.username
        token["is_staff"] = user.is_staff
        token["is_superuser"] = user.is_superuser
        
        return token