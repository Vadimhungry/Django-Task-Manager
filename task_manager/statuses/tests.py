from django.test import TestCase, Client
from django.urls import reverse
from .models import Status
from task_manager.users.models import CustomUser
from task_manager.statuses.views import (
    StatusCreate,
    StatusUpdate,
    StatusDelete,
)


class TestCreate(TestCase):
    fixtures = ["statuses.json", "users.json"]

    def setUp(self):
        self.client = Client()
        self.client.force_login(CustomUser.objects.first())

    def test_status_create(self):
        response = self.client.get(reverse("statuses_index"))
        self.assertNotContains(response, "Another status")

        response = self.client.get(reverse("status_create"))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(reverse("status_create"), "/statuses/create/")
        self.assertIs(
            response.resolver_match.func.view_class,
            StatusCreate
        )

        response = self.client.post(
            reverse("status_create"), data={"name": "Another status"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("statuses_index"))

        response = self.client.get(reverse("statuses_index"))
        self.assertContains(response, "Another status")


class TestUpdate(TestCase):
    fixtures = ["statuses.json", "users.json"]

    def setUp(self):
        self.client = Client()
        self.client.force_login(CustomUser.objects.first())
        self.old_status = Status.objects.all().first()
        self.updated_status = {"name": "Updated status"}
        print(self.old_status)

    def test_status_update(self):
        url_update = reverse(
            "status_update",
            kwargs={"pk": self.old_status.id}
        )

        response = self.client.get(url_update)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            url_update,
            f"/statuses/{self.old_status.pk}/update/"
        )
        self.assertIs(
            response.resolver_match.func.view_class,
            StatusUpdate
        )

        response = self.client.post(url_update, self.updated_status)
        self.assertRedirects(response, reverse("statuses_index"), 302)
        self.assertEqual(response["Location"], reverse("statuses_index"))

        response = self.client.get(reverse("statuses_index"))
        self.assertContains(response, "Updated status")


class TestDelete(TestCase):
    fixtures = ["statuses.json", "users.json"]

    def setUp(self):
        self.client = Client()
        self.client.force_login(CustomUser.objects.first())

    def test_delete_statuses(self):
        del_status = Status.objects.get(name="second")
        url_delete = reverse(
            "delete_status",
            kwargs={"pk": del_status.id}
        )

        response = self.client.get(url_delete)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(url_delete, f"/statuses/{del_status.id}/delete/")
        self.assertIs(
            response.resolver_match.func.view_class,
            StatusDelete
        )

        response = self.client.post(url_delete)
        self.assertEquals(url_delete, f"/statuses/{del_status.id}/delete/")
        self.assertRedirects(response, reverse("statuses_index"), 302)
        self.assertIs(
            response.resolver_match.func.view_class,
            StatusDelete
        )
        self.assertEqual(response["Location"], reverse("statuses_index"))
        self.assertFalse(Status.objects.filter(name="second").exists())
