from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from arkestra_utilities.views import ArkestraGenericView

from models import Study

from .lister import StudiesLister


class StudiesArchiveView(ArkestraGenericView):

    def get(self, request, *args, **kwargs):
        self.get_entity()

        self.lister = StudiesLister(
            entity=self.entity,
            request=self.request
            )

        self.main_page_body_file = "arkestra/generic_filter_list.html"
        self.meta = {"description": "Searchable archive of clinical studies"}
        self.title = u"Clinical studies archive for %s" % unicode(self.entity)
        self.pagetitle = u"Clinical studies archive for %s" % unicode(self.entity)

        return self.response(request)


def clinical_study(request, slug):
    """
    Responsible for publishing news article
    """
    if request.user.is_staff:
        study = get_object_or_404(Study, slug=slug)
    else:
        study = get_object_or_404(
            Study,
            slug=slug,
            published=True,
            )

    return render_to_response(
        "clinical_studies/study.html", {
            "study": study,
            "entity": study.get_hosted_by,
            "meta": {"description": study.summary}
        },
        RequestContext(request),
    )
