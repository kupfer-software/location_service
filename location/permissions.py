import re

from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError


def _valid_uuid4(uuid_string):
    uuid4hex = re.compile('^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}\Z',
                          re.I)
    match = uuid4hex.match(uuid_string)
    return bool(match)


class AllowOptionsAuthentication(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method == 'OPTIONS':
            return True

        if getattr(request, 'session', None) and request.session.get('jwt_organization_uuid'):
            organization_uuid = request.session['jwt_organization_uuid']
            if not _valid_uuid4(organization_uuid):
                raise ValidationError(
                    f'organization_uuid from JWT Token "{organization_uuid}" is not a valid UUID.'
                )
            return True
        return False


class OrganizationPermission(AllowOptionsAuthentication):
    def has_object_permission(self, request, _view, obj):
        if getattr(request, 'session', None):
            if request.session.get('jwt_organization_uuid') == \
                    str(obj.organization_uuid):
                return True
            else:
                raise PermissionDenied('User is not in the same organization '
                                       'as the object.')
