from django.db.models import Q
from django_filters import rest_framework as django_filters

from location.models import SiteProfile


class BaseInArrayFilter(django_filters.BaseInFilter):

    def filter(self, qs, value):
        if not value:
            return qs
        params = Q()
        for item in value:
            params |= Q(**{f'{self.field_name}__contains': [item, ]})
        return qs.filter(params)


class SiteProfileFilter(django_filters.FilterSet):
    workflowlevel2_uuid = BaseInArrayFilter()

    class Meta:
        model = SiteProfile
        fields = ('profiletype__id',)
