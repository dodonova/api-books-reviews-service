from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import SignUpView, UserViewSet, token_jwt

router = DefaultRouter()
router.register(r'users', UserViewSet)

auth_urls = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('token/', token_jwt, name='token'),
]

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/auth/', include(auth_urls)),
]
