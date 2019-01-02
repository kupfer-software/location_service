from django.test import TestCase
from django.urls import reverse


class ProfileTypeOptionsViewsTest(TestCase):
    def test_get_docs_swagger_ui(self):
        response = self.client.get(reverse('docs-swagger-ui'))
        self.assertEqual(response.status_code, 200)

    def test_get_docs_swagger_raw(self):
        # I tried to use reverse(), but does not work
        response = self.client.get('/docs/swagger.json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b'"info": {"title": "Location Service API", "version": "latest"}',
            response.content)

        # I tried to use reverse(), but does not work
        response = self.client.get('/docs/swagger.yaml')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'title: Location Service API', response.content)
