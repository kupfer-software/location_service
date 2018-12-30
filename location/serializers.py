from rest_framework import serializers
from . import models


class ProfileTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProfileType
        fields = '__all__'
