from django.db import models

from contacts_and_people.models import Person, Entity

from arkestra_utilities.generic_models import (
    ArkestraGenericModel
    )


class ClinicalTrial(ArkestraGenericModel):

    date = models.DateField(
        "Start date",
        null=True, blank=True,
        )

    end_date = models.DateField(null=True, blank=True)

    please_contact = models.ManyToManyField(
        "Trial managers",
        Person,
        related_name='%(class)s_person',
        null=True, blank=True
        )

    chief_investigators = models.ManyToManyField(
        Person,
        related_name='%(class)s_person',
        null=True, blank=True
        )

    publish_to = models.ManyToManyField(
        Entity, verbose_name="Also involved",
        null=True, blank=True,
        related_name="%(class)s_publish_to",
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
        ("setup", "In setup")
        ("recruiting", "Recruiting")
        ("running", "Running")
        ("closed", "Closed")
        )
