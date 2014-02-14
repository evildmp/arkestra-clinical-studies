from django.contrib import admin

from arkestra_utilities.admin_mixins import (
    GenericModelAdmin, GenericModelForm, fieldsets
    )

from .models import ClinicalTrial


class ClinicalTrialsForm(GenericModelForm):
    pass


class ClinicalTrialAdmin(GenericModelAdmin):
    form = ClinicalTrialsForm

    tabs = (
        ['Basic', {
            'fieldsets': (
                fieldsets["basic"],
                fieldsets["host"],
                fieldsets["image"],
                fieldsets["publishing_control"],
            ),
        }],
        ['Body', {'fieldsets': [fieldsets["body"]]}],
        ['When', {'fieldsets': [
            ['', {'fields': ['date', 'end_date']}]]
        }],
        ['Where to Publish', {'fieldsets': [fieldsets["where_to_publish"]]}],
        ['Related people', {'fieldsets': [fieldsets["people"]]}],
        ['Advanced Options', {'fieldsets': [
            fieldsets["url"],  fieldsets["slug"]
            ]
        }],
    )

    related_search_fields = ['hosted_by', 'external_url']


admin.site.register(ClinicalTrial, ClinicalTrialAdmin)
