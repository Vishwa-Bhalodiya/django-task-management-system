from django.urls import path,include
from .views import RegisterView, LoginView, NormalUserAPI, SuperUserAPI, AnonymousAPI,UserViewSet, NormalAPI, SuperAPI,AnonymousUserAPI, ExternalAPITest, UserServiceAPI
from rest_framework import routers, viewsets
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('api1/', NormalUserAPI.as_view()),
    path('api2/', SuperUserAPI.as_view()),
    path('api3/', AnonymousAPI.as_view()),
    path('api4/', NormalAPI.as_view()),
    path('api5/', SuperAPI.as_view()),
    path('api6/', AnonymousUserAPI.as_view()),
    path('external-api-test/', ExternalAPITest.as_view()),
    path('user-service-api/', UserServiceAPI.as_view()),
    path('', include(router.urls)),
]
