from django.http import HttpRequest
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.request import Request

from .models import ProfileType, SiteProfile
from .permissions import OrganizationPermission
from .serializers import ProfileTypeSerializer, SiteProfileSerializer


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
        data = request.data.copy()
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


class SiteProfileViewSet(viewsets.ModelViewSet):
    """
    SiteProfile can be used to store any international address thanks to the
    flexible schema provided.

    For listing objects, there is a `profiletype__id` filter to be used in
    the querystring.

    The `country` field is a two-char ISO code.
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

    queryset = SiteProfile.objects.all()
    permission_classes = (OrganizationPermission,)
    serializer_class = SiteProfileSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ('profiletype__id',)
    ordering = ('name',)
