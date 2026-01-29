from .base_api import BaseAPI
from users.serializers import UserSerializer

class UserAPI(BaseAPI):

    def process_request(self, request):
        user = request.user
        return {
            "id": user.id,
            "username":user.username,
            "email": user.email,
            "role": user.role,
            "is_superuser": user.is_superuser,
            "is_staff": user.is_staff,
            "is_active": user.is_active,
            "date_joined": user.date_joined,
            
        }
        """
        return UserSerializer(user).data
        """