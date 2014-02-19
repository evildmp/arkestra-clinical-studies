from django.utils.translation import ugettext as _
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import Http404

from arkestra_utilities.views import ArkestraGenericView

from contacts_and_people.models import Entity

from models import ClinicalTrial

from .lister import ClinicalTrialsLister
#
#
# from arkestra_utilities.settings import MULTIPLE_ENTITY_MODE
#
# class ClinicalTrialsView(ArkestraGenericView):
#     auto_page_attribute = "auto_clinical_trials__page"
#
#     def get(self, request, *args, **kwargs):
#         self.get_entity()
#
#         self.lister = ClinicalTrialsCurrentLister(
#             entity=self.entity,
#             request=self.request
#             )
#
#         self.main_page_body_file = "arkestra/generic_lister.html"
#         self.meta = {"description": "Current clinical trials",}
#         self.title = unicode(self.entity) + u" clinical trials"
#         if MULTIPLE_ENTITY_MODE:
#             self.pagetitle = unicode(self.entity) + u" clinical trials"
#         else:
#             self.pagetitle = "Clinical trials"
#
#         return self.response(request)
#
class ClinicalTrialsArchiveView(ArkestraGenericView):

    def get(self, request, *args, **kwargs):
        self.get_entity()

        self.lister = ClinicalTrialsLister(
            entity=self.entity,
            request=self.request
            )

        self.main_page_body_file = "arkestra/generic_filter_list.html"
        self.meta = {"description": "Searchable archive of clinical trials",}
        self.title = u"Clinical trials archive for %s" % unicode(self.entity)
        self.pagetitle = u"Clinical trials archive for %s" % unicode(self.entity)

        return self.response(request)

def clinical_trial(request, slug):
    """
    Responsible for publishing news article
    """
    if request.user.is_staff:
        clinicaltrial = get_object_or_404(ClinicalTrial, slug=slug)
    else:
        clinicaltrial = get_object_or_404(
            ClinicalTrial,
            slug=slug,
            published=True,
            )
    return render_to_response(
        "clinical_trials/clinicaltrial.html",
        {
        "clinicaltrial":clinicaltrial,
        "entity": clinicaltrial.get_hosted_by,
        "meta": {"description": clinicaltrial.summary,}
        },
        RequestContext(request),
    )
