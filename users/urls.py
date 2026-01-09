from django.urls import path,include
from .views import RegisterView, LoginView, NormalUserAPI, SuperUserAPI, AnonymousAPI,UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('api1/', NormalUserAPI.as_view()),
    path('api2/', SuperUserAPI.as_view()),
    path('api3/', AnonymousAPI.as_view()),
    path('', include(router.urls)),
]
