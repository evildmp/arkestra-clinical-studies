from django.conf.urls.defaults import patterns, url

from arkestra_clinical_trials import views

urlpatterns = patterns('arkestra_clinical_trials.views',

    # clinical trial items
    url(
        r"^clinical-trial/(?P<slug>[-\w]+)/$",
        view="clinical_trial",
        name="clinical-trial"
        ),

    # # main clinical trials page - named entity
    # url(
    #     r"^clinical-trials/(?:(?P<slug>[-\w]+)/)$",
    #     views.ClinicalTrialsView.as_view(),
    #     name="clinical-trials"
    #     ),
    #
    # # main clinical trials page - base entity
    # url(
    #     r"^clinical-trials/$",
    #     views.ClinicalTrialsView.as_view(),
    #     {"slug": None},
    #     name="clinical-trials-base"
    #     ),
    #
    # clinical trials archive - named entity
    url(
        r"^clinical-trials/(?:(?P<slug>[-\w]+)/)$",
        views.ClinicalTrialsArchiveView.as_view(),
        name="clinical-trials"
        ),

    # clinical trials archive - base entity
    url(
        r'^clinical-trials/$',
        views.ClinicalTrialsArchiveView.as_view(),
        {"slug": None},
        name="clinical-trials-base"
        ),
    #
    # # previous events
    # url(
    #     r"^previous-events/(?:(?P<slug>[-\w]+)/)$",
    #     views.EventsArchiveView.as_view(),
    #     name="events-archive"
    #     ),
    #
    # url(
    #     r'^previous-events/$',
    #     views.EventsArchiveView.as_view(),
    #     {"slug": None},
    #     name="events-archive-base"
    #     ),
    #
    # # forthcoming events
    # url(
    #     r"^forthcoming-events/(?:(?P<slug>[-\w]+)/)$",
    #     views.EventsForthcomingView.as_view(),
    #     name="events-forthcoming"
    #     ),
    #
    # url(
    #     r'^forthcoming-events/$',
    #     views.EventsForthcomingView.as_view(),
    #     {"slug": None},
    #     name="events-forthcoming-base"
    #     ),
    )
