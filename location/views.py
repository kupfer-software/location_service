from django.http import HttpRequest
from django_filters import rest_framework as django_filters
from rest_framework import viewsets, status
from rest_framework import filters as drf_filters
from rest_framework.request import Request
from rest_framework.response import Response

from .models import ProfileType, SiteProfile
from .permissions import OrganizationPermission
from .serializers import ProfileTypeSerializer, SiteProfileSerializer
from . import filters


class OrganizationQuerySetMixin(object):
    """
    Adds functionality to return a queryset filtered by the organization_uuid in the JWT header.
    If no jwt header is given, an empty queryset will be returned.
    """
    def get_queryset(self):
        queryset = super().get_queryset()
        organization_uuid = self.request.session.get('jwt_organization_uuid', None)
        if not organization_uuid:
            return queryset.none()
        return queryset.filter(organization_uuid=organization_uuid)


class OrganizationExtensionMixin(object):
    """
    Extends the data with the organization from the JWT header for creation and validation in the serializer.
    """
    @staticmethod
    def _extend_request(request):
        data = request.data.copy()
        data['organization_uuid'] = request.session['jwt_organization_uuid']
        request_extended = Request(HttpRequest())
        request_extended._full_data = data
        return request_extended

    def create(self, request, *args, **kwargs):
        request_extended = self._extend_request(request)
        serializer = self.get_serializer(data=request_extended.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(organization_uuid=request_extended.data['organization_uuid'])
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        request_extended = self._extend_request(request)
        return super().update(request_extended, *args, **kwargs)


class ProfileTypeViewSet(OrganizationQuerySetMixin,
                         OrganizationExtensionMixin,
                         viewsets.ModelViewSet):
    """
    ProfileType helps grouping SiteProfiles together. For example, a
    ProfileType called 'billing' can be created to classify all billing
    addresses stored.
    """

    queryset = ProfileType.objects.all()
    permission_classes = (OrganizationPermission,)
    serializer_class = ProfileTypeSerializer
    filter_backends = (drf_filters.OrderingFilter,)
    ordering = ('name',)


class SiteProfileViewSet(OrganizationQuerySetMixin,
                         OrganizationExtensionMixin,
                         viewsets.ModelViewSet):
    """
    SiteProfile can be used to store any international address thanks to the
    flexible schema provided.

    For listing objects, there is a `profiletype__id` filter to be used in
    the querystring.

    The `country` field is a two-char ISO code.
    """

    filter_backends = (django_filters.DjangoFilterBackend,
                       drf_filters.SearchFilter,
                       drf_filters.OrderingFilter)
    filter_class = filters.SiteProfileFilter
    ordering = ('name',)
    permission_classes = (OrganizationPermission,)
    queryset = SiteProfile.objects.all()
    serializer_class = SiteProfileSerializer
    search_fields = ('address_line1', 'postcode', 'city', )
