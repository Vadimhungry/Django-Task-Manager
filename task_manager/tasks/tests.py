from django.urls import reverse
from .models import Task
from ..users.models import CustomUser
from ..statuses.models import Status
from django.test import TestCase, Client
from .views import TaskCreate, TaskUpdate, TaskDelete
from ..utils import get_json_data
from django.utils.translation import gettext as _


class TestCreate(TestCase):
    fixtures = ["labels.json", "tasks.json", "statuses.json", "users.json"]

    def setUp(self):
        self.client = Client()
        self.client.force_login(CustomUser.objects.first())
        self.status = Status.objects.get(name="first")
        self.executor = CustomUser.objects.get(username="Gamma")
        data = get_json_data('task_manager/fixtures/test_data.json')
        self.created_task = data.get('tasks').get('new_task')

    def test_index_tasks(self):
        response = self.client.get(reverse("tasks_index"))
        self.assertContains(response, "one")
        self.assertContains(response, "two")
        self.assertNotContains(response, "ghost")

    def test_tasks_create(self):
        response = self.client.get(reverse("tasks_index"))
        self.assertNotContains(response, self.created_task['name'])

        response = self.client.get(reverse("task_create"))
        self.assertEquals(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, TaskCreate)

        response = self.client.post(
            reverse("task_create"),
            self.created_task,
            follow=True
        )
        self.assertContains(
            response,
            _("Task successfully created")
        )
        response = self.client.get(reverse("tasks_index"))
        self.assertContains(response, self.created_task['name'])


class TestUpdate(TestCase):
    fixtures = ["labels.json", "tasks.json", "statuses.json", "users.json"]

    def setUp(self):
        self.client = Client()
        self.client.force_login(CustomUser.objects.first())
        self.status = Status.objects.all().first()
        self.task = Task.objects.all().first()
        self.executor = CustomUser.objects.get(username="Alpha")
        self.updated_task = {
            "name": "updated task",
            "description": "Updated Description",
            "status": self.status.id,
            "executor": self.executor.id,
        }

    def test_tasks_update(self):
        url_update = reverse("task_update", kwargs={"pk": self.task.id})

        response = self.client.get(reverse("tasks_index"))
        self.assertNotContains(response, self.updated_task['name'])

        response = self.client.get(url_update)
        self.assertEquals(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, TaskUpdate)

        response = self.client.post(
            url_update,
            self.updated_task,
            follow=True
        )
        self.assertContains(
            response,
            _("Task successfully updated")
        )

        response = self.client.get(reverse("tasks_index"))
        self.assertContains(response, self.updated_task['name'])


class TestDelete(TestCase):
    fixtures = ["labels.json", "tasks.json", "statuses.json", "users.json"]

    def setUp(self):
        self.client = Client()
        self.client.force_login(CustomUser.objects.first())
        self.del_task = Task.objects.get(name="one")
        self.undelateble_task = Task.objects.get(name="two")

    def test_delete_tasks(self):
        response = self.client.get(reverse("tasks_index"))
        self.assertContains(response, "one")

        url_delete = reverse(
            "task_delete",
            kwargs={"pk": self.del_task.id}
        )

        response = self.client.get(url_delete)
        self.assertEquals(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, TaskDelete)

        response = self.client.post(
            url_delete,
            follow=True
        )
        self.assertContains(
            response,
            _("The task has been successfully deleted")
        )
        self.assertFalse(Task.objects.filter(name="one").exists())

    def test_unsuccsessfull_delete(self):

        url_delete = reverse(
            "task_delete",
            kwargs={"pk": self.undelateble_task.id}
        )

        response = self.client.post(url_delete, follow=True)
        self.assertContains(
            response,
            _("The task can only be deleted by its author")
        )
