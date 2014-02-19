from django.contrib import admin

from arkestra_utilities.admin_mixins import (
    GenericModelAdmin, GenericModelForm, fieldsets
    )

from .models import ClinicalTrial, ClinicalTrialEntity


fieldsets["people"] = ['', {'fields': [
    'please_contact',
    'chief_investigators',
    'trial_managers'
    ]}]
fieldsets["sponsors"] = ['', {'fields': ['sponsor', 'funding_body']}]
fieldsets["basic"] = ['', {'fields': [
    'title',
    'short_title',
    'summary',
    'grant_value'
    ]}]

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
        ['When', {'fieldsets': [
            ['', {'fields': ['date', 'end_date']}]]
        }],
        ['Body', {'fieldsets': [fieldsets["body"]]}],
        ['Sponsors & funders', {'fieldsets': [fieldsets["sponsors"]]}],
        ['Related people', {'fieldsets': [fieldsets["people"]]}],
        ['Where to Publish', {'fieldsets': [fieldsets["where_to_publish"]]}],
        ['Advanced Options', {'fieldsets': [
            fieldsets["url"],  fieldsets["slug"]
            ]
        }],
    )

    filter_horizontal = (
        'please_contact',
        'publish_to',
        'sponsor',
        'funding_body',
        'chief_investigators',
        'trial_managers',
        )

    related_search_fields = ['hosted_by', 'external_url']
    prepopulated_fields = {'slug': ['title']}


admin.site.register(ClinicalTrial, ClinicalTrialAdmin)
admin.site.register(ClinicalTrialEntity)
