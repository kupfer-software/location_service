import uuid

from factory import DjangoModelFactory, Iterator, SubFactory

from ..models import ProfileType as ProfileTypeM, SiteProfile as SiteProfileM


class ProfileType(DjangoModelFactory):
    organization_uuid = str(uuid.uuid4())

    class Meta:
        model = ProfileTypeM


class SiteProfile(DjangoModelFactory):
    profiletype = SubFactory(ProfileType)
    country = Iterator(['ES', 'GB', 'DE'])
    organization_uuid = str(uuid.uuid4())
    workflowlevel2_uuid = [str(uuid.uuid4())]

    class Meta:
        model = SiteProfileM
