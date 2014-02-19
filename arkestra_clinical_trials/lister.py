import operator
from datetime import datetime, timedelta

from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from arkestra_utilities.generic_lister import (
    ArkestraGenericLister, ArkestraGenericFilterList, ArkestraGenericFilterSet
    )

from arkestra_utilities.settings import (
    NEWS_AND_EVENTS_LAYOUT, LISTER_MAIN_PAGE_LIST_LENGTH,
    AGE_AT_WHICH_ITEMS_EXPIRE, MULTIPLE_ENTITY_MODE
    )

from .models import ClinicalTrial


class ClinicalTrialsFilterSet(ArkestraGenericFilterSet):
    fields = ['date']


class ClinicalTrialsList(ArkestraGenericFilterList):
    model = ClinicalTrial
    search_fields = [
        {
            "field_name": "text",
            "field_label": "Search title/summary",
            "placeholder": "Search",
            "search_keys": [
                "title__icontains",
                "summary__icontains",
                ],
            },
        ]


class ClinicalTrialsLister(ArkestraGenericLister):
    listkinds = [("clinicaltrials", ClinicalTrialsList)]
    display = "clinicaltrials"


# class ClinicalTrialsMenuLister(ArkestraGenericLister):
#     listkinds = [
#         ("clinicaltrials", ClinicalTrialsListCurrent),
#         ]
#     display = "clinical trials"
#     limit_to = LISTER_MAIN_PAGE_LIST_LENGTH
#

