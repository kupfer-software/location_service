import uuid

from django.core.exceptions import ValidationError
from django.test import TestCase

from ..models import ProfileType, SiteProfile


class ProfileTypeTest(TestCase):
    def test_save_profiletype(self):
        data = {
            'name': 'home',
            'organization_uuid': uuid.uuid4(),
        }
        ProfileType.objects.create(**data)
        ProfileType.objects.get(**data)

    def test_save_profiletype_not_valid(self):
        profiletype = ProfileType()
        self.assertRaises(ValidationError, profiletype.full_clean)

        profiletype = ProfileType(name='home')
        self.assertRaises(ValidationError, profiletype.full_clean)

        profiletype = ProfileType(organization_uuid=uuid.uuid4())
        self.assertRaises(ValidationError, profiletype.full_clean)

        profiletype = ProfileType(name='home', organization_uuid='fake')
        self.assertRaises(ValidationError, profiletype.full_clean)


class SiteProfileTest(TestCase):
    def setUp(self):
        self.profiletype = ProfileType.objects.create(
            name='home', organization_uuid=uuid.uuid4())

    def test_save_siteprofile(self):
        SiteProfile.objects.create(
            profiletype=self.profiletype,
            organization_uuid=uuid.uuid4())

    def test_save_siteprofile_germany(self):
        SiteProfile.objects.create(
            profiletype=self.profiletype,
            # https://en.wikipedia.org/wiki/Address#Germany
            address_line1='Humanitec GmBH',
            address_line2='Human Resources',
            address_line3='Wöhlertstraße 12',
            address_line4='10115 Berlin',
            postcode='10115',
            city='Berlin',
            country='DE',
            # https://en.wikipedia.org/wiki/List_of_administrative_divisions_by_country
            administrative_level1='Berlin',  # Land (Federal state)
            administrative_level2='Berlin',  # Kreis
            administrative_level3='',  # Gemeinde (Municipalities)
            #
            latitude='51.1657',
            longitude='10.4515',
            notes='Hinterhof',
            organization_uuid=uuid.uuid4())

    def test_save_siteprofile_spain(self):
        SiteProfile.objects.create(
            profiletype=self.profiletype,
            # https://en.wikipedia.org/wiki/Address#Spain
            address_line1='Hotel Yaramar',
            address_line2='Paseo Marítimo Rey de España, 64',
            address_line3='29640 Fuengirola',
            address_line4='Málaga',
            postcode='29640',
            city='Fuengirola',
            country='ES',
            # https://en.wikipedia.org/wiki/List_of_administrative_divisions_by_country
            administrative_level1='Andalucía',  # Comunidad Autónoma
            administrative_level2='Málaga',  # Provincia
            administrative_level3='Costa del Sol',  # Comarca
            administrative_level4='Fuengirola',  # Municipio
            #
            latitude='40.4637',
            longitude='3.7492',
            notes='Patio interior',
            organization_uuid=uuid.uuid4(),
            workflowlevel2_uuid=[uuid.uuid4()],)
