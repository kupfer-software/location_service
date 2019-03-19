from django.contrib import admin
from .models import ProfileType, SiteProfile


class SiteProfileAdmin(admin.ModelAdmin):
    list_display = ('uuid',
                    'organization_uuid',
                    'workflowlevel2_uuid',
                    'name',
                    'address_line1',
                    'address_line2',
                    'address_line2',
                    'address_line4',
                    'city',
                    'create_date',
                    'edit_date')
    list_filter = ('organization_uuid', )
    search_fields = ('uuid',
                     'organization_uuid',
                     'workflowlevel2_uuid',
                     'name',
                     'address_line1',
                     'address_line2',
                     'address_line2',
                     'address_line4',
                     'city', )


admin.site.register(ProfileType)
admin.site.register(SiteProfile, SiteProfileAdmin)
