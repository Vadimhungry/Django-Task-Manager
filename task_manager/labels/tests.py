from django.test import TestCase, Client
from django.urls import reverse
from .models import Label


class LabelTest(TestCase):
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

        response = self.client.get("/labels/create/")
        self.assertEqual(response.status_code, 200)
        label_create_url = reverse("label_create")
        data = {"name": "fun label"}

        response = self.client.post(label_create_url, data, follow=True)
        self.assertContains(response, "Метка успешно создана")

    def test_index(self):
        response = self.client.get("/labels/")
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        response = self.client.get("/labels/create/")
        self.assertEqual(response.status_code, 200)
        label_create_url = reverse("label_create")
        data = {"name": "fun status"}
        response = self.client.post(label_create_url, data, follow=True)
        self.assertContains(response, "Метка успешно создана")

    def test_update(self):
        new_form_data = {
            "name": "Updated Label",
        }
        label_id = Label.objects.get(name="fun label").id
        update_url = reverse("label_update", kwargs={"label_id": label_id})
        response = self.client.post(update_url, data=new_form_data, follow=True)
        self.assertContains(response, "Updated Label")
