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

from models import Study
from lister import StudiesList, StudiesLister
from views import clinical_study, StudiesArchiveView


# create a study and test its attributes
class StudyTests(TestCase):
    def setUp(self):
        # create a clinical study
        self.study = Study(
            title="Can teeth bite?",
            slug="can-teeth-bite",
            date=datetime.now(),
            )

    def test_generic_attributes(self):
        self.study.save()
        # the item has no informative content
        self.assertEqual(self.study.is_uninformative, True)

        # no Entities in the database, so this can't be hosted_by anything
        self.assertEqual(self.study.hosted_by, None)

        #  no Entities in the database, so default to settings's template
        self.assertEqual(
            self.study.get_template,
            settings.CMS_TEMPLATES[0][0]
            )

    def test_link_to_more(self):
        self.assertEqual(
            self.study.auto_page_view_name,
            "clinical-studies"
            )
        self.study.hosted_by = Entity(slug="slug")
        self.assertEqual(
            self.study.link_to_more(),
            "/clinical-studies/slug/"
            )


class StudyListTests(TestCase):
    def setUp(self):
        self.item1 = Study(
            title="newer",
            in_lists=True,
            published=True,
            date=datetime.now(),
            slug="item1"
            )
        self.item1.save()

        self.item2 = Study(
            title="older",
            in_lists=True,
            published=True,
            date=datetime.now()-timedelta(days=200),
            slug="item2"
            )
        self.item2.save()

        self.item3 = Study(
            title="unpublished",
            in_lists=True,
            published=False,
            date=datetime.now(),
            slug="item3"
            )
        self.item1.save()

        self.itemlist = StudiesList(request=RequestFactory().get("/"))

    def test_build(self):
        self.itemlist.build()

        self.assertItemsEqual(
            self.itemlist.items,
            [self.item1, self.item2]
        )

    def test_lister_has_list(self):
        lister = StudiesLister(request=RequestFactory().get("/"))

        self.assertIsInstance(lister.lists[0], StudiesList)

    def test_list_has_correct_filter_fields(self):
        self.assertItemsEqual(
            self.itemlist.filter_set.fields,
            ["date", "status", "studytype"]
            )


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

        self.item1 = Study(
            title="newer",
            in_lists=True,
            published=True,
            date=datetime.now(),
            slug="item1"
            )
        self.item1.save()

        self.item2 = Study(
            title="older",
            in_lists=True,
            published=True,
            date=datetime.now()-timedelta(days=200),
            slug="item2"
            )
        self.item2.save()

        self.item3 = Study(
            title="unpublished",
            in_lists=True,
            published=False,
            date=datetime.now(),
            slug="item3"
            )
        self.item1.save()

        self.itemlist = StudiesList(request=RequestFactory().get("/"))

    def test_main_url(self):
        self.school.save()
        response = self.client.get('/clinical-studies/')
        self.assertEqual(response.status_code, 200)

        self.assertItemsEqual(
            response.context["lister"].lists[0].items,
            [self.item1, self.item2]
            )

    def test_entity_url(self):
        self.school.save()
        response = self.client.get('/clinical-studies/medicine/')
        self.assertEqual(response.status_code, 200)


class ResolveURLsTests(TestCase):
    def test_resolve_study_url(self):
        resolver = resolve('/clinical-study/can-teeth-bite/')
        self.assertEqual(resolver.view_name, "clinical-study")
        self.assertEqual(resolver.func, clinical_study)

    def test_resolve_study_filter_list_base_url(self):
        resolver = resolve('/clinical-studies/')
        self.assertEqual(resolver.view_name, "clinical-studies")

    def test_resolve_study_filter_list_named_url(self):
        resolver = resolve('/clinical-studies/some-slug/')
        self.assertEqual(resolver.view_name, "clinical-studies")


class ReverseURLsTests(TestCase):
    def test_studies_reverse_url(self):
        self.assertEqual(
            reverse("clinical-study", kwargs={"slug": "can-teeth-bite"}),
            "/clinical-study/can-teeth-bite/"
            )

    def test_studies_base_reverse_url(self):
        self.assertEqual(
            reverse("clinical-studies"),
            "/clinical-studies/"
            )

    def test_news_archive_named_entity_reverse_url(self):
        self.assertEqual(
            reverse("clinical-studies", kwargs={"slug": "some-slug"}),
            "/clinical-studies/some-slug/"
            )


@override_settings(CMS_TEMPLATES=(('null.html', "Null"),))
class StudyDetailTests(TestCase):
    def setUp(self):
        self.item1 = Study(
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

    def test_unpublished_clinical_study_404(self):
        self.item1.save()

        response = self.client.get("/clinical-study/item1/")
        self.assertEqual(response.status_code, 404)

    def test_unpublished_clinical_study_200_for_admin(self):
        self.item1.save()

        # log in a staff user
        self.client.login(username='arkestra', password='arkestra')
        response = self.client.get('/clinical-study/item1/')
        self.assertEqual(response.status_code, 200)

    def test_published_clinical_study_200_for_everyone(self):
        self.item1.published = True
        self.item1.save()

        # Check that the response is 200 OK.
        response = self.client.get('/clinical-study/item1/')
        self.assertEqual(response.status_code, 200)

    def test_published_clinical_study_context(self):
        self.item1.published = True
        self.item1.save()
        response = self.client.get('/clinical-study/item1/')
        self.assertEqual(response.context['study'], self.item1)


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

        response = self.client.get('/admin/arkestra_clinical_studies/study/add/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context_data["title"],
            u'Add study'
        )
