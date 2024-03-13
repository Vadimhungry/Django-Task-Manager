from django.test import TestCase, Client
from django.urls import reverse
from .models import Label
from task_manager.users.models import CustomUser
from task_manager.tasks.models import Task
from .views import LabelCreate, LabelUpdate, LabelDelete
from django.utils.translation import gettext as _
from task_manager.statuses.models import Status
from task_manager.utils import get_fixture_data
from task_manager.settings import FIXTURE_PATH
import os


class TestCreate(TestCase):
    fixtures = ["labels.json", "users.json"]

    def setUp(self):
        self.client = Client()
        self.client.force_login(CustomUser.objects.first())

    def test_index_labels(self):
        response = self.client.get(reverse("labels_index"))
        for label in Label.objects.all():
            self.assertContains(response, label)

    def test_labels_create(self):
        response = self.client.get(reverse("labels_index"))
        data = get_fixture_data(os.path.join(FIXTURE_PATH, 'test_data.json'))
        self.new_label = data.get('labels').get('new_label')
        self.assertNotContains(response, self.new_label['name'])

        response = self.client.get(reverse("label_create"))
        self.assertEquals(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, LabelCreate)

        response = self.client.post(
            reverse("label_create"), data=self.new_label, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            _("The label has been created successfully")
        )

        response = self.client.get(reverse("labels_index"))
        self.assertContains(response, self.new_label['name'])


class TestUpdate(TestCase):
    fixtures = ["labels.json", "users.json"]

    def setUp(self):
        self.client = Client()
        self.client.force_login(CustomUser.objects.first())
        self.old_label = Label.objects.get(id=1)
        data = get_fixture_data('task_manager/fixtures/test_data.json')
        self.updated_label = data.get('labels').get('update_label')

    def test_label_update(self):
        url_update = reverse('label_update', kwargs={'pk': self.old_label.pk})
        response = self.client.get(url_update)
        self.assertEquals(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, LabelUpdate)

        response = self.client.post(
            url_update,
            self.updated_label,
            follow=True
        )
        self.assertContains(
            response,
            _("The label has been successfully updated")
        )

        response = self.client.get(reverse("labels_index"))
        self.assertContains(response, self.updated_label['name'])


class TestDelete(TestCase):
    fixtures = [
        "labels.json",
        "users.json",
        "statuses.json"
    ]

    def setUp(self):
        self.client = Client()
        self.client.force_login(CustomUser.objects.first())
        self.del_label = Label.objects.all().first()
        self.undeletable_label = Label.objects.last()

    def test_delete_label(self):
        response = self.client.get(reverse("labels_index"))
        self.assertContains(response, self.del_label)

        url_delete = reverse(
            "label_delete",
            kwargs={"pk": self.del_label.id}
        )
        response = self.client.get(url_delete)
        self.assertEquals(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, LabelDelete)

        response = self.client.post(url_delete, follow=True)
        self.assertContains(
            response,
            _("The label has been successfully deleted")
        )

        response = self.client.get(reverse("labels_index"))
        self.assertNotContains(response, self.del_label)


class TestUnableDelete(TestCase):
    fixtures = [
        "labels.json",
        "users.json",
        "statuses.json"
    ]

    def setUp(self):
        self.client = Client()
        self.client.force_login(CustomUser.objects.first())
        self.del_label = Label.objects.all().first()
        self.undeletable_label = Label.objects.get(id=3)
        self.status = Status.objects.all().first()
        self.executor = CustomUser.objects.all().first()

    def test_delete_label(self):
        task = Task.objects.create(
            name="Test Task",
            description="Test Description",
            status=self.status,
            executor=self.executor,
            author=CustomUser.objects.first()
        )

        url_update = reverse("task_update", kwargs={"pk": task.pk})
        updated_task = {
            "name": "updated task",
            "description": "Updated Description",
            "status": self.status.id,
            "executor": self.executor.id,
            "labels": [self.undeletable_label.id]
        }
        self.client.post(
            url_update,
            updated_task,
            follow=True
        )

        url_delete = reverse(
            "label_delete",
            kwargs={"pk": self.undeletable_label.id}
        )
        response = self.client.post(url_delete, follow=True)
        self.assertContains(
            response,
            _("Unable to delete the label because it is in use")
        )
