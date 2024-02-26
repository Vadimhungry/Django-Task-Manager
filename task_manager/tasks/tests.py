from django.test import TestCase
from django.urls import reverse
from .models import Task
from ..users.models import CustomUser
from ..statuses.models import Status
from ..labels.models import Label
from ..tasks.filters import TaskFilter
from django.test import RequestFactory


class TaskViewTests(TestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = CustomUser.objects.create_user(
            username="testuser", password="12345"
        )
        self.client.login(username="testuser", password="12345")

        # Создаем статус и метку для использования в тесте
        self.status = Status.objects.create(name="Test Status")
        self.label = Label.objects.create(name="Test Label")

        # URL для создания задачи
        self.url = reverse("task_create")

        self.task = Task.objects.create(
            name="Test Task",
            description="Test Description",
            executor=self.user,
            author=self.user,
            status=self.status,
        )

    def test_task_create_view(self):
        data = {
            "name": "2Test Task",
            "description": "2Test Description",
            "executor": self.user.id,
            "author": self.user.id,
            "status": self.status.id,
            "labels": [self.label.id],
        }

        response = self.client.post(self.url, data)

        self.assertTrue(Task.objects.filter(name="2Test Task").exists())

        created_task = Task.objects.get(name="2Test Task")

        self.assertEqual(created_task.name, "2Test Task")
        self.assertEqual(created_task.description, "2Test Description")
        self.assertEqual(created_task.executor, self.user)
        self.assertEqual(created_task.author, self.user)
        self.assertEqual(created_task.status, self.status)
        self.assertTrue(created_task.labels.filter(id=self.label.id).exists())

        self.assertRedirects(response, reverse("tasks_index"))

    def test_index_view(self):
        response = self.client.get(reverse("tasks_index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/index.html")

    def test_task_update_view(self):
        url = reverse("task_update", kwargs={"task_id": self.task.id})

        updated_data = {
            "name": "777Updated Test Task",
            "description": "777Updated Test Description",
            "executor": self.user.id,
            "author": self.user.id,
            "status": self.status.id,
            "labels": [self.label.id],
        }

        response = self.client.post(url, updated_data)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "777Updated Test Task")
        self.assertEqual(self.task.description, "777Updated Test Description")
        self.assertEqual(self.task.status, self.status)
        self.assertTrue(self.task.labels.filter(id=self.label.id).exists())
        self.assertRedirects(response, reverse("tasks_index"))


class TaskFilterTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser", password="12345"
        )
        self.client.login(username="testuser", password="12345")

        # Создаем статус и метку для использования в тесте
        self.status = Status.objects.create(name="Test Status")
        self.label = Label.objects.create(name="Test Label")

        # URL для создания задачи
        self.url = reverse("task_create")

        self.task1 = Task.objects.create(
            name="Test Task",
            description="Test Description",
            executor=self.user,
            author=self.user,
            status=self.status,
        )
        self.task2 = Task.objects.create(
            name="2Test Task",
            description="2Test Description",
            executor=self.user,
            author=self.user,
            status=self.status,
        )

    def test_filter_created_by_current_user(self):
        # Test for regular user
        request = RequestFactory().get("/")
        request.user = CustomUser.objects.create_user(
            username="regular_user",
            email="user@example.com",
            password="password"
        )
        filter = TaskFilter(
            {"created_by_current_user": "on"},
            queryset=Task.objects.all(),
            request=request,
        )
        print(filter.qs)
        self.assertQuerysetEqual(filter.qs, [])
