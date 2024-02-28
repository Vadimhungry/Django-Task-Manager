from django.urls import reverse
from .models import Task
from ..users.models import CustomUser
from ..statuses.models import Status
from django.test import TestCase, Client
from .views import TaskCreate, TaskUpdate, TaskDelete


class TestCreate(TestCase):
    fixtures = [
        'labels.json',
        'tasks.json',
        'statuses.json',
        'users.json'
    ]

    def setUp(self):
        self.client = Client()
        self.client.force_login(CustomUser.objects.first())
        self.status = Status.objects.get(name="first")
        self.executor = CustomUser.objects.get(username="Gamma")
        self.created_task = {
            "name": "Test task",
            "description": "Test",
            "status": self.status.id,
            "executor": self.executor.id
        }

    def test_index_tasks(self):
        response = self.client.get(reverse("tasks_index"))
        self.assertContains(response, "one")
        self.assertContains(response, "two")
        self.assertNotContains(response, "ghost")

    def test_tasks_create(self):
        response = self.client.get(reverse("tasks_index"))
        self.assertNotContains(response, "Test task")

        response = self.client.get(reverse("task_create"))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(reverse("task_create"), '/tasks/create/')
        self.assertIs(response.resolver_match.func.view_class, TaskCreate)

        response = self.client.post(reverse("task_create"), self.created_task)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], reverse("tasks_index"))

        response = self.client.get(reverse("tasks_index"))
        self.assertContains(response, "Test task")


class TestUpdate(TestCase):
    fixtures = [
        'labels.json',
        'tasks.json',
        'statuses.json',
        'users.json'
    ]

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
            "executor": self.executor.id
        }

    def test_tasks_update(self):
        url_update = reverse("task_update", kwargs={"task_id": self.task.id})

        response = self.client.get(reverse("tasks_index"))
        self.assertNotContains(response, "updated task")

        response = self.client.get(url_update)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(url_update, f"/tasks/{self.task.pk}/update/")
        self.assertIs(response.resolver_match.func.view_class, TaskUpdate)

        response = self.client.post(url_update, self.updated_task)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], reverse("tasks_index"))

        response = self.client.get(reverse("tasks_index"))
        self.assertContains(response, "updated task")


class TestDelete(TestCase):
    fixtures = [
        'labels.json',
        'tasks.json',
        'statuses.json',
        'users.json'
    ]

    def setUp(self):
        self.client = Client()
        self.client.force_login(CustomUser.objects.first())
        self.del_task = Task.objects.get(name="one")

    def test_delete_tasks(self):
        response = self.client.get(reverse("tasks_index"))
        self.assertContains(response, "one")

        url_delete = reverse("task_delete", kwargs={"task_id": self.del_task.id})

        response = self.client.get(url_delete)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(url_delete, f"/tasks/1/delete/")
        self.assertIs(
            response.resolver_match.func.view_class,
            TaskDelete
        )

        response = self.client.post(url_delete)
        self.assertRedirects(response, reverse("tasks_index"), 302)
        self.assertEqual(response['Location'], reverse("tasks_index"))
        self.assertFalse(Task.objects.filter(name="one").exists())
