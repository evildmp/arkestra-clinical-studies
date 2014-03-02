from django.conf.urls.defaults import patterns, url

from arkestra_clinical_trials import views

urlpatterns = patterns('arkestra_clinical_trials.views',

    # the view for a particular clinical trial
    url(
        r"^clinical-trial/(?P<slug>[-\w]+)/$",
        view="clinical_trial",
        name="clinical-trial"
        ),

    # list of clinical trials (in "archive" view, i.e. the list will be
    # paginated, filtered and searchable) for a named entity, e.g.
    # haematology/clinicaltrials
    url(
        r"^clinical-trials/(?:(?P<slug>[-\w]+)/)$",
        views.TrialsArchiveView.as_view(),
        name="clinical-trials"
        ),

    # the same list, where no entity is given in the url
    url(
        r'^clinical-trials/$',
        views.TrialsArchiveView.as_view(),
        {"slug": None},
        name="clinical-trials-base"
        ),
    )
