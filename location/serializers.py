from rest_framework import serializers
from django_countries.serializer_fields import CountryField
from django_countries import Countries

from . import models


class ProfileTypeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    organization_uuid = serializers.CharField(
        required=False,
        help_text='Any value sent will be ignored and will be just taken '
                  'from JWT payload')

    class Meta:
        model = models.ProfileType
        fields = '__all__'


class CountriesWithBlank(Countries):
    """Add empty Country for having the blank choice in the swagger docs."""
    override = [
        ('', ''),
    ]


class SiteProfileSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()
    organization_uuid = serializers.CharField(
        required=False,
        help_text='Any value sent will be ignored and will be just taken '
                  'from JWT payload')
    country = CountryField(required=False, countries=CountriesWithBlank())

    class Meta:
        model = models.SiteProfile
        fields = '__all__'

    def validate_profiletype(self, value):
        if (self.initial_data['organization_uuid'] !=
                str(value.organization_uuid)):
            raise serializers.ValidationError(
                'Invalid ProfileType. It should belong to your organization')
        return value

    def validate(self, attrs):
        """Validate that at least one of the defined fields is filled."""
        one_of_required_fields = (
            'name',
            'country',
            'city',
            'latitude',
            'longitude',
            'address_line1',
            'address_line2',
            'address_line3',
            'address_line4',
        )
        if not set(one_of_required_fields).intersection(attrs.keys()):
            raise serializers.ValidationError(f'One of {one_of_required_fields} must be defined.')
        return super().validate(attrs)
