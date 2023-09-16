from django.urls import include, path
from rest_framework import routers

from .views import CategoryViewSet, GenreViewSet, TitleViewSet

router = routers.DefaultRouter()
router.register(r'category', CategoryViewSet),
router.register(r'genre', GenreViewSet)
router.register(r'titles', TitleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('v1/api-token-auth/', views.obtain_auth_token)
    # path('v1/', include('djoser.urls.jwt')),
    # path('v1/auth/', include('djoser.urls')),
]
