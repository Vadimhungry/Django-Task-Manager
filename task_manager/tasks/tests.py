from django.urls import reverse
from .models import Task
from task_manager.users.models import CustomUser
from task_manager.statuses.models import Status
from django.test import TestCase, Client
from .views import TaskCreate, TaskUpdate, TaskDelete
from task_manager.utils import get_fixture_data
from django.utils.translation import gettext as _
from task_manager.settings import FIXTURE_PATH
import os


class TestCreate(TestCase):
    fixtures = ["labels.json", "tasks.json", "statuses.json", "users.json"]

    def setUp(self):
        self.client = Client()
        self.client.force_login(CustomUser.objects.first())
        self.status = Status.objects.first()
        self.executor = CustomUser.objects.last()
        self.data = get_fixture_data(
            os.path.join(FIXTURE_PATH, 'test_data.json')
        )
        self.created_task = self.data.get('tasks').get('new_task')

    def test_index_tasks(self):
        response = self.client.get(reverse("tasks_index"))
        tasks = Task.objects.all()
        for task in tasks:
            self.assertContains(response, task.name)

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
        self.executor = CustomUser.objects.first()
        self.data = get_fixture_data(
            os.path.join(FIXTURE_PATH, 'test_data.json')
        ).get('tasks')
        update_name = self.data.get('update_task').get('name')
        update_description = self.data.get('update_task').get('description')
        self.updated_task = {
            "name": update_name,
            "description": update_description,
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
        self.del_task = Task.objects.first()
        self.undelateble_task = Task.objects.last()

    def test_delete_tasks_success(self):
        response = self.client.get(reverse("tasks_index"))
        self.assertContains(response, self.del_task)

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
        self.assertFalse(Task.objects.filter(name=self.del_task).exists())

    def test_delete_tasks_failture(self):

        url_delete = reverse(
            "task_delete",
            kwargs={"pk": self.undelateble_task.id}
        )

        response = self.client.post(url_delete, follow=True)
        self.assertContains(
            response,
            _("The task can only be deleted by its author")
        )
