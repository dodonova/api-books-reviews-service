from django.contrib import admin
<<<<<<< HEAD
=======
from django.urls import path, include
>>>>>>> feature/Anton
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import ReviewViewSet, CommentViewSet


urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
<<<<<<< HEAD
    path('api/v1/', include('api.urls')),
=======
    path('api/v1/', include('users.urls'))
>>>>>>> feature/Anton
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
