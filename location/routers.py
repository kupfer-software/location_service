from rest_framework import routers
from . import views

router = routers.SimpleRouter()
router.register(r'profiletypes', views.ProfileTypeViewSet)
router.register(r'siteprofiles', views.SiteProfileViewSet)
