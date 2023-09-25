from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import SignUpView, UserViewSet, token_jwt

router = DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/auth/signup/', SignUpView.as_view(), name='signup'),
    path('api/v1/auth/token/', token_jwt, name='token'),
]
