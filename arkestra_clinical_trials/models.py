from datetime import datetime

from django.db import models

from cms.models.fields import PlaceholderField

from contacts_and_people.models import Person, Entity

from arkestra_utilities.generic_models import (
    ArkestraGenericModel
    )
from arkestra_utilities.mixins import URLModelMixin


class ClinicalTrial(ArkestraGenericModel, URLModelMixin):
    url_path = "clinical-trial"

    date = models.DateField(
        "Start date",
        default=datetime.now,
        )

    end_date = models.DateField(null=True, blank=True)

    chief_investigators = models.ManyToManyField(
        Person,
        related_name='%(class)s_chief_investigators',
        null=True, blank=True
        )

    trial_managers = models.ManyToManyField(
        Person,
        related_name='%(class)s_trial_managers',
        null=True, blank=True
        )

    funding_body = models.ManyToManyField(
        Entity, verbose_name="Funding body",
        null=True, blank=True,
        related_name="%(class)s_funding_bodies",
        )

    sponsor = models.ManyToManyField(
        Entity, verbose_name="Sponsor",
        null=True, blank=True,
        related_name="%(class)s_sponsors",
        )

    STATUSES = (
        ("setup", "In setup"),
        ("recruiting", "Recruiting"),
        ("running", "Running"),
        ("closed", "Closed"),
        )

    status = models.CharField(
        "Status",
        max_length=25,
        choices=STATUSES, default="setup"
        )

    grant_value = models.CharField(
        max_length=25,
        null=True, blank=True,
    )


class ClinicalTrialEntity(models.Model):

    #one-to-one link to contacts_and_people.Person
    entity = models.OneToOneField(
        'contacts_and_people.Entity',
        primary_key=True, related_name="clinical_trial_entity",
        help_text=
        """
        Do not under any circumstances change this field. No, really. Don't
        touch this.
        """
        )
    publish_page = models.BooleanField(
        u"Publish an automatic clinical trials page",
        default=False,
        )
    menu_title = models.CharField(
        u"Title",
        max_length=50,
        default="Clinical trials"
        )
    # clinical_trials_page_intro = PlaceholderField(
    #     'body',
    #     related_name="clinical_trials_page_intro",
    #     )
