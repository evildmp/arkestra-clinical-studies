from datetime import datetime, timedelta

from django.test import TestCase
from django.test.client import Client
from django.test.utils import override_settings
from django.http import HttpRequest
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse, resolve
from django.contrib.auth.models import User
from django.conf import settings

from cms.api import create_page

from contacts_and_people.models import Entity

from models import ClinicalTrial
from lister import ClinicalTrialsList, ClinicalTrialsLister
from views import clinical_trial, ClinicalTrialsArchiveView


# create a trial and test its attributes

class ClinicalTrialTests(TestCase):
    def setUp(self):
        # create a clinical trial
        self.trial = ClinicalTrial(
            title="Can teeth bite?",
            slug="can-teeth-bite",
            date=datetime.now(),
            )

    def test_generic_attributes(self):
        self.trial.save()
        # the item has no informative content
        self.assertEqual(self.trial.is_uninformative, True)

        # no Entities in the database, so this can't be hosted_by anything
        self.assertEqual(self.trial.hosted_by, None)

        #  no Entities in the database, so default to settings's template
        self.assertEqual(
            self.trial.get_template,
            settings.CMS_TEMPLATES[0][0]
            )


class ClinicalTrialListTests(TestCase):
    def setUp(self):
        self.item1 = ClinicalTrial(
            title="newer",
            in_lists=True,
            published=True,
            date=datetime.now(),
            slug="item1"
            )
        self.item1.save()

        self.item2 = ClinicalTrial(
            title="older",
            in_lists=True,
            published=True,
            date=datetime.now()-timedelta(days=200),
            slug="item2"
            )
        self.item2.save()

        self.item3 = ClinicalTrial(
            title="unpublished",
            in_lists=True,
            published=False,
            date=datetime.now(),
            slug="item3"
            )
        self.item1.save()

        self.itemlist = ClinicalTrialsList(request=RequestFactory().get("/"))

    def test_build(self):
        self.itemlist.build()

        self.assertItemsEqual(
            self.itemlist.items,
            [self.item1, self.item2]
        )

    def test_lister_has_list(self):
        lister = ClinicalTrialsLister(request=RequestFactory().get("/"))

        self.assertIsInstance(lister.lists[0], ClinicalTrialsList)


@override_settings(CMS_TEMPLATES=(('null.html', "Null"),))
class ClinicalEntityPagesTests(TestCase):
    def setUp(self):

        home_page = create_page(
            "School home page",
            "null.html",
            "en",
            published=True
            )

        self.school = Entity(
            name="School of Medicine",
            slug="medicine",
            auto_news_page=True,
            website=home_page
            )

        self.item1 = ClinicalTrial(
            title="newer",
            in_lists=True,
            published=True,
            date=datetime.now(),
            slug="item1"
            )
        self.item1.save()

        self.item2 = ClinicalTrial(
            title="older",
            in_lists=True,
            published=True,
            date=datetime.now()-timedelta(days=200),
            slug="item2"
            )
        self.item2.save()

        self.item3 = ClinicalTrial(
            title="unpublished",
            in_lists=True,
            published=False,
            date=datetime.now(),
            slug="item3"
            )
        self.item1.save()

        self.itemlist = ClinicalTrialsList(request=RequestFactory().get("/"))

    def test_main_url(self):
        self.school.save()
        response = self.client.get('/clinical-trials/')
        self.assertEqual(response.status_code, 200)

        self.assertItemsEqual(
            response.context["lister"].lists[0].items,
            [self.item1, self.item2]
            )

    def test_entity_url(self):
        self.school.save()
        response = self.client.get('/clinical-trials/medicine/')
        self.assertEqual(response.status_code, 200)


class ReverseURLsTests(TestCase):
    def test_clinicaltrials_reverse_url(self):
        self.assertEqual(
            reverse("clinical-trial", kwargs={"slug": "can-teeth-bite"}),
            "/clinical-trial/can-teeth-bite/"
            )

    def testclinicaltrials_base_reverse_url(self):
        self.assertEqual(
            reverse("clinical-trials-base"),
            "/clinical-trials/"
            )

    def test_news_archive_named_entity_reverse_url(self):
        self.assertEqual(
            reverse("clinical-trials", kwargs={"slug": "some-slug"}),
            "/clinical-trials/some-slug/"
            )

class ResolveURLsTests(TestCase):
    def test_resolve_clinicaltrial_url(self):
        resolver = resolve('/clinical-trial/can-teeth-bite/')
        self.assertEqual(resolver.view_name, "clinical-trial")
        self.assertEqual(resolver.func, clinical_trial)

    def test_resolve_clinicaltrial_filter_list_base_url(self):
        resolver = resolve('/clinical-trials/')
        self.assertEqual(resolver.view_name, "clinical-trials-base")

    def test_resolve_clinicaltrial_filter_list_named_url(self):
        resolver = resolve('/clinical-trials/some-slug/')
        self.assertEqual(resolver.view_name, "clinical-trials")


@override_settings(CMS_TEMPLATES=(('null.html', "Null"),))
class ClinicalTrialDetailTests(TestCase):
    def setUp(self):
        self.item1 = ClinicalTrial(
            title="newer",
            slug="item1"
            )

        self.adminuser = User.objects.create_user(
            'arkestra',
            'arkestra@example.com',
            'arkestra'
            )
        self.adminuser.is_staff = True
        self.adminuser.save()

    def test_unpublished_clinical_trial_404(self):
        self.item1.save()

        response = self.client.get("/clinical-trial/item1/")
        self.assertEqual(response.status_code, 404)

    def test_unpublished_clinical_trial_200_for_admin(self):
        self.item1.save()

        # log in a staff user
        self.client.login(username='arkestra', password='arkestra')
        response = self.client.get('/clinical-trial/item1/')
        self.assertEqual(response.status_code, 200)

    def test_published_clinical_trial_200_for_everyone(self):
        self.item1.published = True
        self.item1.save()

        # Check that the response is 200 OK.
        response = self.client.get('/clinical-trial/item1/')
        self.assertEqual(response.status_code, 200)

    def test_published_clinical_trial_context(self):
        self.item1.published = True
        self.item1.save()
        response = self.client.get('/clinical-trial/item1/')
        self.assertEqual(response.context['clinicaltrial'], self.item1)


class AdminInterfaceTests(TestCase):
    def test_admin_interface_is_available(self):
        self.adminuser = User.objects.create_superuser(
            'arkestra',
            'arkestra@example.com',
            'arkestra'
            )
        self.adminuser.is_staff = True
        self.adminuser.save()

        self.client.login(username="arkestra", password="arkestra")

        response = self.client.get('/admin/arkestra_clinical_trials/clinicaltrial/add/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context_data["title"],
            u'Add clinical trial'
        )
