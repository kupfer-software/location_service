from decimal import Decimal
import uuid

from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.indexes import GinIndex
from django.db import models
from django_countries.fields import CountryField


class ProfileType(models.Model):
    """
    ProfileType helps grouping SiteProfiles together. For example, a
    ProfileType called 'billing' can be created to classify all billing
    addresses stored.
    """
    name = models.CharField(max_length=255, help_text='Name of the ProfileType.')
    organization_uuid = models.UUIDField('Organization UUID', db_index=True, help_text='ID of the organization that has access to the ProfileType.')
    create_date = models.DateTimeField(auto_now_add=True, help_text='Timestamp when the SiteProfile was created (automatically set, ISO format).')
    edit_date = models.DateTimeField(auto_now=True, help_text='Timestamp when the SiteProfile was last modified (automatically set, ISO format).')
    is_global = models.BooleanField(default=False, help_text="All organizations have access to global ProfileTypes.")


class SiteProfile(models.Model):
    """
    SiteProfile can be used to store any international address thanks to the
    flexible schema provided.

    For listing objects, there is a `profiletype__id` filter to be used in
    the querystring.
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text='UUID of the SiteProfile.')
    name = models.CharField(max_length=255, blank=True, help_text='Name of the SiteProfile.')
    profiletype = models.ForeignKey(ProfileType, on_delete=models.CASCADE, blank=True, null=True, help_text='UUID of the related ProfileType of the SiteProfile.')
    address_line1 = models.CharField('Address line 1', max_length=255, blank=True, help_text='First line of the SiteProfile\'s address, like street and number.')
    address_line2 = models.CharField('Address line 2', max_length=255, blank=True, help_text='Second line of the SiteProfile\'s address')
    address_line3 = models.CharField('Address line 3', max_length=255, blank=True, help_text='Third line of the SiteProfile\'s address')
    address_line4 = models.CharField('Address line 4', max_length=255, blank=True, help_text='Fourth line of the SiteProfile\'s address')
    postcode = models.CharField(max_length=20, blank=True, help_text='Postal code where the SiteProfile is located')
    city = models.CharField(max_length=85, blank=True, help_text='City where the SiteProfile is located')
    country = CountryField(blank=True, help_text="two-char ISO code")
    administrative_level1 = models.CharField('Administrative division (First level)', max_length=255, blank=True)
    administrative_level2 = models.CharField('Administrative division (Second level)', max_length=255, blank=True)
    administrative_level3 = models.CharField('Administrative division (Third level)', max_length=255, blank=True)
    administrative_level4 = models.CharField('Administrative division (Fourth level)', max_length=255, blank=True)
    latitude = models.DecimalField(decimal_places=16, max_digits=25, blank=True, default=Decimal('0.00'), help_text='Latitude coordinates of the SiteProfile (decimal format)')
    longitude = models.DecimalField(decimal_places=16, max_digits=25, blank=True, default=Decimal('0.00'), help_text='Longitude coordinates of the SiteProfile (decimal format)')
    notes = models.TextField(blank=True, help_text='Textual notes for the SiteProfile')

    organization_uuid = models.UUIDField('Organization UUID', db_index=True, help_text='UUID of the organization that has access to the SiteProfile')
    create_date = models.DateTimeField(auto_now_add=True, help_text='Timestamp when the SiteProfile was created (set automatically, ISO format)')
    edit_date = models.DateTimeField(auto_now=True, help_text='Timestamp when the SiteProfile was last modified (set automatically, ISO format)')

    workflowlevel2_uuid = ArrayField(models.CharField(max_length=36), blank=True, null=True, help_text='Array of WorkflowLevel2s associated with the SiteProfile.')

    class Meta:
        indexes = [
            GinIndex(fields=['workflowlevel2_uuid'])
        ]
