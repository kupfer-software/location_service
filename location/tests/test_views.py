import uuid

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory

from ..models import ProfileType
from ..views import ProfileTypeViewSet


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
