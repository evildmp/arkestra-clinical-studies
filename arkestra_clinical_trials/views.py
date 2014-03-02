from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from arkestra_utilities.views import ArkestraGenericView

from models import Trial

from .lister import TrialsLister


class TrialsArchiveView(ArkestraGenericView):
    auto_page_attribute = "ddd"

    def get(self, request, *args, **kwargs):
        self.get_entity()

        self.lister = TrialsLister(
            entity=self.entity,
            request=self.request
            )

        self.main_page_body_file = "arkestra/generic_filter_list.html"
        self.meta = {"description": "Searchable archive of clinical trials"}
        self.title = u"Clinical trials archive for %s" % unicode(self.entity)
        self.pagetitle = u"Clinical trials archive for %s" % unicode(self.entity)

        return self.response(request)


def clinical_trial(request, slug):
    """
    Responsible for publishing news article
    """
    if request.user.is_staff:
        trial = get_object_or_404(Trial, slug=slug)
    else:
        trial = get_object_or_404(
            Trial,
            slug=slug,
            published=True,
            )

    return render_to_response(
        "clinical_trials/trial.html", {
            "trial": trial,
            "entity": trial.get_hosted_by,
            "meta": {"description": trial.summary}
        },
        RequestContext(request),
    )
