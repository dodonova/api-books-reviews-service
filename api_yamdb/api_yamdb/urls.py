from django.contrib import admin
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
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )

router = SimpleRouter()
router.register(
    r'titles/(?P<title_id>[^/.]+)/reviews/(?P<review_id>[^/.]+)/comments',
    CommentViewSet,
    basename='comment'
)
router.register(
    r'titles/(?P<title_id>[^/.]+)/reviews/',
    ReviewViewSet,
    basename='review'
)


urlpatterns = [
    path('api/v1/', include(router.urls)),
]
