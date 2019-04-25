from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, re_path, include
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from location.routers import router

swagger_info = openapi.Info(
    title='Location Service API',
    default_version='latest',
    description="The location service enables your application to store and group international addresses.",
)

schema_view = get_schema_view(
    swagger_info,
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^docs/swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='docs-swagger-raw'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0),
         name='docs-swagger-ui'),
    path('health_check/', include('health_check.urls')),
    path('', include((router.urls, 'app_name'), namespace='location')),
]

urlpatterns += staticfiles_urlpatterns()
