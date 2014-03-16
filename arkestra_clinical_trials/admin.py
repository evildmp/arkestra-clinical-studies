from django.contrib import admin

# these aren't all in fact mixins (it's misnamed) but they are useful
# building blocks for the admin interface we'll create
from arkestra_utilities.admin_mixins import (
    WidgetifiedModelAdmin,
    GenericModelForm,
    fieldsets,
    SupplyRequestMixin
    )

# the PhoneContactInline is available from contacts_and_people
from contacts_and_people.admin import PhoneContactInline

# for the links tab
from links.admin import ObjectLinkInline

from .models import Trial, TrialEntity, TrialType


# on the modelform for Trials we inherit from GenericModelForm
# so we need to override the labels and help_text on a few fields
class TrialsForm(GenericModelForm):
    def __init__(self, *args, **kwargs):
        super(TrialsForm, self).__init__(*args, **kwargs)

        self.fields["please_contact"].label = "Trial managers"
        self.fields["hosted_by"].label = "Published by"

        self.fields["title"].help_text = "e.g. POETIC"
        self.fields["expanded_title"].help_text = """
            e.g. Point of Care Testing for Urinary Tract Infections In
            Primary care
            """
        self.fields["short_title"].help_text = """
            If necessary, a shorter version of the Title
            """
        self.fields["summary"].help_text = """
            e.g. POETIC is part of a larger study, R-GNOSIS, and
            funded by the EU Seventh Framework Programme (FP7).
            """


# WidgetifiedModelAdmin provides some hooks and widgets for the more
# fully-featured admin, such as tabs, autocomplete search
# There's also a GenericModelAdmin available, but in this case we happen to
# override all the attributes it sets, so there's no point
class TrialAdmin(WidgetifiedModelAdmin):
    form = TrialsForm

    # these fieldsets are already defined, but we need to change them
    fieldsets["people"] = ['', {'fields': [
        'please_contact',
        'chief_investigators',
        ]}]
    fieldsets["basic"] = ['', {'fields': [
        'title',
        'expanded_title',
        'short_title',
        'summary',
        'isrctn',
        'nct',
        'grant_value',
        'status',
        'trialtype',
        ]}]

    # this is an entirely new fieldset
    fieldsets["entities"] = ['', {'fields': [
        'sponsor',
        'funding_body',
        'clinical_centre',
        ]}]
    # define the tabs for the admin
    tabs = (
        ['Basic', {
            'fieldsets': (
                fieldsets["basic"],
                fieldsets["host"],
                fieldsets["image"],
                fieldsets["publishing_control"],
            ),
        }],
        ('Contact information', {
            'fieldsets': (fieldsets["email"],),
            'inlines': [PhoneContactInline,]
            }),
        ['When', {'fieldsets': [
            ['', {'fields': ['date', 'end_date']}]]
        }],
        ['Body', {'fieldsets': [fieldsets["body"]]}],
        ['Sponsors & funders', {'fieldsets': [fieldsets["entities"]]}],
        ['Related people', {'fieldsets': [fieldsets["people"]]}],
        ['Where to Publish', {'fieldsets': [fieldsets["where_to_publish"]]}],
        ('Links', {'inlines': (ObjectLinkInline,),}),
        ['Advanced Options', {'fieldsets': [
            fieldsets["url"],  fieldsets["slug"]
            ]
        }],
    )

    filter_horizontal = (
        'please_contact',
        'chief_investigators',
        'publish_to',
        'sponsor',
        'funding_body',
        'clinical_centre',
        'trialtype',
        )

    search_fields = ['title', 'expanded_title', 'short_title']
    prepopulated_fields = {'slug': ['title']}

    # autocomplete search fields
    related_search_fields = ['hosted_by', 'external_url']


class TrialsEntityAdmin(WidgetifiedModelAdmin):

    basic_fieldset = [None, {'fields': [
        'entity',
        'publish_page',
        'menu_title',
        ]}]
    page_intro_fieldset = [None, {
        'fields': ['trials_page_intro'],
        'classes': ['plugin-holder', 'plugin-holder-nopage']
        }]

    list_display = ('entity', 'publish_page')

    tabs = [
        ['Basic', {'fieldsets': [basic_fieldset]}],
        ["Page introduction", {'fieldsets': [page_intro_fieldset]}],
        ]
    search_fields = ['entity']
    related_search_fields = ['entity']

admin.site.register(Trial, TrialAdmin)
admin.site.register(TrialEntity, TrialsEntityAdmin)
admin.site.register(TrialType)
