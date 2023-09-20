from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SignUpView, UserViewSet, token_jwt

router = DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', SignUpView.as_view(), name='signup'),
    path('auth/token/', token_jwt, name='token'),
]