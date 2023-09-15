from django.urls import include, path
from .views import signup
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, signup, token_jwt


router = DefaultRouter()
router.register(r'users', UserViewSet)



urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', signup, name='signup'),
    path('auth/token/', token_jwt, name='token'),
]