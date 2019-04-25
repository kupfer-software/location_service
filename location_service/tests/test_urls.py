import uuid

from django.test import TestCase
from django.urls import reverse


class ProfileTypeOptionsViewsTest(TestCase):
    def setUp(self) -> None:
        session = self.client.session
        session['jwt_organization_uuid'] = str(uuid.uuid4())
        session.save()

    def test_get_docs_swagger_ui(self):
        # reverse() would be better
        response = self.client.get(reverse('docs-swagger-ui'))
        self.assertEqual(response.status_code, 200)

    def test_get_docs_swagger_raw(self):
        # reverse() would be better
        response = self.client.get('/docs/swagger.json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Location Service', str(response.content))

        # reverse() would be better
        response = self.client.get('/docs/swagger.yaml')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'title: Location Service API', response.content)
