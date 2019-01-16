from rest_framework import serializers
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


class SiteProfileSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()
    organization_uuid = serializers.CharField(
        required=False,
        help_text='Any value sent will be ignored and will be just taken '
                  'from JWT payload')

    class Meta:
        model = models.SiteProfile
        fields = '__all__'

    def validate_profiletype(self, value):
        if (self.initial_data['organization_uuid'] !=
                str(value.organization_uuid)):
            raise serializers.ValidationError(
                'Invalid ProfileType. It should belong to your organization')
        return value
