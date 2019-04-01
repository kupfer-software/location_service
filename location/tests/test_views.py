from decimal import Decimal
import uuid

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory

from . import model_factories as mfactories
from ..models import ProfileType, SiteProfile
from ..views import ProfileTypeViewSet, SiteProfileViewSet


# ###########
# ProfileType

class ProfileTypeOptionsViewsTest(TestCase):
    def test_options(self):
        response = self.client.options(reverse('location:profiletype-list'))
        self.assertIn(
            b'"name":"Profile Type List"',
            response.content)


class ProfileTypeListViewsTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.organization_uuid = str(uuid.uuid4())
        self.session = {
            'jwt_organization_uuid': self.organization_uuid,
        }

    def test_list_empty(self):
        request = self.factory.get('')
        request.session = self.session
        view = ProfileTypeViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 0)
        self.assertIsNone(response.data['next'])
        self.assertIsNone(response.data['previous'])

    def test_list_ordering_default(self):
        for name in ('C', 'A', 'B'):
            ProfileType.objects.create(
                name=name,
                organization_uuid=self.organization_uuid)
        ProfileType.objects.create(
            name='Not visible',
            organization_uuid=uuid.uuid4())

        request = self.factory.get('')
        request.session = self.session
        view = ProfileTypeViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 3)
        self.assertEqual(response.data['results'][0]['name'], 'A')
        self.assertEqual(response.data['results'][1]['name'], 'B')
        self.assertEqual(response.data['results'][2]['name'], 'C')

    def test_list_ordering_by_name_desc(self):
        for name in ('C', 'A', 'B'):
            ProfileType.objects.create(
                name=name,
                organization_uuid=self.organization_uuid)
        ProfileType.objects.create(
            name='Not visible',
            organization_uuid=uuid.uuid4())

        request = self.factory.get('?ordering=-name')
        request.session = self.session
        view = ProfileTypeViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 3)
        self.assertEqual(response.data['results'][0]['name'], 'C')
        self.assertEqual(response.data['results'][1]['name'], 'B')
        self.assertEqual(response.data['results'][2]['name'], 'A')

    def test_list_missing_organization_uuid(self):
        request = self.factory.get('')
        request.session = {}
        view = ProfileTypeViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 403)

    def test_list_profiletype_anonymoususer(self):
        request = self.factory.get('')
        view = ProfileTypeViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 403)


class ProfileTypeRetrieveViewsTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.organization_uuid = str(uuid.uuid4())
        self.session = {
            'jwt_organization_uuid': self.organization_uuid,
        }
        self.profiletype = ProfileType.objects.create(
            name='Nämé', organization_uuid=self.organization_uuid)

    def test_retrieve_successfully(self):
        request = self.factory.get('')
        request.session = self.session
        view = ProfileTypeViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=self.profiletype.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Nämé')
        self.assertEqual(response.data['organization_uuid'],
                         self.organization_uuid)

    def test_retrieve_not_allowed(self):
        request = self.factory.get('')
        request.session = {
            'jwt_organization_uuid': str(uuid.uuid4()),
        }
        view = ProfileTypeViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=self.profiletype.pk)
        self.assertEqual(response.status_code, 404)

    def test_retrieve_not_found(self):
        request = self.factory.get('')
        request.session = self.session
        view = ProfileTypeViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=288)
        self.assertEqual(response.status_code, 404)

    def test_retrieve_anonymoususer(self):
        request = self.factory.get('')
        view = ProfileTypeViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=288)
        self.assertEqual(response.status_code, 403)


class ProfileTypeCreateViewsTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.organization_uuid = str(uuid.uuid4())
        self.session = {
            'jwt_organization_uuid': self.organization_uuid,
        }

    def test_create_successfully(self):
        data = {
            'name': 'Söme namé',
        }
        request = self.factory.post('', data)
        request.session = self.session
        view = ProfileTypeViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, 201)

        profiletype = ProfileType.objects.get(pk=response.data['id'])
        self.assertEqual(profiletype.name, data['name'])
        self.assertEqual(str(profiletype.organization_uuid),
                         self.organization_uuid)

    def test_create_missing_param(self):
        request = self.factory.post('', {})
        request.session = self.session
        view = ProfileTypeViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(str(response.data['name'][0]),
                         'This field is required.')

    def test_create_missing_auth(self):
        request = self.factory.post('', {})
        view = ProfileTypeViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, 403)


class ProfileTypeUpdateViewsTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.organization_uuid = str(uuid.uuid4())
        self.session = {
            'jwt_organization_uuid': self.organization_uuid,
        }
        self.profiletype = ProfileType.objects.create(
            name='Nämé', organization_uuid=self.organization_uuid)

    def test_update_successfully(self):
        data = {
            'name': 'Nëw Náme',
        }
        request = self.factory.post('', data)
        request.session = self.session
        view = ProfileTypeViewSet.as_view({'post': 'update'})
        response = view(request, pk=self.profiletype.pk)
        self.assertEqual(response.status_code, 200)
        profiletype = ProfileType.objects.get(pk=self.profiletype.pk)
        self.assertEqual(profiletype.name, data['name'])

    def test_update_missing_data(self):
        request = self.factory.post('', {})
        request.session = self.session
        view = ProfileTypeViewSet.as_view({'post': 'update'})
        response = view(request, pk=self.profiletype.pk)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(str(response.data['name'][0]),
                         'This field is required.')

    def test_update_not_allowed(self):
        data = {
            'name': 'Nëw Náme',
        }
        request = self.factory.post('', data)
        request.session = {
            'jwt_organization_uuid': str(uuid.uuid4()),
        }
        view = ProfileTypeViewSet.as_view({'post': 'update'})
        response = view(request, pk=self.profiletype.pk)
        self.assertEqual(response.status_code, 404)
        self.assertTrue(
            ProfileType.objects.filter(pk=self.profiletype.pk).exists())

    def test_update_missing_auth(self):
        request = self.factory.post('', {})
        view = ProfileTypeViewSet.as_view({'post': 'update'})
        response = view(request, pk=self.profiletype.pk)
        self.assertEqual(response.status_code, 403)


class ProfileTypeDeleteViewsTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.organization_uuid = str(uuid.uuid4())
        self.session = {
            'jwt_organization_uuid': self.organization_uuid,
        }
        self.profiletype = ProfileType.objects.create(
            name='Nämé', organization_uuid=self.organization_uuid)

    def test_delete_successfully(self):
        request = self.factory.delete('', {})
        request.session = self.session
        view = ProfileTypeViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=self.profiletype.pk)
        self.assertEqual(response.status_code, 204)
        self.assertRaises(
            ProfileType.DoesNotExist,
            ProfileType.objects.get,
            pk=self.profiletype.pk)

    def test_delete_not_allowed(self):
        request = self.factory.delete('', {})
        request.session = {
            'jwt_organization_uuid': str(uuid.uuid4()),
        }
        view = ProfileTypeViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=self.profiletype.pk)
        self.assertEqual(response.status_code, 404)
        self.assertTrue(
            ProfileType.objects.filter(pk=self.profiletype.pk).exists())

    def test_delete_missing_auth(self):
        request = self.factory.delete('', {})
        view = ProfileTypeViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=self.profiletype.pk)
        self.assertEqual(response.status_code, 403)


# ############
# SiteProfile

class SiteProfileOptionsViewsTest(TestCase):
    def test_options(self):
        response = self.client.options(reverse('location:siteprofile-list'))
        self.assertIn(
            b'"name":"Site Profile List"',
            response.content)


class SiteProfileListViewsTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.organization_uuid = str(uuid.uuid4())
        self.session = {
            'jwt_organization_uuid': self.organization_uuid,
        }

    def test_list_empty(self):
        uuid_other = uuid.uuid4()
        profiletype_other = ProfileType.objects.create(
            name='ProfileType',
            organization_uuid=uuid_other)
        SiteProfile.objects.create(
            name=f'Not showing',
            profiletype=profiletype_other,
            organization_uuid=uuid_other)

        request = self.factory.get('')
        request.session = self.session
        view = SiteProfileViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 0)
        self.assertIsNone(response.data['next'])
        self.assertIsNone(response.data['previous'])

    def test_list_ordering_default(self):
        profiletype = ProfileType.objects.create(
            name='ProfileType',
            organization_uuid=self.organization_uuid)
        for name in ('B', 'A', 'C'):
            SiteProfile.objects.create(
                name=f'{name}-Ñáme',
                address_line1=f'{name}-al1',
                profiletype=profiletype,
                organization_uuid=self.organization_uuid)

        request = self.factory.get('')
        request.session = self.session
        view = SiteProfileViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 3)
        self.assertNotIn('id', response.data['results'][0])
        self.assertEqual(response.data['results'][0]['name'], 'A-Ñáme')
        self.assertEqual(response.data['results'][0]['address_line1'], 'A-al1')
        self.assertEqual(response.data['results'][1]['name'], 'B-Ñáme')
        self.assertEqual(response.data['results'][1]['address_line1'], 'B-al1')
        self.assertEqual(response.data['results'][2]['name'], 'C-Ñáme')
        self.assertEqual(response.data['results'][2]['address_line1'], 'C-al1')

    def test_list_ordering_by_name_desc(self):
        profiletype = ProfileType.objects.create(
            name='ProfileType',
            organization_uuid=self.organization_uuid)
        for name in ('B', 'A', 'C'):
            SiteProfile.objects.create(
                name=f'{name}-Ñáme',
                profiletype=profiletype,
                organization_uuid=self.organization_uuid)

        request = self.factory.get('?ordering=-name')
        request.session = self.session
        view = SiteProfileViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 3)
        self.assertEqual(response.data['results'][0]['name'], 'C-Ñáme')
        self.assertEqual(response.data['results'][1]['name'], 'B-Ñáme')
        self.assertEqual(response.data['results'][2]['name'], 'A-Ñáme')

    def test_list_filtering_by_profiletype(self):
        profiletypes = []
        for name in ('A', ' B'):
            profiletypes.append(ProfileType.objects.create(
                name=f'{name}-pt',
                organization_uuid=self.organization_uuid))
        SiteProfile.objects.bulk_create([
            SiteProfile(
                name='A-Show',
                profiletype=profiletypes[0],
                organization_uuid=self.organization_uuid),
            SiteProfile(
                name='B-Show',
                profiletype=profiletypes[0],
                organization_uuid=self.organization_uuid),
            SiteProfile(
                name='No display',
                profiletype=profiletypes[1],
                organization_uuid=self.organization_uuid),
        ])

        request = self.factory.get(f'?profiletype__id={profiletypes[0].id}')
        request.session = self.session
        view = SiteProfileViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['name'], 'A-Show')
        self.assertEqual(response.data['results'][1]['name'], 'B-Show')

    def test_list_missing_organization_uuid(self):
        request = self.factory.get('')
        request.session = {}
        view = SiteProfileViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 403)

    def test_list_profiletype_anonymoususer(self):
        request = self.factory.get('')
        view = SiteProfileViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 403)

    def test_list_siteprofiles_pagination_limit(self):
        mfactories.SiteProfile.create_batch(
            size=51, **{'organization_uuid': self.organization_uuid})
        request = self.factory.get('')
        request.session = self.session
        view = SiteProfileViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 50)
        self.assertEqual(response.data['next'], 'http://testserver/?limit=50&offset=50')


class SiteProfileCreateViewsTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.organization_uuid = str(uuid.uuid4())
        self.session = {
            'jwt_organization_uuid': self.organization_uuid,
        }

    def test_create_successfully_minimal(self):
        profiletype = ProfileType.objects.create(
            name='any', organization_uuid=self.organization_uuid)

        data = {
            'country': 'ES',
            'profiletype': profiletype.pk,
        }
        request = self.factory.post('', data)
        request.session = self.session
        view = SiteProfileViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, 201)

        siteprofile = SiteProfile.objects.get(uuid=str(response.data['uuid']))
        self.assertEqual(siteprofile.country, data['country'])
        self.assertEqual(siteprofile.profiletype.pk, data['profiletype'])

    def test_create_successfully(self):
        profiletype = ProfileType.objects.create(
            name='any', organization_uuid=self.organization_uuid)

        data = {
            'uuid': str(uuid.uuid4()),
            'name': 'Námê',
            'profiletype': profiletype.pk,
            'address_line1': 'ÁddL1',
            'address_line2': 'ÁddL2',
            'address_line3': 'ÁddL3',
            'address_line4': 'ÁddL4',
            'postcode': '10115',
            'city': 'Berlin',
            'country': 'DE',
            'administrative_level1': 'ÄdmL1',
            'administrative_level2': 'ÄdmL2',
            'administrative_level3': 'ÄdmL3',
            'administrative_level4': 'ÄdmL4',
            'latitude': '52.5200',
            'longitude': '13.4050',
            'notes': 'Nótés',
        }
        request = self.factory.post('', data)
        request.session = self.session
        view = SiteProfileViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, 201)

        siteprofile = SiteProfile.objects.get(uuid=str(response.data['uuid']))
        self.assertNotEqual(str(siteprofile.uuid), data['uuid'],
                            'UUID should be ignored and autogenerated on save')
        for field in data.keys():
            if field in ('uuid', 'profiletype'):
                continue
            elif field in ('latitude', 'longitude'):
                self.assertEqual(getattr(siteprofile, field),
                                 Decimal(data.get(field)))
            else:
                self.assertEqual(getattr(siteprofile, field), data.get(field))
        self.assertEqual(siteprofile.profiletype.pk, data['profiletype'])

    def test_create_denied_profiletype_different_org(self):
        profiletype = ProfileType.objects.create(
            name='any', organization_uuid=uuid.uuid4())

        data = {
            'country': 'ES',
            'profiletype': profiletype.pk,
        }
        request = self.factory.post('', data)
        request.session = self.session
        view = SiteProfileViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            str(response.data['profiletype'][0]),
            'Invalid ProfileType. It should belong to your organization')

    def test_create_missing_param(self):
        request = self.factory.post('', {})
        request.session = self.session
        view = SiteProfileViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(str(response.data['country'][0]),
                         'This field is required.')

    def test_create_missing_auth(self):
        request = self.factory.post('', {})
        view = SiteProfileViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, 403)


class SiteProfileUpdateViewsTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.organization_uuid = str(uuid.uuid4())
        self.session = {
            'jwt_organization_uuid': self.organization_uuid,
        }
        self.profiletype = ProfileType.objects.create(
            name='Nämé', organization_uuid=self.organization_uuid)
        self.siteprofile = SiteProfile.objects.create(
            name='Initial Námë',
            profiletype=self.profiletype,
            organization_uuid=self.organization_uuid)

    def test_update_successfully(self):
        data = {
            'uuid': str(uuid.uuid4()),
            'name': 'Námê Updated',
            'country': 'ES',
            'profiletype': self.profiletype.pk,
        }
        request = self.factory.post('', data)
        request.session = self.session
        view = SiteProfileViewSet.as_view({'post': 'update'})
        response = view(request, pk=self.siteprofile.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['country'], data['country'])

    def test_update_missing_params(self):
        request = self.factory.post('', {})
        request.session = self.session
        view = SiteProfileViewSet.as_view({'post': 'update'})
        response = view(request, pk=self.siteprofile.pk)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(str(response.data['country'][0]),
                         'This field is required.')

    def test_update_missing_auth(self):
        request = self.factory.post('', {})
        view = SiteProfileViewSet.as_view({'post': 'update'})
        response = view(request, pk=self.siteprofile.pk)
        self.assertEqual(response.status_code, 403)


class SiteProfileDeleteViewsTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.organization_uuid = str(uuid.uuid4())
        self.session = {
            'jwt_organization_uuid': self.organization_uuid,
        }
        profiletype = ProfileType.objects.create(
            name='Nämé', organization_uuid=self.organization_uuid)
        self.siteprofile = SiteProfile.objects.create(
            profiletype=profiletype,
            organization_uuid=self.organization_uuid)

    def test_delete_successfully(self):
        request = self.factory.delete('', {})
        request.session = self.session
        view = SiteProfileViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=self.siteprofile.pk)
        self.assertEqual(response.status_code, 204)
        self.assertRaises(
            SiteProfile.DoesNotExist,
            SiteProfile.objects.get,
            pk=self.siteprofile.pk)

    def test_delete_not_allowed(self):
        request = self.factory.delete('', {})
        request.session = {
            'jwt_organization_uuid': str(uuid.uuid4()),
        }
        view = SiteProfileViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=self.siteprofile.pk)
        self.assertEqual(response.status_code, 404)
        self.assertTrue(
            SiteProfile.objects.filter(pk=self.siteprofile.pk).exists())

    def test_delete_missing_auth(self):
        request = self.factory.delete('', {})
        view = SiteProfileViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=self.siteprofile.pk)
        self.assertEqual(response.status_code, 403)
