from django.test import TestCase, Client
from django.urls import reverse
from .models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import CustomUser
from task_manager.statuses.views import (
    StatusCreate,
    StatusUpdate,
    StatusDelete,
)
from ..utils import get_fixture_data
from django.utils.translation import gettext as _
from ..settings import FIXTURE_PATH
import os


class TestCreate(TestCase):
    fixtures = ["statuses.json", "users.json"]

    def setUp(self):
        self.client = Client()
        self.client.force_login(CustomUser.objects.first())
        data = get_fixture_data(os.path.join(FIXTURE_PATH, 'test_data.json'))
        self.new_status = data.get('statuses').get('new_status')

    def test_status_create(self):
        response = self.client.get(reverse("statuses_index"))
        self.assertNotContains(response, self.new_status['name'])

        response = self.client.get(reverse("status_create"))
        self.assertEquals(response.status_code, 200)
        self.assertIs(
            response.resolver_match.func.view_class,
            StatusCreate
        )

        response = self.client.post(
            reverse("status_create"),
            data=self.new_status,
            follow=True
        )

        self.assertContains(
            response,
            _("Status successfully created")
        )

        response = self.client.get(reverse("statuses_index"))
        self.assertContains(response, self.new_status['name'])


class TestUpdate(TestCase):
    fixtures = ["statuses.json", "users.json"]

    def setUp(self):
        self.client = Client()
        self.client.force_login(CustomUser.objects.first())
        self.old_status = Status.objects.all().first()
        data = get_fixture_data(os.path.join(FIXTURE_PATH, 'test_data.json'))
        self.updated_status = data.get('statuses').get('updated_status')

    def test_status_update(self):
        url_update = reverse(
            "status_update",
            kwargs={"pk": self.old_status.id}
        )

        response = self.client.get(url_update)
        self.assertEquals(response.status_code, 200)
        self.assertIs(
            response.resolver_match.func.view_class,
            StatusUpdate
        )

        response = self.client.post(
            url_update,
            self.updated_status,
            follow=True
        )
        self.assertContains(
            response,
            _("Status successfully updated")
        )

        response = self.client.get(reverse("statuses_index"))
        self.assertContains(response, self.updated_status['name'])


class TestDelete(TestCase):
    fixtures = ["statuses.json", "users.json"]

    def setUp(self):
        self.client = Client()
        self.client.force_login(CustomUser.objects.first())
        self.status = Status.objects.get(name="second")
        self.executor = CustomUser.objects.get(username="Alpha")

    def test_delete_statuses(self):
        del_status = Status.objects.get(name="second")
        url_delete = reverse(
            "delete_status",
            kwargs={"pk": del_status.id}
        )

        response = self.client.get(url_delete)
        self.assertEquals(response.status_code, 200)
        self.assertIs(
            response.resolver_match.func.view_class,
            StatusDelete
        )

        response = self.client.post(url_delete, follow=True)
        self.assertContains(
            response,
            _("Status successfully deleted")
        )

        self.assertFalse(Status.objects.filter(name="second").exists())

    def test_unsuccsessfull_delete(self):
        Task.objects.create(
            name="Test Task",
            description="Test Description",
            status=self.status,
            executor=self.executor,
            author=CustomUser.objects.first()
        )

        del_status = Status.objects.get(name="second")

        url_delete = reverse(
            "delete_status",
            kwargs={"pk": del_status.id}
        )

        response = self.client.get(url_delete)
        self.assertEquals(response.status_code, 200)
        self.assertIs(
            response.resolver_match.func.view_class,
            StatusDelete
        )

        response = self.client.post(url_delete, follow=True)
        self.assertContains(
            response,
            _("Unable to delete the status because it is in use")
        )
        self.assertTrue(Status.objects.filter(name="second").exists())
