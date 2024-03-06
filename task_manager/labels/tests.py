from django.test import TestCase, Client
from django.urls import reverse
from .models import Label
from task_manager.users.models import CustomUser
from .views import LabelCreate, LabelUpdate, LabelDelete
import json


class TestCreate(TestCase):
    fixtures = ["labels.json", "users.json"]

    def setUp(self):
        self.client = Client()
        self.client.force_login(CustomUser.objects.first())

    def test_index_labels(self):
        response = self.client.get(reverse("labels_index"))
        self.assertContains(response, "label_1")
        self.assertContains(response, "label_2")
        self.assertNotContains(response, "ghost")

    def test_labels_create(self):
        response = self.client.get(reverse("labels_index"))
        with open('task_manager/fixtures/test_data.json', 'r') as f:
            data = json.load(f)
            self.new_label = data.get('labels').get('new_label')
        self.assertNotContains(response, self.new_label['name'])

        response = self.client.get(reverse("label_create"))
        self.assertEquals(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, LabelCreate)

        response = self.client.post(
            reverse("label_create"), data=self.new_label
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("labels_index"))

        response = self.client.get(reverse("labels_index"))
        self.assertContains(response, self.new_label['name'])


class TestUpdate(TestCase):
    fixtures = ["labels.json", "users.json"]

    def setUp(self):
        self.client = Client()
        self.client.force_login(CustomUser.objects.first())
        self.old_label = Label.objects.get(id=1)
        with open('task_manager/fixtures/test_data.json', 'r') as f:
            data = json.load(f)
            self.updated_label = data.get('labels').get('update_label')

    def test_label_update(self):
        url_update = reverse('label_update', kwargs={'pk': self.old_label.pk})
        response = self.client.get(url_update)
        self.assertEquals(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, LabelUpdate)

        response = self.client.post(url_update, self.updated_label)
        self.assertRedirects(response, reverse("labels_index"), 302)
        self.assertEqual(response["Location"], reverse("labels_index"))

        response = self.client.get(reverse("labels_index"))
        self.assertContains(response, self.updated_label['name'])


class TestDelete(TestCase):
    fixtures = ["labels.json", "users.json"]

    def setUp(self):
        self.client = Client()
        self.client.force_login(CustomUser.objects.first())
        self.del_label = Label.objects.all().first()

    def test_delete_label(self):
        response = self.client.get(reverse("labels_index"))
        self.assertContains(response, "label_1")

        url_delete = reverse(
            "label_delete",
            kwargs={"pk": self.del_label.id}
        )
        response = self.client.get(url_delete)
        self.assertEquals(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, LabelDelete)

        response = self.client.post(url_delete)
        self.assertRedirects(response, reverse("labels_index"), 302)
        self.assertEqual(response["Location"], reverse("labels_index"))

        response = self.client.get(reverse("labels_index"))
        self.assertNotContains(response, "label_1")
