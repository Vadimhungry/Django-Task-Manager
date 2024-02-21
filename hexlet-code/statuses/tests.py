from django.test import TestCase, Client
from django.urls import reverse
from .models import Status


class TestStatuses(TestCase):
    def setUp(self):
        self.client = Client()
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
        self.client.post(login_url, data=login_data, follow=True)
        self.assertTrue("_auth_user_id" in self.client.session)

        response = self.client.get("/statuses/create/")
        self.assertEqual(response.status_code, 200)
        status_create_url = reverse("status_create")
        data = {"name": "fun status"}

        response = self.client.post(status_create_url, data, follow=True)
        self.assertContains(response, "Статус успешно создан")

    def test_index(self):
        response = self.client.get("/statuses/")
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        response = self.client.get("/statuses/create/")
        self.assertEqual(response.status_code, 200)
        status_create_url = reverse("status_create")
        data = {"name": "fun status"}
        response = self.client.post(status_create_url, data, follow=True)
        self.assertContains(response, "Статус успешно создан")

    def test_update(self):
        new_form_data = {
            "name": "Updated Status",
        }
        status_id = Status.objects.get(name="fun status").id
        update_url = reverse("status_update", kwargs={"status_id": status_id})
        response = self.client.post(
            update_url,
            data=new_form_data,
            follow=True
        )
        self.assertContains(response, "Updated Status")
