from django.test import TestCase
from rest_framework.test import APIRequestFactory

from location.serializers import SiteProfileSerializer
from . import model_factories as mfactories


class LocationSerializerTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_country_field(self):
        site_profile = mfactories.SiteProfile()
        serializer = SiteProfileSerializer(site_profile)

        data = serializer.data

        keys = ('uuid',
                'organization_uuid',
                'name',
                'address_line1',
                'address_line2',
                'address_line3',
                'address_line4',
                'postcode',
                'city',
                'country',
                'administrative_level1',
                'administrative_level2',
                'administrative_level3',
                'administrative_level4',
                'latitude',
                'longitude',
                'notes',
                'create_date',
                'edit_date',
                'workflowlevel2_uuid',
                'profiletype')

        self.assertEqual(set(data.keys()), set(keys))
