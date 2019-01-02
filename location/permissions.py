from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied


class AllowOptionsAuthentication(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method == 'OPTIONS':
            return True

        if getattr(request, 'session', None) and \
                request.session.get('jwt_organization_uuid'):
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
