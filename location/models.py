from decimal import Decimal
import uuid

from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.indexes import GinIndex
from django.db import models
from django_countries.fields import CountryField


class ProfileType(models.Model):
    name = models.CharField(max_length=255)
    organization_uuid = models.UUIDField('Organization UUID', db_index=True)
    create_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)


class SiteProfile(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, blank=True)
    profiletype = models.ForeignKey(ProfileType, on_delete=models.CASCADE, blank=True, null=True)
    address_line1 = models.CharField('Address line 1', max_length=255, blank=True)
    address_line2 = models.CharField('Address line 2', max_length=255, blank=True)
    address_line3 = models.CharField('Address line 3', max_length=255, blank=True)
    address_line4 = models.CharField('Address line 4', max_length=255, blank=True)
    postcode = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=85, blank=True)
    country = CountryField(blank=True, null=True)
    administrative_level1 = models.CharField('Administrative division (First level)', max_length=255, blank=True)
    administrative_level2 = models.CharField('Administrative division (Second level)', max_length=255, blank=True)
    administrative_level3 = models.CharField('Administrative division (Third level)', max_length=255, blank=True)
    administrative_level4 = models.CharField('Administrative division (Fourth level)', max_length=255, blank=True)
    latitude = models.DecimalField(decimal_places=16, max_digits=25, blank=True, default=Decimal('0.00'), help_text='Latitude (Decimal Coordinates)')
    longitude = models.DecimalField(decimal_places=16, max_digits=25, blank=True, default=Decimal('0.00'), help_text='Longitude (Decimal Coordinates)')
    notes = models.TextField(blank=True)

    organization_uuid = models.UUIDField('Organization UUID', db_index=True)
    create_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)

    workflowlevel2_uuid = ArrayField(
        models.UUIDField(), blank=True, null=True,
        help_text='List of WorkflowLevel2s')

    class Meta:
        indexes = [
            GinIndex(fields=['workflowlevel2_uuid'])
        ]
