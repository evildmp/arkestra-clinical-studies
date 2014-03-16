from django.db import models
from django.contrib.contenttypes import generic
from django.core.validators import RegexValidator

# PlaceholderField is required so we can use django CMS plugins
from cms.models.fields import PlaceholderField

# all the useful fields and methods of the generic model
from arkestra_utilities.generic_models import ArkestraGenericModel

# url fields and methods; mechanisms for referirng to external trials
from arkestra_utilities.mixins import URLModelMixin

# for the relationships to people and entities
from contacts_and_people.models import Person, Entity, PhoneContact


# types will typcially include: "first human", "randomised", etc
class TrialType(models.Model):
    name = models.CharField(
        u"Name",
        max_length=100
        )

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["name"]


# The Trial model describes a clinical trial
# It sub-classes ArkestraGenericModel and URLModelMixin - see the
# ArkestraGenericModel and URLModelMixin for more on what they provide
class Trial(ArkestraGenericModel, URLModelMixin):
    # the get_absolute_url() of URLModelMixin needs to know the view_name
    view_name = "clinical-trial"

    # the link_to_more() method of the ArkestraGenericModel needs to know
    # where we can find more of these items - this *must* match the view name in
    # urls
    auto_page_view_name = "clinical-trials"

    # the ArkestraGenericModel already provides a title and optional
    # short_title; a clinical trial may not use the latter but will
    # usually have an expanded_title too
    expanded_title = models.CharField(
        max_length=255, null=True, blank=True,
        help_text=u"e.g. Man bites dog (if blank, will be copied from Title)"
        )

    isrctn = models.PositiveIntegerField(
        verbose_name="ISRCTN",
        validators=[
            RegexValidator(
                regex="^\d{8}$",
                message="An ISRCTN must be an 8-digit number",
                # for some reason, the validation error message is incorrect:
                #     '%s' value must be an integer.
                # unless a non-default code is provided
                code="wrong"
                )
            ],
        help_text="International Standard Randomised Controlled Trial Number",
        blank=True, null=True
        )
    ukcrn = models.PositiveIntegerField(
        verbose_name="UKCRN ID",
        validators=[
            RegexValidator(
                regex="\d{5}",
                message="ID must be four or five digits",
                # for some reason, the validation error message is incorrect:
                #     '%s' value must be an integer.
                # unless a non-default code is provided
                code="wrong"
                )
            ],
        help_text="UK Clinical Research Network Study Portfolio",
        blank=True, null=True
        )
    eudract = models.CharField(
        verbose_name="EudraCT Number",
        max_length=18,
        validators=[
            RegexValidator(
                regex="^\d{4}-\d{6}-\d{2}$",
                message="EudraCT Number must be in the form '2007-003877-21'",
                # for some reason, the validation error message is incorrect:
                #     '%s' value must be an integer.
                # unless a non-default code is provided
                code="wrong"
                )
            ],
        help_text="EU Clinical Trials Register Number (format: '2007-003877-21')",
        blank=True, null=True
        )
    nct = models.CharField(
        verbose_name="NCT code",
        max_length=11,
        validators=[
            RegexValidator(
                regex="^NCT\d{8}$",
                message="Must begin 'NCT' and be followed by 8 digits",
                # for some reason, the validation error message is incorrect:
                #     '%s' value must be an integer.
                # unless a non-default code is provided
                code="wrong"
                )
            ],
        help_text="ClinicalTrials.gov registry code (begins 'NCT')",
        blank=True, null=True
        )

    # dates are optional - we don't always know when a trial will begin/end
    date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    trialtype = models.ManyToManyField(
        TrialType, verbose_name="Trial type",
        null=True, blank=True,
        )

    STATUSES = (
        ("setup", "In setup"),
        ("recruiting", "Recruiting"),
        ("running", "Running"),
        ("hold", "On hold"),
        ("followup", "In follow-up"),
        ("closed", "Closed"),
        )

    status = models.CharField(
        "Status",
        max_length=25,
        choices=STATUSES, default="setup"
        )

    # the ArkestraGenericModel provides a please_contact field, which we
    # re-label in the admin for trial_managers
    # note the way of providing related_names, which helps ensure uniqueness
    chief_investigators = models.ManyToManyField(
        Person,
        related_name='%(class)s_chief_investigators',
        null=True, blank=True
        )

    clinical_centre = models.ManyToManyField(
        Entity, verbose_name="Clinical centre",
        null=True, blank=True,
        related_name="%(class)s_clinical_centres",
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

    grant_value = models.CharField(
        max_length=25,
        null=True, blank=True,
        )

    email = models.EmailField(
        verbose_name="Email address", null=True, blank=True
        )

    # the phone_contacts field is taken from contacts_and_people
    phone_contacts = generic.GenericRelation(PhoneContact)


# If an entity is to publish clinical trials, we need a TrialEntity for it
# to control and manage this
class TrialEntity(models.Model):
    class Meta:
        verbose_name = "Entity that publishes trials"
        verbose_name_plural = "Entities that publish trials"

    #one-to-one link to contacts_and_people.Person
    entity = models.OneToOneField(
        'contacts_and_people.Entity',
        primary_key=True, related_name="trial_entity",
        help_text=
        """
        Do not under any circumstances change this field. No, really. Don't
        touch this.
        """
        )

    # in this case, publish_page must be selected in order for the menu to be
    # created. This is determined by the menu.TrialMenu class. Similarly, its
    # menu_title is also configurable here.
    publish_page = models.BooleanField(
        u"Publish an automatic clinical trials page",
        default=False,
        )
    menu_title = models.CharField(
        u"Title",
        max_length=50,
        default="Clinical trials"
        )

    # each entity's main clinical trials page can have a placeholder for
    # django CMS plugins, if wanted
    trials_page_intro = PlaceholderField(
        'body',
        related_name="trials_page_intro",
        )

    # we just get the name from the entity
    def __unicode__(self):
        return self.entity.__unicode__()
