
from django.db.models import Q
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
    retrieve:
    Retrieves a ProfileType by its ID.

    Retrieves a ProfileType by its ID.

    list:
    Retrieves a list of ProfileTypes.

    Retrieves a list of ProfileTypes.

    create:
    Creates a new ProfileType.

    Creates a new ProfileType.

    update:
    Updates the ProfileType with the given ID (all fields).

    Updates the ProfileType with the given ID (all fields).

    partial_update:
    Updates the ProfileType with the given ID (only specified fields).

    Updates the ProfileType with the given ID (only specified fields).

    destroy:
    Deletes the ProfileType with the given ID.

    Deletes the ProfileType with the given ID.
    """

    def list(self, request, *args, **kwargs):
        """
        Filter for organization only if query-param is_global=False or
        for organization AND global ProfileTypes.
        """
        if not request.query_params.get('is_global', 'false').lower() == 'true':
            queryset = ProfileType.objects.all().filter(
                Q(organization_uuid=self.request.session['jwt_organization_uuid']) |
                Q(is_global=True))
        else:
            queryset = ProfileType.objects.all().filter(is_global=True)
        queryset = self.filter_queryset(queryset)
        queryset = self.paginate_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)
        return self.get_paginated_response(serializer.data)

    queryset = ProfileType.objects.all()
    permission_classes = (OrganizationPermission,)
    serializer_class = ProfileTypeSerializer
    filter_backends = (django_filters.DjangoFilterBackend,
                       drf_filters.OrderingFilter,)
    filter_fields = ('is_global', )
    ordering = ('name',)


class SiteProfileViewSet(OrganizationQuerySetMixin,
                         OrganizationExtensionMixin,
                         viewsets.ModelViewSet):
    """
    retrieve:
    Retrieves a SiteProfile by its UUID.

    Retrieves a SiteProfile by its UUID.

    list:
    Retrieves a list of SiteProfiles.

    Retrieves a list of SiteProfiles.

    create:
    Creates a new SiteProfile.

    Creates a new SiteProfile.

    partial_update:
    Updates the SiteProfile with the given UUID (only specified fields).

    Updates the SiteProfile with the given UUID (only specified fields).

    update:
    Updates the SiteProfile with the given UUID (all fields).

    Updates the SiteProfile with the given UUID (all fields).

    destroy:
    Deletes the SiteProfile with the given UUID.

    Deletes the SiteProfile with the given UUID.
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
