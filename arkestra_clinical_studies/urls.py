from django.conf.urls.defaults import patterns, url

from arkestra_clinical_studies import views

urlpatterns = patterns('arkestra_clinical_studies.views',

    # the view for a particular clinical study
    url(
        r"^clinical-study/(?P<slug>[-\w]+)/$",
        view="clinical_study",
        name="clinical-study"
        ),

    # the view for an entity's clinical studies
    # matches "clinical-studies" and "clinical-studies/wctu"
    url(
        r"^clinical-studies/(?:(?P<slug>[-\w]+)/)?$",
        views.StudiesArchiveView.as_view(),
        name="clinical-studies"
        ),
    )

