import operator
from datetime import datetime, timedelta

from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from arkestra_utilities.generic_lister import (
    ArkestraGenericLister, ArkestraGenericList, ArkestraGenericFilterList,
    ArkestraGenericFilterSet
    )

from arkestra_utilities.settings import (
    NEWS_AND_EVENTS_LAYOUT, LISTER_MAIN_PAGE_LIST_LENGTH,
    AGE_AT_WHICH_ITEMS_EXPIRE, MULTIPLE_ENTITY_MODE
    )

from .models import Trial


class TrialsFilterSet(ArkestraGenericFilterSet):
    fields = ["date", "status", "trialtype"]


class TrialsList(ArkestraGenericFilterList):
    filter_set = TrialsFilterSet
    model = Trial
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


class TrialsLister(ArkestraGenericLister):
    listkinds = [("trials", TrialsList)]
    display = "trials"

class TrialsMenuList(ArkestraGenericList):
    model = Trial
    heading_text = _(u"News")


class TrialsMenuLister(ArkestraGenericLister):
    listkinds = [("trials", TrialsMenuList)]
    display = "trials"




# class TrialsMenuLister(ArkestraGenericLister):
#     listkinds = [
#         ("Trials", TrialsListCurrent),
#         ]
#     display = "clinical trials"
#     limit_to = LISTER_MAIN_PAGE_LIST_LENGTH
#

