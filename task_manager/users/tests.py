from django.test import TestCase, Client
from django.urls import reverse, reverse_lazy
from .models import CustomUser


# Create your tests here.
class TestUsers(TestCase):
    fixtures = ['user.json',]
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

        # Send a POST request with valid form data
        response = self.client.post(reverse("user_create"), valid_form_data)

        user = CustomUser.objects.get(username="testuser")
        print('+++++++++++++')
        print(user.username)
        print(user.id)
        print('+++++++++++++')

        # Check if the response redirects to the 'user_login' URL
        self.assertRedirects(response, reverse("user_login"), status_code=302)




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

    def test_user_update(self):
        valid_form_data = {
            "first_name": "Ivan",
            "last_name": "Durak",
            "username": "testuser",
            "password1": "Testpassword12345",
            "password2": "Testpassword12345",
        }

        self.client.post(reverse("user_create"), valid_form_data)
        user_id = CustomUser.objects.get(username="testuser").id
        response = self.client.get(f"/users/{user_id}/update/")
        self.assertEqual(response.status_code, 200)

        new_data = {
            "first_name": "new_guy",
            "last_name": "new_guy",
            "username": "updated_testuser",
            "password1": "uuuTestpassword12345",
            "password2": "uuuTestpassword12345",
        }
        url = reverse("user_update", kwargs={"user_id": user_id})
        response = self.client.post(url, new_data)
        self.assertRedirects(
            response,
            reverse_lazy("users_index"),
            status_code=302
        )
