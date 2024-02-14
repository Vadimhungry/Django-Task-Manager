from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from .models import Task
from ..users.models import CustomUser
from ..statuses.models import Status


class TaskViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username="testuser", password="12345"
        )
        self.client.login(username="testuser", password="12345")

    def test_index_view(self):
        response = self.client.get(reverse("tasks_index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/index.html")

    def test_create_task_view(self):
        # Создание статуса для задачи
        test_status = Status.objects.create(name="Test Status")

        test_user = CustomUser.objects.get(username="testuser")

        # Определение данных для создания задачи
        task_data = {
            "name": "Test Task",
            "description": "Test Description",
            "status": test_status.id,
            "executor": test_user.id,
        }

        # Отправка POST-запроса для создания задачи
        response = self.client.post(reverse("task_create"), task_data)
        # Проверка, что задача была успешно создана
        task_exists = Task.objects.filter(name="Test Task").exists()
        self.assertTrue(task_exists)

        created_task = Task.objects.get(name="Test Task")
        self.assertEqual(created_task.description, "Test Description")

        self.assertRedirects(
            response, reverse("tasks_index")
        )  # Проверка на перенаправление

    def test_update_task_view(self):
        test_status = Status.objects.create(name="Test Status")
        test_user = CustomUser.objects.get(username="testuser")

        task_data = {
            "name": "Test Task",
            "description": "Test Description",
            "status": test_status.id,
            "executor": test_user.id,
        }

        self.client.post(reverse("task_create"), task_data)

        task_id = Task.objects.get(name="Test Task").id

        update_data = {
            "name": "Updated Task",
            "description": "Updated Description",
            "status": test_status.id,
            "executor": test_user.id,
        }
        self.client.post(
            reverse("task_update", kwargs={"task_id": task_id}), update_data
        )

        updated_task = Task.objects.get(id=task_id)
        self.assertEqual(updated_task.name, "Updated Task")
        self.assertEqual(updated_task.description, "Updated Description")

    def test_delete_task_view(self):
        test_status = Status.objects.create(name="Test Status")
        test_user = CustomUser.objects.get(username="testuser")

        task_data = {
            "name": "Test Task",
            "description": "Test Description",
            "status": test_status.id,
            "executor": test_user.id,
        }

        self.client.post(reverse("task_create"), task_data)
        task_id = Task.objects.get(name="Test Task").id
        self.client.post(reverse("task_delete", kwargs={"task_id": task_id}))

        self.assertEqual(Task.objects.filter(name="Test Task").exists(), False)

    def test_read_task_view(self):
        test_status = Status.objects.create(name="Test Status")
        test_user = CustomUser.objects.get(username="testuser")

        task_data = {
            "name": "Test Task",
            "description": "Test Description",
            "status": test_status.id,
            "executor": test_user.id,
        }

        self.client.post(reverse("task_create"), task_data)
        task_id = Task.objects.get(name="Test Task").id
        response = self.client.get(reverse("task", kwargs={"task_id": task_id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/task.html")
