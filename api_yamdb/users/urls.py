from django.urls import include, path
from rest_framework import routers

from .views import CustomUserViewSet, get_confirmation_code, get_token

router_v1 = routers.DefaultRouter()
router_v1.register('users', CustomUserViewSet, basename='users')


urlpatterns = [
    path('v1/auth/signup/', get_confirmation_code),
    path('v1/auth/token/', get_token),
    path('v1/', include(router_v1.urls)),
]
