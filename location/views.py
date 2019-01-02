from django.http import HttpRequest
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.request import Request

from .models import ProfileType
from .permissions import OrganizationPermission
from .serializers import ProfileTypeSerializer


class ProfileTypeViewSet(viewsets.ModelViewSet):
    """
    ProfileType helps grouping SiteProfiles together. For example, a
    ProfileType called 'billing' can be created to clasify all billing
    addresses stored.
    """
    def get_queryset(self):
        queryset = super().get_queryset()
        organization_uuid = self.request.session['jwt_organization_uuid']
        queryset = queryset.filter(organization_uuid=organization_uuid)
        return queryset

    def _extend_request(self, request):
        data = request.POST.copy()
        data['organization_uuid'] = request.session['jwt_organization_uuid']
        request_extended = Request(HttpRequest())
        request_extended._full_data = data
        return request_extended

    def create(self, request, *args, **kwargs):
        request_extended = self._extend_request(request)
        return super().create(request_extended, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        request_extended = self._extend_request(request)
        return super().update(request_extended, *args, **kwargs)

    queryset = ProfileType.objects.all()
    permission_classes = (OrganizationPermission,)
    serializer_class = ProfileTypeSerializer
    filter_backends = (OrderingFilter,)
    ordering = ('name',)
