from django.test import TestCase, Client
from django.urls import reverse, reverse_lazy
from .models import CustomUser


class TestUsers(TestCase):
    fixtures = [
        "user.json",
    ]

    def setUp(self):
        self.client = Client()

    def test_index(self):
        response = self.client.get("/users/")
        response.status_code
        self.assertEqual(response.status_code, 200)

    def test_user_create_get(self):
        response = self.client.get("/users/create/")
        response.status_code
        self.assertEqual(response.status_code, 200)

    def test_user_create_post(self):
        valid_form_data = {
            "first_name": "2Ivan",
            "last_name": "2Durak",
            "username": "2testuser",
            "password1": "2Testpassword12345",
            "password2": "2Testpassword12345",
        }

        # Отправляем POST запрос с валидными данными формы
        response = self.client.post(
            reverse("user_create"), valid_form_data, follow=True
        )

        # Проверяем, что ответ содержит сообщение об успешной регистрации
        self.assertContains(response, "Пользователь успешно зарегистрирован")

    def test_user_login(self):
        valid_form_data = {
            "first_name": "2Ivan",
            "last_name": "2Durak",
            "username": "2testuser",
            "password1": "2Testpassword12345",
            "password2": "2Testpassword12345",
        }

        self.client.post(reverse("user_create"), valid_form_data)

        login_url = reverse("user_login")
        login_data = {
            "username": "2testuser",
            "password": "2Testpassword12345",
        }

        # Send a POST request to the login view with credentials
        response = self.client.post(login_url, data=login_data, follow=True)
        self.assertTrue("_auth_user_id" in self.client.session)
        self.assertRedirects(response, reverse_lazy("index"), status_code=302)
        self.assertContains(response, "Вы залогинены")

    from django.contrib.auth.models import User

    def test_user_update(self):
        # Создаем пользователя
        valid_form_data = {
            "first_name": "Ivan",
            "last_name": "Durak",
            "username": "2testuser",
            "password1": "2Testpassword12345",
            "password2": "2Testpassword12345",
        }
        self.client.post(reverse("user_create"), valid_form_data)

        # Получаем ID пользователя
        user_id = CustomUser.objects.get(username="testuser").id

        # Отправляем GET запрос на страницу обновления пользователя
        response = self.client.get(f"/users/{user_id}/update/", follow=True)
        self.assertEqual(
            response.status_code,
            200
        )  # Проверяем, что страница доступна
        self.assertContains(
            response, "У вас нет прав для изменения другого пользователя."
        )

        # login as 2testuser
        login_url = reverse("user_login")
        login_data = {
            "username": "2testuser",
            "password": "2Testpassword12345",
        }

        # Send a POST request to the login view with credentials
        self.client.post(login_url, data=login_data, follow=True)
        self.assertTrue("_auth_user_id" in self.client.session)

        new_form_data = {
            "first_name": "Updated Ivan",
            "last_name": "Updated Durak",
            "username": "Updated2testuser",
            "password1": "2Testpassword12345",
            "password2": "2Testpassword12345",
        }
        user_id = CustomUser.objects.get(username="2testuser").id
        update_url = reverse("user_update", kwargs={"user_id": user_id})
        response = self.client.post(
            update_url,
            data=new_form_data,
            follow=True
        )
        self.assertContains(response, "Пользователь успешно изменен")
