from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, re_path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from location.routers import router

schema_view = get_schema_view(
    openapi.Info(
        title='Location Service API',
        default_version='latest',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0),
         name='docs-swagger-ui'),
    re_path(r'^docs/swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0),
            name='docs-swagger-raw'),
    path('health_check/', include('health_check.urls')),
]

urlpatterns += staticfiles_urlpatterns()
