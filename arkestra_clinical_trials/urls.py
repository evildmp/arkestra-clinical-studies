from django.conf.urls.defaults import patterns, url

from arkestra_clinical_trials import views

urlpatterns = patterns('arkestra_clinical_trials.views',

    # the view for a particular clinical trial
    url(
        r"^clinical-trial/(?P<slug>[-\w]+)/$",
        view="clinical_trial",
        name="clinical-trial"
        ),

    # the view for an entity's clinical trials
    # matches "clinical-trials" and "clinical-trials/wctu"
    url(
        r"^clinical-trials/(?:(?P<slug>[-\w]+)/)?$",
        views.TrialsArchiveView.as_view(),
        name="clinical-trials"
        ),
    )

